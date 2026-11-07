"""
Huấn luyện mô hình Deep Learning Object Detection (YOLOv8 / YOLOv11) cho sâu bệnh mít.
Tương ứng: Task 3.1 & Task 3.2.
"""
import os
from pathlib import Path


def train_jackfruit_detector(
    data_yaml_path: str = "ai-pipeline/datasets/data.yaml",
    model_type: str = "yolov8m.pt",
    epochs: int = 100,
    imgsz: int = 640,
    batch_size: int = 16,
    device: str = "0",  # GPU 0 hoặc 'cpu'
    project_name: str = "jackfruit_pest_detection"
):
    """
    Huấn luyện mô hình Object Detection để phát hiện vị trí sâu bệnh trên mít.
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        print("[Warning] Cần cài đặt ultralytics: pip install ultralytics")
        return

    print(f"=== Bắt đầu huấn luyện {model_type} ===")
    print(f"Cấu hình: Epochs={epochs}, ImageSize={imgsz}, Batch={batch_size}")

    model = YOLO(model_type)

    results = model.train(
        data=data_yaml_path,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch_size,
        device=device,
        project=project_name,
        name="jackfruit_yolo_run",
        save=True,
        augment=True,
        plots=True
    )
    print(f"Huấn luyện hoàn tất! Trọng số lưu tại: {results.save_dir}")
    return results


if __name__ == "__main__":
    train_jackfruit_detector()

