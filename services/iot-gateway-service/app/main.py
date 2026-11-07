"""
FastAPI Microservice tiếp nhận Telemetry và Quản lý kết nối thiết bị IoT vườn mít.
Tương ứng: Task 4.1, Task 7.2.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from services.iot_gateway_service.app.mqtt_subscriber import IoTIngestionSubscriber
from shared.schemas.telemetry import OrchardTelemetry

app = FastAPI(
    title="IoT Gateway & Ingestion Service",
    description="Microservice thu thập và đồng bộ dữ liệu cảm biến thời gian thực từ các vườn mít",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mqtt_broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
mqtt_broker_port = int(os.getenv("MQTT_BROKER_PORT", 1883))

subscriber = IoTIngestionSubscriber(broker_host=mqtt_broker_host, broker_port=mqtt_broker_port)

HTML_PATH = os.path.join(os.path.dirname(__file__), "static", "index.html")


@app.on_event("startup")
def startup_event():
    subscriber.start()


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "iot-gateway-service", "version": "1.0.0"}


@app.get("/ui", response_class=HTMLResponse, tags=["Standalone UI"])
def serve_ui():
    """Giao diện Standalone UI độc lập của Module IoT Gateway"""
    if os.path.exists(HTML_PATH):
        return FileResponse(HTML_PATH)
    return "<h1>Module IoT Gateway UI đang được khởi tạo...</h1>"


@app.get("/api/v1/telemetry/{orchard_id}", tags=["IoT Telemetry"])
def get_latest_orchard_telemetry(orchard_id: str):
    """
    Lấy chỉ số môi trường (nhiệt độ, ẩm độ không khí, ẩm độ đất) mới nhất của vườn mít.
    """
    telemetry = subscriber.latest_telemetry_cache.get(orchard_id)
    if not telemetry:
        # Trả về dữ liệu mô phỏng nếu chưa có gói tin thực
        return {
            "device_id": f"dev-{orchard_id}-edge",
            "orchard_id": orchard_id,
            "temperature_celsius": 29.5,
            "air_humidity_percent": 78.0,
            "soil_moisture_percent": 65.2,
            "rainfall_detected": False,
            "is_simulated": True
        }
    return telemetry

