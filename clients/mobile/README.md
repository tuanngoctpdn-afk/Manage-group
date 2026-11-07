# Mobile Application - Jackfruit Pest Doctor (Flutter)

Ứng dụng di động dành cho bà con nông dân và kỹ thuật viên nông nghiệp.
Tương ứng trực tiếp với:
- **Task 5.1**: User-friendly UI/UX design supporting direct camera scanning on mobile phones.
- **Task 5.2**: Integration of the recognition model with real-time diagnostic feedback for users.

## Hướng dẫn cài đặt & chạy thử
```bash
cd clients/mobile
flutter pub get
flutter run
```
Mô hình TFLite được đặt tại `assets/models/jackfruit_model_int8.tflite` để hỗ trợ chẩn đoán Offline khi ra vườn không có sóng 4G.

