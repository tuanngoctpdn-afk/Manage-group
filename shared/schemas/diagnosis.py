"""
Schema dữ liệu kết quả nhận diện AI (Object Detection & Classification).
Phục vụ Task 3.2, 5.2, 6.1, 6.2.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x_min: float = Field(..., description="Tọa độ x góc trên bên trái (chuẩn hóa 0.0 - 1.0)")
    y_min: float = Field(..., description="Tọa độ y góc trên bên trái (chuẩn hóa 0.0 - 1.0)")
    x_max: float = Field(..., description="Tọa độ x góc dưới bên phải (chuẩn hóa 0.0 - 1.0)")
    y_max: float = Field(..., description="Tọa độ y góc dưới bên phải (chuẩn hóa 0.0 - 1.0)")


class DetectedAnomaly(BaseModel):
    disease_id: str = Field(..., description="Mã bệnh tương ứng trong DISEASE_TAXONOMY")
    disease_name_vi: str = Field(..., description="Tên tiếng Việt của bệnh/sâu")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Độ tin cậy của AI (0.0 - 1.0)")
    bbox: Optional[BoundingBox] = None


class AIInferenceResponse(BaseModel):
    inference_id: str
    model_version: str
    inference_time_ms: float
    is_healthy: bool
    detections: List[DetectedAnomaly]


class FruitGradeEvaluation(BaseModel):
    grade: str = Field(..., description="Phẩm cấp quả mít: 'Grade A', 'Grade B', 'Grade C', 'Reject'")
    estimated_weight_kg: float
    surface_defect_ratio: float = Field(..., description="Tỷ lệ khuyết tật/sẹo bề mặt (0.0 - 1.0)")
    is_export_ready: bool
    reasons: List[str]

