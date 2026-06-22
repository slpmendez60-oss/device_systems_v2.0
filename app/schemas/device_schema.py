from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeviceCreate(BaseModel):
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str] = None


class DeviceUpdate(BaseModel):
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str] = None
    is_available: bool


class DevicePatch(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    device_type: Optional[str] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str]
    is_available: bool
    created_at: datetime

    model_config = {"from_attributes": True}