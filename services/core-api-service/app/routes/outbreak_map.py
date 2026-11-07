"""
Routes phục vụ Bản đồ dịch tễ học và giám sát tình hình sâu bệnh theo vùng.
Tương ứng trực tiếp: Task 7.1 (Regional pest and disease situations) & Task 7.2 (Data connectivity).
"""
from fastapi import APIRouter
from typing import List
from services.core_api_service.app.models.orchard import OrchardHousehold, OutbreakRegionSummary

router = APIRouter(prefix="/api/v1", tags=["Regional Outbreak & Orchards"])

# Dữ liệu mô phỏng các vùng trồng mít trọng điểm tại Việt Nam
SAMPLE_ORCHARDS: List[OrchardHousehold] = [
    OrchardHousehold(
        id="TG-001",
        owner_name="Nguyễn Văn An",
        phone="0912345678",
        province="Tiền Giang",
        district="Cái Bè",
        latitude=10.3341,
        longitude=105.9238,
        area_hectares=2.5,
        jackfruit_variety="Mít Thái Changai",
        iot_connected=True
    ),
    OrchardHousehold(
        id="DN-002",
        owner_name="Trần Thị Bình",
        phone="0987654321",
        province="Đồng Nai",
        district="Cẩm Mỹ",
        latitude=10.8921,
        longitude=107.2412,
        area_hectares=4.0,
        jackfruit_variety="Mít Ruột Đỏ Indo",
        iot_connected=True
    ),
    OrchardHousehold(
        id="DL-003",
        owner_name="Lê Hoàng Cường",
        phone="0901234888",
        province="Đắk Lắk",
        district="Cư M'gar",
        latitude=12.8251,
        longitude=108.0645,
        area_hectares=5.2,
        jackfruit_variety="Mít Thái Siêu Sớm",
        iot_connected=False
    )
]


@router.get("/orchards", response_model=List[OrchardHousehold])
def list_orchards():
    """Danh sách các nông hộ và vườn mít được kết nối hệ thống (Task 7.2)"""
    return SAMPLE_ORCHARDS


@router.get("/outbreak-map", response_model=List[OutbreakRegionSummary])
def get_outbreak_map_data():
    """
    Tổng hợp dữ liệu dịch bệnh theo khu vực hiển thị lên bản đồ Web GIS (Task 7.1)
    """
    return [
        OutbreakRegionSummary(
            region_name="Cái Bè - Tiền Giang",
            total_orchards=45,
            infected_orchards=8,
            dominant_disease="Sâu đục trái mít (Diaphania caesalis)",
            risk_level="Warning",
            coordinates=[10.3341, 105.9238]
        ),
        OutbreakRegionSummary(
            region_name="Cẩm Mỹ - Đồng Nai",
            total_orchards=62,
            infected_orchards=3,
            dominant_disease="Bệnh thối mềm (Rhizopus artocarpi)",
            risk_level="Safe",
            coordinates=[10.8921, 107.2412]
        ),
        OutbreakRegionSummary(
            region_name="Cư M'gar - Đắk Lắk",
            total_orchards=38,
            infected_orchards=14,
            dominant_disease="Nứt thân chảy mủ (Phytophthora palmivora)",
            risk_level="Outbreak",
            coordinates=[12.8251, 108.0645]
        )
    ]

