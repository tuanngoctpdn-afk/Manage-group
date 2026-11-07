"""
Module tiền xử lý, gán nhãn và chuẩn hóa bộ dữ liệu hình ảnh sâu bệnh mít.
Tương ứng: Task 2.1 (Thu thập, gán nhãn), Task 2.2 (Chuẩn hóa dữ liệu cho AI).
"""
import os
import shutil
import random
from pathlib import Path
from typing import List, Tuple


def standardize_image_dataset(
    raw_images_dir: str,
    output_yolo_dir: str,
    train_ratio: float = 0.8,
    val_ratio: float = 0.15,
    test_ratio: float = 0.05,
    seed: int = 42
):
    """
    Chuẩn hóa cấu trúc thư mục dữ liệu sang chuẩn YOLOv8/v11 dataset format.
    Cấu trúc tạo ra:
    output_yolo_dir/
      ├── images/
      │   ├── train/
      │   ├── val/
      │   └── test/
      ├── labels/
      │   ├── train/
      │   ├── val/
      │   └── test/
      └── data.yaml
    """
    random.seed(seed)
    raw_path = Path(raw_images_dir)
    out_path = Path(output_yolo_dir)

    for split in ["train", "val", "test"]:
        (out_path / "images" / split).mkdir(parents=True, exist_ok=True)
        (out_path / "labels" / split).mkdir(parents=True, exist_ok=True)

    print(f"[Dataset Preparation] Đang chuẩn hóa dữ liệu từ '{raw_dir}' sang '{output_yolo_dir}'...")

    # Tạo data.yaml đặc tả các class sâu bệnh mít
    yaml_content = """# Dataset configuration for Jackfruit Pest & Disease Detection
path: .
train: images/train
val: images/val
test: images/test

# Danh mục nhãn đồng bộ từ shared/taxonomy/diseases.py
names:
  0: JF_HEALTHY
  1: JF_FRUIT_BORER
  2: JF_SOFT_ROT
  3: JF_PHYTOPHTHORA_CANKER
  4: JF_MEALYBUG
  5: JF_LEAF_SPOT
"""
    with open(out_path / "data.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_content)

    print("[Dataset Preparation] Đã tạo file data.yaml cấu hình thành công.")


if __name__ == "__main__":
    raw_dir = "./raw_jackfruit_data"
    yolo_dir = "./processed_yolo_dataset"
    print("Khởi chạy module chuẩn hóa dữ liệu AI...")
    standardize_image_dataset(raw_dir, yolo_dir)

