"""
Bộ quy tắc suy luận khuyến nghị thông minh (Expert Advisory Engine).
Phục vụ trực tiếp Task 6.1: Provision of pest and disease treatment recommendations
based on recognition results, weather, and environmental data.
"""
from typing import List, Optional
from pydantic import BaseModel
from shared.taxonomy.diseases import DISEASE_TAXONOMY, SeverityLevel
from shared.schemas.telemetry import OrchardTelemetry


class AdvisoryRequest(BaseModel):
    disease_id: str
    confidence: float
    telemetry: Optional[OrchardTelemetry] = None
    orchard_age_years: Optional[float] = 3.0


class TreatmentPlan(BaseModel):
    urgency_level: str
    disease_summary: str
    cultural_actions: List[str]
    biological_solutions: List[str]
    chemical_treatments: List[str]
    environmental_warning: Optional[str] = None


class SmartAdvisoryEngine:
    def generate_recommendations(self, request: AdvisoryRequest) -> TreatmentPlan:
        disease = DISEASE_TAXONOMY.get(request.disease_id)
        if not disease:
            return TreatmentPlan(
                urgency_level="Unknown",
                disease_summary="Không xác định được bệnh cụ thể.",
                cultural_actions=["Liên hệ cán bộ khuyến nông địa phương để kiểm tra thực tế."],
                biological_solutions=[],
                chemical_treatments=[]
            )

        cultural = [disease.cultural_control]
        chemical = []
        biological = []
        warning = None

        for ingredient in disease.recommended_active_ingredients:
            if "Bacillus" in ingredient or "Dầu khoáng" in ingredient:
                biological.append(f"Chế phẩm sinh học: {ingredient}")
            else:
                chemical.append(f"Thuốc có hoạt chất: {ingredient} (Tuân thủ thời gian cách ly PHI)")

        # Phân tích kết hợp yếu tố môi trường (Task 6.1)
        if request.telemetry:
            # Nếu ẩm độ không khí > 85% hoặc có mưa -> Nấm phát triển rất nhanh
            if request.telemetry.air_humidity_percent > 85 or request.telemetry.rainfall_detected:
                warning = (
                    f"CẢNH BÁO MÔI TRƯỜNG: Độ ẩm không khí đang cao ({request.telemetry.air_humidity_percent}%), "
                    "thích hợp cho nấm thối quả (Rhizopus / Phytophthora) bùng phát lây lan nhanh! "
                    "Không nên phun thuốc hóa học ngay khi trời sắp mưa để tránh rửa trôi."
                )
                cultural.append("Khơi thông rãnh thoát nước vườn, tránh đọng nước quanh gốc cây.")

            if request.telemetry.temperature_celsius > 35:
                warning = "Nhiệt độ môi trường cao trên 35°C, lưu ý phun thuốc vào sáng sớm hoặc chiều mát để tránh cháy lá."

        urgency = "KHẨN CẤP" if disease.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH] else "TRUNG BÌNH"

        return TreatmentPlan(
            urgency_level=urgency,
            disease_summary=f"{disease.vietnamese_name} ({disease.scientific_name}). Triệu chứng: {disease.primary_symptoms}",
            cultural_actions=cultural,
            biological_solutions=biological,
            chemical_treatments=chemical,
            environmental_warning=warning
        )

