"""
FastAPI Microservice quản lý Nông hộ, Vườn Mít và Bản đồ Dịch Tễ vùng.
Tương ứng: Task 7.1, Task 7.2.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from services.core_api_service.app.routes.outbreak_map import router as outbreak_router

app = FastAPI(
    title="Core Orchard & Regional Disease API",
    description="Microservice quản lý cơ sở dữ liệu vườn mít, nông hộ và giám sát dịch tễ trên nền tảng Web",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(outbreak_router)

HTML_PATH = os.path.join(os.path.dirname(__file__), "static", "index.html")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "core-api-service", "version": "1.0.0"}


@app.get("/ui", response_class=HTMLResponse, tags=["Standalone UI"])
def serve_ui():
    """Giao diện Standalone UI độc lập của Module Quản lý Vườn & Dịch tễ"""
    if os.path.exists(HTML_PATH):
        return FileResponse(HTML_PATH)
    return "<h1>Module Quản Lý Vườn UI đang được khởi tạo...</h1>"

