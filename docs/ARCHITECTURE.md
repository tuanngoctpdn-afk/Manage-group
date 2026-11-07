# Kiến Trúc Hệ Thống (System Architecture)

Dự án **Smart Jackfruit AgriTech** được thiết kế theo mô hình **Microservices & Event-Driven Architecture** kết hợp tính toán biên (**Edge Computing**), giải quyết toàn diện 7 mục tiêu từ thu thập dữ liệu, phân tích AI, xử lý biên đến ứng dụng Web/Mobile.

---

## 1. Sơ Đồ Kiến Trúc Tổng Thể

```
+-----------------------------------------------------------------------------------+
|                            NGƯỜI DÙNG & NGOẠI VI                                  |
|                                                                                   |
|  [Bà Con Nông Dân]           [Cán Bộ Nông Nghiệp / Hợp Tác Xã]     [Vườn Mít IoT] |
|   Mobile App (Flutter)            Web Dashboard (Next.js)           Camera + Sensor|
+----------+---------------------------------+-------------------------------+------+
           |                                 |                               |
           v                                 v                               |
+----------+---------------------------------+-------+                       |
|           KONG / NGINX API GATEWAY (Port 8000)     |                       |
+----+-------------------+--------------------+------+                       |
     |                   |                    |                              |
     v                   v                    v                              |
+----+----------+  +-----+----------+  +------+------------+                 |
|  AI Inference |  | Recommendation |  | Core Orchard API  |                 |
|    Service    |  |    Service     |  |    (Quản lý vườn) |                 |
|   (FastAPI)   |  |   (FastAPI)    |  |    (FastAPI)      |                 |
|  (Port 8001)  |  |  (Port 8002)   |  |   (Port 8003)     |                 |
+-------+-------+  +-----+----------+  +------+------------+                 |
        |                |                    |                              |
        +--------+-------+                    |                              |
                 v                            v                              |
        [PostgreSQL + Redis]         [PostgreSQL DB]                         |
                                                                             |
+----------------------------------------------------------------------------+------+
|                         HẠ TẦNG IOT & TÍNH TOÁN BIÊN                              |
|                                                                                   |
|  [Edge Device (Jetson / RPi)] -------- MQTT Broker (Mosquitto:1883)               |
|   - Real-time video scan                |                                         |
|   - Sensor read (Temp, Humid, Soil)     v                                         |
|   - Local TFLite Alert -------> IoT Ingestion Gateway Service                      |
|                                         |                                         |
|                                         v                                         |
|                                 [TimescaleDB / InfluxDB]                          |
+-----------------------------------------------------------------------------------+
```

---

## 2. Chi Tiết Các Phân Hệ & Microservices

### 2.1. Phân hệ Nghiên cứu & Huấn luyện AI (`ai-pipeline/`)
- **Mục tiêu**: Thực hiện Tasks 2.1, 2.2, 3.1, 3.2.
- **Workflow**:
  1. `datasets/`: Thu thập ảnh từ khảo sát thực địa (Task 1.1, 2.1), lọc trùng, chuẩn hóa ảnh RGB 640x640, sinh nhãn định dạng YOLO/PASCAL VOC/COCO.
  2. `training/`: Huấn luyện song song mô hình Object Detection (YOLOv8, YOLOv11) và Classification (EfficientNetV2, ResNet50).
  3. `evaluation/`: So sánh mAP@0.5, mAP@0.5:0.95, Recall, FPS, Latency và kích thước mô hình.
  4. `export/`: Đóng gói mô hình sang `.onnx`, `.tflite` (quantization FP16/INT8) để nhúng vào Mobile và Edge.

### 2.2. Phân hệ IoT & Tính Toán Biên (`edge/` & `services/iot-gateway-service/`)
- **Mục tiêu**: Thực hiện Tasks 4.1, 4.2.
- **Tại vườn mít (Edge Device)**:
  - Thiết bị: Raspberry Pi 4 / Nvidia Jetson Nano kết hợp Camera module và cảm biến nhiệt ẩm không khí, cảm biến độ ẩm đất.
  - Xử lý cục bộ: Đọc cảm biến định kỳ (mỗi 5 phút), chụp ảnh định kỳ hoặc khi có chuyển động. Chạy model TFLite tối ưu để phát hiện dấu hiệu sâu đục quả ngay tại vườn.
  - Giao thức: Truyền tải dữ liệu qua **MQTT (Message Queuing Telemetry Transport)** với cơ chế lưu đệm ngoại tuyến (Offline Buffering) khi mất sóng 4G/WiFi.
- **IoT Gateway Service (Cloud)**:
  - Lắng nghe topic `orchard/+/sensors` và `orchard/+/alerts`.
  - Lưu trữ dữ liệu chuỗi thời gian (time-series) phục vụ biểu đồ giám sát và hệ khuyến nghị.

### 2.3. Dịch vụ AI Inference Microservice (`services/ai-service/`)
- **Mục tiêu**: Cung cấp API trực tuyến cho Mobile App và Web Portal (Task 3.2, 5.2, 6.2).
- **Tính năng**:
  - Endpoint `/api/v1/detect`: Tiếp nhận ảnh, trả về tọa độ bounding box sâu bệnh, tên bệnh, độ tin cậy (`confidence`).
  - Endpoint `/api/v1/quality-grading`: Phân loại phẩm cấp mít (Loại 1, 2, 3) dựa trên hình thái, kích thước và vết sẹo bề mặt (Task 6.2).

### 2.4. Dịch vụ Khuyến Nghị Thông Minh (`services/recommendation-service/`)
- **Mục tiêu**: Thực hiện Task 6.1.
- **Nguyên lý hoạt động**:
  - Nhận đầu vào: Loại bệnh vừa chẩn đoán + Điều kiện thời tiết (nhiệt độ cao, ẩm ướt, mưa bão) lấy từ IoT sensors.
  - Đưa ra giải pháp tổng hợp IPM (Quản lý dịch hại tổng hợp):
    - Biện pháp canh tác (tỉa cành, bao trái).
    - Biện pháp sinh học (sử dụng nấm đối kháng Trichoderma, ong ký sinh).
    - Biện pháp hóa học an toàn (hoạt chất thuốc bảo vệ thực vật nằm trong danh mục cấp phép, liều lượng và thời gian cách ly).

### 2.5. Dịch vụ Lõi Quản Lý Vườn & Dịch Tễ (`services/core-api-service/`)
- **Mục tiêu**: Thực hiện Task 7.1, 7.2.
- **Tính năng**:
  - Quản lý danh sách nông hộ, vị trí tọa độ GPS vườn mít.
  - Tổng hợp mật độ ổ dịch sâu bệnh theo tỉnh/huyện/xã để vẽ bản đồ nhiệt dịch tễ (Epidemiological Heatmap).
  - Gửi thông báo khẩn cấp (Push Notification) tới các hộ trong bán kính có nguy cơ lây lan bùng phát dịch (như rệp sáp, ruồi đục quả).

### 2.6. Khách hàng Ứng dụng Di động (`clients/mobile/`)
- **Mục tiêu**: Thực hiện Task 5.1, 5.2.
- **Công nghệ**: Flutter (Dart) tương thích cả Android và iOS.
- **Giao diện**: Camera Preview trực tiếp, quét AI real-time offline (qua TFLite) hoặc online (gọi API service), giao diện tiếng Việt thân thiện với bà con nông dân.

### 2.7. Nền tảng Web Giám sát (`clients/web/`)
- **Mục tiêu**: Thực hiện Task 7.1, 7.2.
- **Công nghệ**: Next.js / React + TailwindCSS + Leaflet/Mapbox GIS.
- **Giao diện**: Dashboard giám sát chỉ số khí hậu, cảnh báo sâu bệnh thời gian thực theo vùng địa lý.

