"""
Schema dữ liệu cảm biến IoT tại vườn mít.
Phục vụ Task 4.1, 4.2, 7.2.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class OrchardTelemetry(BaseModel):
    device_id: str = Field(..., description="Mã định danh thiết bị biên / sensor hub")
    orchard_id: str = Field(..., description="Mã định danh vườn mít")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    temperature_celsius: float = Field(..., description="Nhiệt độ môi trường (°C)")
    air_humidity_percent: float = Field(..., description="Độ ẩm không khí (%)")
    soil_moisture_percent: float = Field(..., description="Độ ẩm đất (%)")
    light_lux: Optional[float] = Field(None, description="Cường độ ánh sáng (Lux)")
    rainfall_detected: Optional[bool] = Field(False, description="Có mưa hay không")


class EdgeAnomalyAlert(BaseModel):
    alert_id: str
    device_id: str
    orchard_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    disease_id: str
    confidence: float
    snapshot_image_url: Optional[str] = None
    telemetry_snapshot: Optional[OrchardTelemetry] = None

