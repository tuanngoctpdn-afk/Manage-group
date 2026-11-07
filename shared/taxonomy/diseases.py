"""
Danh mục chuẩn hóa định danh sâu bệnh hại cây mít tại Việt Nam.
Ánh xạ trực tiếp từ Task 1.1, Task 1.2 và phục vụ Task 2.1, 2.2, 3.1, 6.1.
"""
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel


class JackfruitPart(str, Enum):
    LEAF = "leaf"       # Lá
    STEM = "stem"       # Thân, gốc
    FRUIT = "fruit"     # Quả / Trái
    FLOWER = "flower"   # Hoa / Chồi non


class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DiseaseInfo(BaseModel):
    id: str
    vietnamese_name: str
    scientific_name: str
    target_parts: List[JackfruitPart]
    severity: SeverityLevel
    primary_symptoms: str
    recommended_active_ingredients: List[str]
    cultural_control: str


DISEASE_TAXONOMY: Dict[str, DiseaseInfo] = {
    "JF_HEALTHY": DiseaseInfo(
        id="JF_HEALTHY",
        vietnamese_name="Cây / Quả khỏe mạnh",
        scientific_name="Normal healthy condition",
        target_parts=[JackfruitPart.LEAF, JackfruitPart.STEM, JackfruitPart.FRUIT],
        severity=SeverityLevel.LOW,
        primary_symptoms="Gai nở đều đặn, màu vỏ sáng, lá xanh bóng, thân cây liền lạc không chảy mủ.",
        recommended_active_ingredients=[],
        cultural_control="Duy trì bón phân cân đối N-P-K kết hợp phân hữu cơ vi sinh, tỉa cành định kỳ."
    ),
    "JF_FRUIT_BORER": DiseaseInfo(
        id="JF_FRUIT_BORER",
        vietnamese_name="Sâu đục trái mít",
        scientific_name="Diaphania caesalis",
        target_parts=[JackfruitPart.FRUIT],
        severity=SeverityLevel.HIGH,
        primary_symptoms="Lỗ đục tròn trên vỏ quả, đùn hạt phân màu nâu/đen ra ngoài, quả dễ thối nhũn và rụng sớm.",
        recommended_active_ingredients=["Bacillus thuringiensis (Bt)", "Emamectin benzoate", "Spinetoram"],
        cultural_control="Bao trái bằng túi chuyên dụng khi quả đạt đường kính 7-10cm, thu gom và tiêu hủy quả nhiễm sâu."
    ),
    "JF_SOFT_ROT": DiseaseInfo(
        id="JF_SOFT_ROT",
        vietnamese_name="Bệnh thối mềm / Thối đen trái",
        scientific_name="Rhizopus artocarpi / Phomopsis artocarpina",
        target_parts=[JackfruitPart.FRUIT, JackfruitPart.FLOWER],
        severity=SeverityLevel.CRITICAL,
        primary_symptoms="Vết úng màu nâu đậm lan nhanh trên quả, hình thành lớp nấm sợi đen như bông xơ hoặc hạt than.",
        recommended_active_ingredients=["Copper Hydroxide", "Mancozeb", "Metalaxyl"],
        cultural_control="Vệ sinh vườn sau mưa, tránh làm trầy xước vỏ quả, tạo thông thoáng cho tán lá."
    ),
    "JF_PHYTOPHTHORA_CANKER": DiseaseInfo(
        id="JF_PHYTOPHTHORA_CANKER",
        vietnamese_name="Bệnh nứt thân chảy mủ",
        scientific_name="Phytophthora palmivora",
        target_parts=[JackfruitPart.STEM],
        severity=SeverityLevel.CRITICAL,
        primary_symptoms="Vỏ thân gốc nứt toác, ứa mủ vàng cam sau đó chuyển nâu đen, gỗ thân bị hoại tử thâm tím.",
        recommended_active_ingredients=["Phosphonate (Agri-Fos)", "Metalaxyl-M", "Dimethomorph"],
        cultural_control="Cạo sạch phần vỏ thâm đen quét thuốc gốc đồng, thoát nước tốt mùa mưa, bón nấm Trichoderma định kỳ."
    ),
    "JF_MEALYBUG": DiseaseInfo(
        id="JF_MEALYBUG",
        vietnamese_name="Rệp sáp hại mít",
        scientific_name="Planococcus lilacinus",
        target_parts=[JackfruitPart.FRUIT, JackfruitPart.FLOWER],
        severity=SeverityLevel.MEDIUM,
        primary_symptoms="Lớp phấn trắng phủ kín kẽ gai mít và cuống quả, tạo mật ngọt dẫn dụ nấm bồ hóng đen xì.",
        recommended_active_ingredients=["Dầu khoáng nông nghiệp", "Spirotetramat", "Buprofezin"],
        cultural_control="Diệt trừ kiến đen tha rệp, phun vòi nước áp lực cao vào kẽ quả để rửa trôi rệp non."
    ),
    "JF_LEAF_SPOT": DiseaseInfo(
        id="JF_LEAF_SPOT",
        vietnamese_name="Bệnh đốm lá mít",
        scientific_name="Colletotrichum sp.",
        target_parts=[JackfruitPart.LEAF],
        severity=SeverityLevel.LOW,
        primary_symptoms="Các đốm tròn màu nâu vàng có viền sẫm trên bề mặt phiến lá, tâm đốm khô rách thủng.",
        recommended_active_ingredients=["Azoxystrobin", "Chlorothalonil"],
        cultural_control="Tỉa bớt cành tăm, thu gom lá rụng tiêu hủy, không tưới đẫm lên tán lúc chiều tối."
    )
}

