"""
Tối ưu hóa và đóng gói mô hình AI sang ONNX và TensorFlow Lite (TFLite)
cho thiết bị di động (Task 5.2) và thiết bị biên IoT (Task 4.2).
"""
import os
from pathlib import Path


def export_jackfruit_model(
    model_weight_path: str = "best_jackfruit_yolo.pt",
    imgsz: int = 640
):
    """
    Xuất mô hình sang:
    1. ONNX (FP16): Tối ưu cho Cloud Server & Jetson Edge
    2. TFLite (INT8/FP16): Tối ưu cho Mobile Android/iOS và Raspberry Pi
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        print("[Warning] Vui lòng cài đặt ultralytics để export: pip install ultralytics")
        return

    print(f"[Model Export] Đang nạp mô hình từ {model_weight_path}...")
    model = YOLO(model_weight_path)

    # 1. Export ONNX
    print("[Model Export] Đang xuất mô hình ONNX...")
    onnx_path = model.export(format="onnx", imgsz=imgsz, dynamic=False, simplify=True)
    print(f"-> ONNX lưu tại: {onnx_path}")

    # 2. Export TFLite
    print("[Model Export] Đang xuất mô hình TFLite (INT8/FP16) cho Mobile & Edge...")
    tflite_path = model.export(format="tflite", imgsz=imgsz, int8=False)
    print(f"-> TFLite lưu tại: {tflite_path}")

    return {"onnx": onnx_path, "tflite": tflite_path}


if __name__ == "__main__":
    export_jackfruit_model()

