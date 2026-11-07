"""
FastAPI Microservice cho Hệ thống Khuyến Nghị Nông Nghiệp Thông Minh.
Tương ứng: Task 6.1.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from services.recommendation_service.app.rules.advisory_engine import (
    SmartAdvisoryEngine,
    AdvisoryRequest,
    TreatmentPlan
)

app = FastAPI(
    title="Smart Agricultural Recommendation Service",
    description="Microservice khuyến nghị biện pháp phòng trừ sâu bệnh trên mít kết hợp dữ liệu AI và IoT",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = SmartAdvisoryEngine()

HTML_PATH = os.path.join(os.path.dirname(__file__), "static", "index.html")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "recommendation-service", "version": "1.0.0"}


@app.get("/ui", response_class=HTMLResponse, tags=["Standalone UI"])
def serve_ui():
    """Giao diện Standalone UI độc lập của Module Khuyến Nông"""
    if os.path.exists(HTML_PATH):
        return FileResponse(HTML_PATH)
    return "<h1>Module Khuyến Nông UI đang được khởi tạo...</h1>"


@app.post("/api/v1/recommend", response_model=TreatmentPlan, tags=["Advisory"])
def get_recommendation(request: AdvisoryRequest):
    """
    Tiếp nhận mã bệnh từ AI và chỉ số môi trường từ IoT, sinh ra phác đồ điều trị chi tiết.
    """
    return engine.generate_recommendations(request)

