from pydantic import BaseModel
from typing import Optional


class CameraBase(BaseModel):
    name: str
    ip: str
    rtsp_port: int = 554
    stream_path: str = "/stream1"
    rtsp_user: str
    is_active: bool = True
    fk_idOwner: int


class CameraCreate(CameraBase):
    rtsp_password: str


class CameraUpdate(BaseModel):
    name: Optional[str] = None
    ip: Optional[str] = None
    rtsp_port: Optional[int] = None
    stream_path: Optional[str] = None
    rtsp_user: Optional[str] = None
    rtsp_password: Optional[str] = None
    is_active: Optional[bool] = None
    fk_idOwner: Optional[int] = None


class Camera(CameraBase):
    """Response schema — rtsp_password is intentionally excluded."""
    idCamera: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
