"""
Data Models cho Nông hộ, Vườn Mít và Nhật ký dịch bệnh.
Phục vụ Task 7.1, 7.2.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class OrchardHousehold(BaseModel):
    id: str = Field(..., description="Mã nông hộ / vườn mít")
    owner_name: str = Field(..., description="Tên chủ hộ")
    phone: str
    province: str = Field(..., description="Tỉnh / Thành phố (ví dụ: Tiền Giang, Đồng Nai, Đắk Lắk)")
    district: str = Field(..., description="Quận / Huyện")
    latitude: float
    longitude: float
    area_hectares: float
    jackfruit_variety: str = Field(default="Mít Thái Changai", description="Giống mít chính")
    iot_connected: bool = Field(default=False)


class OutbreakRegionSummary(BaseModel):
    region_name: str
    total_orchards: int
    infected_orchards: int
    dominant_disease: str
    risk_level: str  # Safe, Warning, Outbreak
    coordinates: List[float]  # [lat, lng]

