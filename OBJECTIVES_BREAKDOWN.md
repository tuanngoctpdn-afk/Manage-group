# Kế Hoạch & Phân Chia Nội Dung Kỹ Thuật Theo Từng Mục Tiêu (Objective Breakdown)

Tài liệu này chi tiết hóa toàn bộ 7 Mục tiêu nghiên cứu từ `object.md`, phân định rõ ràng phạm vi công việc, mã nguồn phụ trách, đầu ra (deliverables) và nhánh Git (branch) tương ứng trong repository: `https://gitlab.com/sdc-group1230845/sdc-village-manage.git`.

---

## Danh Mục Phân Chia Nhánh Git Theo Mục Tiêu

| Mục Tiêu (Objective) | Tên Nhánh Git (Branch) | Mô Tả Trọng Tâm | Thư Mục / Module Chính |
| :--- | :--- | :--- | :--- |
| **Nền tảng chung** | `establish` | Cấu trúc nền tảng monorepo, Docker Compose, Micro-Frontend Hub, CI/CD | Root, `docker-compose.yml`, `docs/`, `shared/` |
| **Objective 1** | `obj-1-pest-survey-symptoms` | Khảo sát thực địa & Phân tích triệu chứng sâu bệnh trên mít | `shared/taxonomy/`, `docs/DISEASE_TAXONOMY.md` |
| **Objective 2** | `obj-2-dataset-annotation` | Xây dựng, chuẩn hóa & gán nhãn tập dữ liệu ảnh AI | `ai-pipeline/datasets/` |
| **Objective 3** | `obj-3-deep-learning-models` | Nghiên cứu, huấn luyện & benchmark mô hình (CNN, YOLO, EfficientNet) | `ai-pipeline/training/`, `ai-pipeline/evaluation/`, `ai-pipeline/export/` |
| **Objective 4** | `obj-4-iot-edge-cloud` | Thu thập dữ liệu IoT, tính toán biên (Edge AI) & MQTT Gateway | `edge/`, `services/iot-gateway-service/` |
| **Objective 5** | `obj-5-mobile-app` | Ứng dụng di động (Flutter) quét camera chẩn đoán thời gian thực | `clients/mobile/` |
| **Objective 6** | `obj-6-smart-recommendation` | Hệ thống khuyến nghị phòng trừ thông minh & Phân loại phẩm cấp mít | `services/recommendation-service/`, `services/ai-service/app/engine/grader.py` |
| **Objective 7** | `obj-7-web-remote-monitoring` | Nền tảng Web GIS giám sát dịch tễ vùng & kết nối dữ liệu nông hộ | `clients/web/`, `services/core-api-service/` |

---

## Chi Tiết Nội Dung Từng Mục Tiêu (Objective Details)

### 📌 Objective 1: Nghiên cứu các loài sâu bệnh hại phổ biến trên cây mít và quả mít tại Việt Nam
- **Tasks**:
  - `Task 1.1`: Khảo sát thực địa và thu thập dữ liệu về các loài sâu bệnh hại chính (Đồng bằng sông Cửu Long, Đông Nam Bộ, Tây Nguyên).
  - `Task 1.2`: Phân tích triệu chứng gây hại trên lá, thân và quả mít nhằm thiết lập tiêu chí nhận diện hình thái lâm sàng.
- **Mã nguồn & Tài liệu**:
  - `shared/taxonomy/diseases.py`: Định nghĩa danh mục bệnh chuẩn (Sâu đục trái, nấm thối đen, nứt thân xì mủ, rệp sáp, đốm lá).
  - `docs/DISEASE_TAXONOMY.md`: Bảng triệu chứng lâm sàng và tiêu chuẩn nhận dạng.
- **Đầu ra**:
  - Bảng tiêu chí nhận diện hình ảnh sâu bệnh cây mít tại Việt Nam.

---

### 📌 Objective 2: Xây dựng và phát triển bộ dữ liệu hình ảnh chuyên dụng về sâu bệnh hại mít
- **Tasks**:
  - `Task 2.1`: Thu thập và gán nhãn (annotation) hình ảnh sâu bệnh trên cây mít qua các giai đoạn sinh trưởng.
  - `Task 2.2`: Chuẩn hóa định dạng dữ liệu hình ảnh phục vụ huấn luyện mô hình AI (YOLO / COCO / VOC format).
- **Mã nguồn**:
  - `ai-pipeline/datasets/prepare_dataset.py`: Script tự động lọc, chuẩn hóa kích thước, chia tập train/val/test và sinh file `data.yaml`.
- **Đầu ra**:
  - Dataset chuẩn hóa sẵn sàng cho quá trình train Deep Learning.

---

### 📌 Objective 3: Nghiên cứu và ứng dụng kỹ thuật Học máy & Học sâu trong nhận diện sâu bệnh
- **Tasks**:
  - `Task 3.1`: Đánh giá so sánh hiệu năng các mô hình học sâu (CNN, YOLOv8/v11, EfficientNetV2, ResNet50).
  - `Task 3.2`: Đề xuất mô hình tối ưu cho việc phát hiện sớm sâu bệnh và xuất định dạng biên/di động (ONNX, TFLite).
- **Mã nguồn**:
  - `ai-pipeline/training/train_detector.py`: Script huấn luyện YOLOv8/v11 Object Detection.
  - `ai-pipeline/training/train_classifier.py`: Script huấn luyện EfficientNetV2 Classifier.
  - `ai-pipeline/evaluation/benchmark_models.py`: Bộ công cụ so sánh mAP@0.5, Precision, Recall, Latency, kích thước mô hình.
  - `ai-pipeline/export/export_tflite.py`: Bộ công cụ xuất và lượng tử hóa mô hình (INT8/FP16).
  - `services/ai-service/`: API suy luận trực tuyến kèm Standalone Web UI.
- **Đầu ra**:
  - Báo cáo benchmark đối sánh khoa học và bộ trọng số tối ưu (`.pt`, `.onnx`, `.tflite`).

---

### 📌 Objective 4: Thiết kế giải pháp phân tích và đánh giá dữ liệu trên nền tảng tính toán biên & đám mây
- **Tasks**:
  - `Task 4.1`: Triển khai đường ống thu thập dữ liệu (ingestion pipeline) từ thiết bị IoT (camera, cảm biến môi trường: nhiệt ẩm, đất).
  - `Task 4.2`: Phân tích dữ liệu thời gian thực trên thiết bị biên (Edge computing) và đồng bộ hóa với nền tảng Cloud.
- **Mã nguồn**:
  - `edge/sensor_collector.py`: Driver đọc cảm biến và gửi MQTT lên Cloud.
  - `edge/edge_infer.py`: Chạy nhận diện cục bộ với độ trễ thấp trên Jetson/Raspberry Pi.
  - `services/iot-gateway-service/`: Microservice tiếp nhận MQTT kèm Standalone Web UI.
- **Đầu ra**:
  - Đường ống dữ liệu IoT Edge-to-Cloud hoạt động liên tục với cơ chế lưu đệm ngoại tuyến.

---

### 📌 Objective 5: Phát triển phần mềm nhận diện sâu bệnh chạy trên thiết bị di động (Android/iOS)
- **Tasks**:
  - `Task 5.1`: Thiết kế UI/UX thân thiện với người nông dân, hỗ trợ quét trực tiếp qua camera điện thoại.
  - `Task 5.2`: Tích hợp mô hình nhận diện (Offline TFLite và Online API) với phản hồi chẩn đoán tức thì.
- **Mã nguồn**:
  - `clients/mobile/`: Toàn bộ ứng dụng Flutter (`lib/main.dart`, `lib/features/camera_scan/scan_screen.dart`, `pubspec.yaml`).
- **Đầu ra**:
  - File cài đặt ứng dụng Android (.apk) và iOS hỗ trợ quét thời gian thực tại vườn mít.

---

### 📌 Objective 6: Xây dựng hệ thống hỗ trợ khuyến nghị nông nghiệp thông minh cho cây mít
- **Tasks**:
  - `Task 6.1`: Đưa ra khuyến nghị giải pháp phòng trừ sâu bệnh dựa trên kết quả nhận diện, thời tiết và dữ liệu môi trường.
  - `Task 6.2`: Hỗ trợ phân loại phẩm cấp mít trong giai đoạn thu hoạch dựa trên xử lý hình ảnh (Grade A, B, C, Reject).
- **Mã nguồn**:
  - `services/recommendation-service/`: Quy tắc suy luận phác đồ IPM (canh tác, sinh học, hóa học an toàn) kèm Standalone Web UI.
  - `services/ai-service/app/engine/grader.py`: Đánh giá hình thái và phẩm cấp trái mít khi thu hoạch.
- **Đầu ra**:
  - Microservice cố vấn nông nghiệp thông minh tự động cảnh báo điều kiện bùng phát nấm bệnh.

---

### 📌 Objective 7: Phát triển hệ thống quan sát và giám sát dịch bệnh từ xa qua nền tảng Web
- **Tasks**:
  - `Task 7.1`: Phát triển ứng dụng Web phục vụ theo dõi tình hình sâu bệnh theo vùng địa lý thời gian thực.
  - `Task 7.2`: Hỗ trợ kết nối dữ liệu từ các nông hộ hoặc trang trại trồng mít riêng lẻ tới hệ thống IoT.
- **Mã nguồn**:
  - `clients/web/`: Web Dashboard Next.js trung tâm kèm chế độ Micro-Frontend Portal.
  - `services/core-api-service/`: Quản lý danh sách nông hộ, tọa độ GPS và bản đồ dịch tễ GIS kèm Standalone Web UI.
- **Đầu ra**:
  - Cổng thông tin web quản lý tập trung cho Hợp tác xã và Chi cục Bảo vệ Thực vật.
