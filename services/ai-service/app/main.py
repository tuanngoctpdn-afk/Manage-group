"""
FastAPI Microservice phục vụ AI Inference trực tuyến cho Mobile App và IoT Cloud.
Tương ứng: Task 3.2, Task 5.2, Task 6.2.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import sys
import os

# Thêm đường dẫn project root để load module shared
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from services.ai_service.app.engine.detector import JackfruitInferenceEngine
from services.ai_service.app.engine.grader import JackfruitQualityGrader
from shared.schemas.diagnosis import AIInferenceResponse, FruitGradeEvaluation

app = FastAPI(
    title="Jackfruit AI Inference Microservice",
    description="Microservice cung cấp API nhận diện sâu bệnh và phân loại phẩm cấp quả mít",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = JackfruitInferenceEngine()
grader = JackfruitQualityGrader()

HTML_PATH = os.path.join(os.path.dirname(__file__), "static", "index.html")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "ai-service", "version": "1.0.0"}


@app.get("/ui", response_class=HTMLResponse, tags=["Standalone UI"])
def serve_ui():
    """Giao diện Standalone UI độc lập của Module AI"""
    if os.path.exists(HTML_PATH):
        return FileResponse(HTML_PATH)
    return "<h1>Module AI UI đang được khởi tạo...</h1>"


@app.post("/api/v1/detect", response_model=AIInferenceResponse, tags=["AI Diagnosis"])
async def detect_pests_and_diseases(file: UploadFile = File(...)):
    """
    Endpoint nhận ảnh từ điện thoại di động hoặc camera vườn và trả về kết quả chẩn đoán.
    Phục vụ Task 3.2, 5.2.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Tập tin tải lên phải là định dạng hình ảnh.")
    
    contents = await file.read()
    results = engine.predict_image(contents)
    return results


@app.post("/api/v1/quality-grading", response_model=FruitGradeEvaluation, tags=["Harvest Quality"])
async def evaluate_jackfruit_grade(file: UploadFile = File(...)):
    """
    Endpoint phân loại phẩm cấp trái mít khi thu hoạch (Task 6.2).
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Tập tin tải lên phải là định dạng hình ảnh.")

    contents = await file.read()
    grade_result = grader.evaluate_harvest_quality(contents)
    return grade_result

