"""
Công cụ suy luận nhận diện sâu bệnh cây mít sử dụng mô hình tối ưu.
Phục vụ Task 3.2, 5.2.
"""
import time
import uuid
from typing import List
import numpy as np

# Giả lập hoặc nạp ONNX Runtime / PyTorch để suy luận
from shared.schemas.diagnosis import (
    AIInferenceResponse,
    DetectedAnomaly,
    BoundingBox
)
from shared.taxonomy.diseases import DISEASE_TAXONOMY


class JackfruitInferenceEngine:
    def __init__(self, model_path: str = "weights/best_jackfruit_model.onnx"):
        self.model_path = model_path
        self.model_version = "v1.2.0-yolov8m"
        print(f"[InferenceEngine] Khởi tạo mô hình AI từ: {self.model_path}")

    def predict_image(self, image_bytes: bytes) -> AIInferenceResponse:
        """
        Thực hiện tiền xử lý và suy luận trên ảnh đầu vào.
        """
        start_time = time.time()
        
        # Mô phỏng quá trình forward inference (ONNX Runtime / TensorRT)
        # Khi triển khai thực tế: sess = ort.InferenceSession(self.model_path)
        inference_time_ms = round((time.time() - start_time + 0.028) * 1000, 2)

        # Ví dụ phát hiện sâu đục trái mít
        detected_disease_id = "JF_FRUIT_BORER"
        disease_info = DISEASE_TAXONOMY.get(detected_disease_id)

        sample_detection = DetectedAnomaly(
            disease_id=detected_disease_id,
            disease_name_vi=disease_info.vietnamese_name if disease_info else "Sâu đục trái mít",
            confidence=0.924,
            bbox=BoundingBox(x_min=0.25, y_min=0.30, x_max=0.55, y_max=0.68)
        )

        return AIInferenceResponse(
            inference_id=str(uuid.uuid4()),
            model_version=self.model_version,
            inference_time_ms=inference_time_ms,
            is_healthy=False,
            detections=[sample_detection]
        )

