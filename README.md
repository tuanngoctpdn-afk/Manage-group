# Smart Jackfruit AgriTech Platform (Hệ Sinh Thái Nông Nghiệp Thông Minh Cho Cây Mít)

Hệ thống toàn diện ứng dụng Trí tuệ Nhân tạo (AI), Vạn vật kết nối (IoT - Edge/Cloud), Ứng dụng Di động và Nền tảng Web phục vụ nghiên cứu, nhận diện sâu bệnh và hỗ trợ canh tác mít tại Việt Nam.

Dự án được xây dựng bám sát theo các mục tiêu nghiên cứu trong [object.md](object.md).

---

## 1. Bản Đồ Ánh Xạ Giữa Mục Tiêu Nghiên Cứu và Mã Nguồn (Traceability Matrix)

| Mục tiêu (Objectives) | Nhiệm vụ (Tasks) | Thư mục / Module phụ trách | Vai trò & Công nghệ chính |
| :--- | :--- | :--- | :--- |
| **Objective 1 & 2**<br>Khảo sát, thu thập & chuẩn hóa bộ dữ liệu | Task 1.1, 1.2<br>Task 2.1, 2.2 | `ai-pipeline/datasets/`<br>`shared/taxonomy/` | Chuẩn hóa danh mục sâu bệnh, script gán nhãn, convert YOLO/COCO, augment ảnh. |
| **Objective 3**<br>Huấn luyện & tối ưu mô hình Deep Learning | Task 3.1<br>Task 3.2 | `ai-pipeline/training/`<br>`ai-pipeline/evaluation/`<br>`ai-pipeline/export/` | So sánh benchmark CNN, YOLOv8/v11, EfficientNet; xuất TFLite/ONNX. |
| **Objective 4**<br>Hạ tầng IoT Edge & Ingestion Cloud | Task 4.1<br>Task 4.2 | `edge/`<br>`services/iot-gateway-service/` | Edge computing (Raspberry Pi/Jetson), đọc cảm biến, MQTT Ingestion pipeline, sync Cloud. |
| **Objective 5**<br>Phần mềm di động (Android / iOS) | Task 5.1<br>Task 5.2 | `clients/mobile/` | Flutter app: quét camera thời gian thực, offline/online AI inference, tra cứu sâu bệnh. |
| **Objective 6**<br>Hệ thống khuyến nghị thông minh | Task 6.1<br>Task 6.2 | `services/recommendation-service/`<br>`services/ai-service/` | Khuyến nghị giải pháp phòng trị theo thời tiết/bệnh; Phân loại phẩm cấp mít thu hoạch. |
| **Objective 7**<br>Nền tảng Web giám sát dịch tễ | Task 7.1<br>Task 7.2 | `clients/web/`<br>`services/core-api-service/` | Web Dashboard Next.js: Bản đồ dịch tễ GIS, quản lý nông hộ/vườn mít, cảnh báo thời gian thực. |

---

## 2. Cấu Trúc Tổng Thể Thư Mục

```text
Village/
├── object.md                         # Đặc tả mục tiêu nghiên cứu gốc
├── README.md                         # Tài liệu hướng dẫn tổng quan hệ thống
├── docker-compose.yml                # Khởi chạy toàn bộ hệ sinh thái Microservices
│
├── ai-pipeline/                      # [Obj 1, 2, 3] Nghiên cứu, huấn luyện & tối ưu mô hình AI
│   ├── datasets/                     # Xử lý, lọc và chuẩn hóa dữ liệu ảnh (Task 2.1, 2.2)
│   ├── training/                     # Scripts huấn luyện YOLO, EfficientNet, CNN (Task 3.1)
│   ├── evaluation/                   # So sánh benchmark mAP, latency, F1-score (Task 3.1)
│   └── export/                       # Tối ưu hóa sang TFLite, ONNX, TensorRT (Task 3.2)
│
├── edge/                             # [Obj 4] Mã nguồn thiết bị biên tại vườn mít
│   ├── edge_infer.py                 # Nhận diện tại chỗ (Edge AI) với camera (Task 4.2)
│   ├── sensor_collector.py           # Thu thập cảm biến môi trường (DHT22, Soil, etc.) (Task 4.1)
│   └── config.yaml                   # Cấu hình kết nối MQTT Gateway & chu kỳ gửi dữ liệu
│
├── services/                         # [Obj 4, 6, 7] Hệ thống Backend Microservices
│   ├── api-gateway/                  # Reverse Proxy định tuyến & xác thực tập trung
│   ├── ai-service/                   # FastAPI phục vụ AI Inference API trực tuyến (Task 3.2, 5.2, 6.2)
│   ├── iot-gateway-service/          # Ingestion dữ liệu MQTT từ vườn và cảm biến (Task 4.1, 7.2)
│   ├── recommendation-service/       # Khuyến nghị kỹ thuật canh tác, trị bệnh (Task 6.1)
│   └── core-api-service/             # Quản lý vườn mít, nông hộ, bản đồ dịch tễ (Task 7.1, 7.2)
│
├── clients/                          # [Obj 5, 7] Ứng dụng người dùng
│   ├── mobile/                       # Ứng dụng Flutter cho nông dân (Android/iOS) (Task 5.1, 5.2)
│   └── web/                          # Web Dashboard Next.js giám sát dịch tễ vùng (Task 7.1)
│
├── shared/                           # Định nghĩa dùng chung giữa các dịch vụ
│   ├── taxonomy/                     # Danh mục chuẩn hóa bệnh cây mít (Task 1.2)
│   └── schemas/                      # Định dạng bản tin dữ liệu chung (Pydantic / DTOs)
│
└── docs/                             # Tài liệu kỹ thuật chi tiết
    ├── ARCHITECTURE.md               # Kiến trúc hệ thống và luồng dữ liệu
    └── DISEASE_TAXONOMY.md           # Bảng phân loại sâu bệnh và triệu chứng lâm sàng
```

---

## 3. Kiến Trúc Giao Diện: Micro-Frontend & Hoạt Động Độc Lập

Hệ thống được thiết kế theo nguyên lý **Phân lập lỗi (Fault Isolation)** và **Giao diện đa phân hệ (Micro-Frontend)**:
1. **Hoạt động độc lập (Standalone Mode)**:
   - Mỗi module sở hữu giao diện Web UI riêng, phục vụ đúng nghiệp vụ chuyên sâu của nó và chạy trên cổng riêng biệt.
   - Khi phát triển hoặc thử nghiệm, bạn có thể chỉ khởi chạy 1 service duy nhất (ví dụ chỉ chạy AI Service hoặc IoT Gateway) và truy cập thẳng vào giao diện của service đó mà không cần bất kỳ service nào khác phải chạy.
2. **Kết hợp tập trung (Host Portal Mode)**:
   - Ứng dụng `clients/web` đóng vai trò là Host Hub, tập hợp tất cả các module UI vào một giao diện điều phối duy nhất.
   - Tự động giám sát trạng thái `health_check` thời gian thực của từng service. Nếu một service bị sự cố (ví dụ mạng chập chờn hoặc hết RAM), chỉ module đó hiển thị cảnh báo Offline; các module khác vẫn hoạt động 100% bình thường, không gây sập cả hệ thống.

### Danh Sách Giao Diện UI Độc Lập:
- 🌐 **Host Portal (Tổng hợp toàn hệ thống)**: `http://localhost:3000`
- 🔬 **Module AI UI (Chẩn đoán sâu bệnh & Phân loại trái)**: `http://localhost:8001/ui`
- 🌾 **Module Khuyến Nông UI (Tra cứu phác đồ điều trị IPM)**: `http://localhost:8002/ui`
- 🗺️ **Module Quản Lý Vườn UI (Bản đồ dịch tễ & Nông hộ)**: `http://localhost:8003/ui`
- 📡 **Module IoT Gateway UI (Giám sát cảm biến thời gian thực)**: `http://localhost:8004/ui`

---

## 4. Hướng Dẫn Khởi Chạy Nhanh (Quick Start)

### Yêu Cầu Tiên Quyết
- Docker & Docker Compose
- Python 3.10+ (cho AI Pipeline & Microservices)
- Node.js 18+ (cho Web Portal)
- Flutter SDK (cho Mobile App)

### Khởi chạy toàn bộ hệ thống bằng Docker
```bash
# Clone dự án & di chuyển vào thư mục gốc
cd Village

# Khởi tạo và chạy toàn bộ dịch vụ nền tảng (Database, Message Broker, APIs)
docker compose up -d --build
```

### Các cổng dịch vụ mặc định:
- **Web Dashboard**: `http://localhost:3000`
- **API Gateway**: `http://localhost:8000`
- **AI Inference Service Docs**: `http://localhost:8001/docs`
- **Recommendation Service Docs**: `http://localhost:8002/docs`
- **Core Orchard API Docs**: `http://localhost:8003/docs`
- **MQTT Broker**: `localhost:1883`

