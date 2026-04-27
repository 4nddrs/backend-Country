from urllib.parse import quote

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.crud import camera as crud_camera
from app.schemas.camera import Camera, CameraCreate, CameraUpdate
from app.services.camera_stream import stream_manager

import asyncio
from typing import List

router = APIRouter(prefix="/cameras", tags=["cameras"])


def _build_rtsp_url(cam: dict) -> str:
    """Construct RTSP URL encoding special characters in the password."""
    password = quote(cam["rtsp_password"], safe="")
    return (
        f"rtsp://{cam['rtsp_user']}:{password}"
        f"@{cam['ip']}:{cam['rtsp_port']}"
        f"{cam['stream_path']}"
    )


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

@router.post("/", response_model=Camera, status_code=status.HTTP_201_CREATED)
async def create_camera(camera_in: CameraCreate):
    camera = await crud_camera.create_camera(camera_in)
    if not camera:
        raise HTTPException(status_code=400, detail="No se pudo crear la cámara")
    return camera


@router.get("/", response_model=List[Camera])
async def list_cameras():
    return await crud_camera.get_all_cameras()


@router.get("/{idCamera}", response_model=Camera)
async def get_camera(idCamera: int):
    camera = await crud_camera.get_camera(idCamera)
    if not camera:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")
    return camera


@router.put("/{idCamera}", response_model=Camera)
async def update_camera(idCamera: int, camera_in: CameraUpdate):
    camera = await crud_camera.update_camera(idCamera, camera_in)
    if not camera:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")
    return camera


@router.delete("/{idCamera}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(idCamera: int):
    stream_manager.stop(idCamera)
    result = await crud_camera.delete_camera(idCamera)
    if not result:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")


# ---------------------------------------------------------------------------
# Stream control
# ---------------------------------------------------------------------------

@router.post("/{idCamera}/connect", status_code=status.HTTP_200_OK)
async def connect_camera(idCamera: int):
    """
    Starts the RTSP capture thread for this camera.
    Returns immediately; the stream becomes available at /{idCamera}/stream.
    """
    cam = await crud_camera.get_camera_credentials(idCamera)
    if not cam:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")
    if not cam.get("is_active"):
        raise HTTPException(status_code=400, detail="La cámara está desactivada")

    rtsp_url = _build_rtsp_url(cam)
    stream_manager.start(idCamera, rtsp_url)
    return {"status": "connecting", "idCamera": idCamera}


@router.post("/{idCamera}/disconnect", status_code=status.HTTP_200_OK)
async def disconnect_camera(idCamera: int):
    """Stops the capture thread and releases the RTSP connection."""
    stream_manager.stop(idCamera)
    return {"status": "disconnected", "idCamera": idCamera}


@router.get("/{idCamera}/status")
async def camera_status(idCamera: int):
    return {
        "idCamera": idCamera,
        "streaming": stream_manager.is_running(idCamera),
    }


# ---------------------------------------------------------------------------
# MJPEG stream endpoint
# ---------------------------------------------------------------------------

@router.get("/{idCamera}/stream")
async def video_stream(idCamera: int):
    """
    Returns a multipart/x-mixed-replace MJPEG stream.
    Auto-starts the capture thread if not yet running.
    The browser consumes this via:  <img src="http://backend/cameras/{id}/stream" />
    """
    cam = await crud_camera.get_camera_credentials(idCamera)
    if not cam:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")

    if not stream_manager.is_running(idCamera):
        rtsp_url = _build_rtsp_url(cam)
        stream_manager.start(idCamera, rtsp_url)
        # Allow the capture thread a moment to connect before streaming
        await asyncio.sleep(2)

    return StreamingResponse(
        stream_manager.generate_frames(idCamera),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
