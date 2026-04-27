"""
Camera Stream Service
=====================
Manages MJPEG streaming from RTSP cameras using OpenCV.

Architecture:
- One background daemon thread per camera reads RTSP frames (blocking I/O).
- The thread encodes each frame as JPEG and stores it as `latest_frame`.
- FastAPI async generators read `latest_frame` and yield multipart chunks.
- When all clients disconnect, the capture thread stops automatically.

Future AI integration:
- To run YOLO inference, import your model inside `_capture_loop` and call
  `results = model(frame); frame = results[0].plot()` before cv2.imencode.
"""

import asyncio
import os
import threading
import time
import cv2
from typing import Optional
from dataclasses import dataclass, field

# Force RTSP over TCP so OpenCV never falls back to CAP_IMAGES.
# Must be set before any cv2.VideoCapture() call.
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

# Seconds to wait for an RTSP connection before giving up.
# Passing a params list to VideoCapture() causes "unsupported parameters in
# .open()" on builds that do not expose that API, so we use a thread-level
# timeout instead — it works on every OpenCV version.
_OPEN_TIMEOUT_SEC = 8.0


def _open_capture(rtsp_url: str) -> cv2.VideoCapture:
    """
    Open RTSP forcing the FFmpeg backend with a Python-level timeout.

    The blocking VideoCapture constructor runs in a daemon thread; if the RTSP
    handshake does not finish within _OPEN_TIMEOUT_SEC, the thread is abandoned
    (it will terminate on its own after the FFmpeg internal timeout) and a
    *closed* VideoCapture is returned so the capture loop retries shortly after.
    """
    result: list[cv2.VideoCapture | None] = [None]

    def _try() -> None:
        c = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
        c.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        result[0] = c

    t = threading.Thread(target=_try, daemon=True)
    t.start()
    t.join(timeout=_OPEN_TIMEOUT_SEC)

    cap = result[0]
    # cap is None  → thread still running (connection timed out at Python level)
    # not isOpened → thread finished but RTSP handshake failed
    if cap is None or not cap.isOpened():
        return cv2.VideoCapture()   # isOpened() → False → capture loop retries
    return cap


@dataclass
class _StreamState:
    rtsp_url: str
    running: bool = True
    latest_frame: Optional[bytes] = None
    client_count: int = 0
    thread: Optional[threading.Thread] = None
    # Per-stream lock guards latest_frame reads/writes
    frame_lock: threading.Lock = field(default_factory=threading.Lock)


class CameraStreamManager:
    """Singleton that owns all active RTSP capture threads."""

    def __init__(self) -> None:
        self._streams: dict[int, _StreamState] = {}
        self._dict_lock = threading.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self, camera_id: int, rtsp_url: str) -> None:
        """Start a capture thread for *camera_id* if not already running."""
        with self._dict_lock:
            if camera_id in self._streams:
                return  # already active
            state = _StreamState(rtsp_url=rtsp_url)
            self._streams[camera_id] = state

        t = threading.Thread(
            target=self._capture_loop,
            args=(camera_id, state),
            daemon=True,
            name=f"cam-{camera_id}",
        )
        state.thread = t
        t.start()

    def stop(self, camera_id: int) -> None:
        """Signal the capture thread to stop and remove the stream entry."""
        with self._dict_lock:
            state = self._streams.pop(camera_id, None)
        if state:
            state.running = False

    def is_running(self, camera_id: int) -> bool:
        with self._dict_lock:
            return camera_id in self._streams

    async def generate_frames(self, camera_id: int):
        """
        Async generator that yields MJPEG multipart chunks.
        Tracks connected clients; stops the thread when the last client exits.
        Closes the stream if no frame arrives within 12 seconds so the browser
        img.onError fires instead of hanging indefinitely.
        """
        self._add_client(camera_id)
        no_frame_since = asyncio.get_event_loop().time()
        try:
            while True:
                state = self._get_state(camera_id)
                if state is None or not state.running:
                    break

                with state.frame_lock:
                    frame = state.latest_frame

                if frame:
                    no_frame_since = asyncio.get_event_loop().time()
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                    )
                else:
                    # Close stream after 12 s with no frames so the frontend
                    # detects the failure via img onError / connection drop.
                    if asyncio.get_event_loop().time() - no_frame_since > 12:
                        break

                # ~30 fps cap; non-blocking so FastAPI event loop stays free
                await asyncio.sleep(0.033)
        finally:
            self._remove_client(camera_id)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_state(self, camera_id: int) -> Optional[_StreamState]:
        with self._dict_lock:
            return self._streams.get(camera_id)

    def _add_client(self, camera_id: int) -> None:
        state = self._get_state(camera_id)
        if state:
            state.client_count += 1

    def _remove_client(self, camera_id: int) -> None:
        state = self._get_state(camera_id)
        if state:
            state.client_count -= 1
            if state.client_count <= 0:
                self.stop(camera_id)

    def _capture_loop(self, camera_id: int, state: _StreamState) -> None:
        """
        Runs in a daemon thread.
        Reads frames from RTSP, encodes them as JPEG, stores latest.
        Reconnects automatically on stream loss.
        """
        cap = _open_capture(state.rtsp_url)
        consecutive_failures = 0

        while state.running:
            # ── Camera not open: wait and retry ───────────────────────
            if not cap.isOpened():
                cap.release()
                for _ in range(20):          # 2-second wait, interruptible
                    if not state.running:
                        return
                    time.sleep(0.1)
                cap = _open_capture(state.rtsp_url)
                continue

            ret, frame = cap.read()

            if not ret:
                consecutive_failures += 1
                # After 5 bad reads, force a full reconnect
                if consecutive_failures >= 5:
                    cap.release()
                    consecutive_failures = 0
                    for _ in range(20):      # 2-second reconnect delay
                        if not state.running:
                            return
                        time.sleep(0.1)
                    cap = _open_capture(state.rtsp_url)
                continue

            consecutive_failures = 0

            # ---------------------------------------------------------
            # AI HOOK: insert YOLO inference here in the future
            # Example:
            #   results = yolo_model(frame)
            #   frame = results[0].plot()
            # ---------------------------------------------------------

            ok, buffer = cv2.imencode(
                ".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 75]
            )
            if ok:
                with state.frame_lock:
                    state.latest_frame = buffer.tobytes()

        cap.release()


# Module-level singleton — imported by the router
stream_manager = CameraStreamManager()
