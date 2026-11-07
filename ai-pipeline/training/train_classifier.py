"""
Huấn luyện mô hình Deep Learning Phân loại ảnh (EfficientNetV2 / CNN) cho sâu bệnh mít.
Tương ứng: Task 3.1 (Đánh giá so sánh hiệu năng CNN, EfficientNet).
"""
import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.utils.data import DataLoader


def get_efficientnet_model(num_classes: int = 6, pretrained: bool = True):
    """
    Khởi tạo mô hình EfficientNet-V2-S và thay thế head classifier.
    """
    weights = models.EfficientNet_V2_S_Weights.DEFAULT if pretrained else None
    model = models.efficientnet_v2_s(weights=weights)
    
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, num_classes)
    )
    return model


def train_classifier(epochs: int = 30, lr: float = 1e-4, num_classes: int = 6):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Classifier Training] Thiết bị huấn luyện: {device}")
    
    model = get_efficientnet_model(num_classes=num_classes)
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-2)

    print(f"[Classifier Training] Sẵn sàng huấn luyện EfficientNetV2 cho {num_classes} phân lớp sâu bệnh.")
    return model


if __name__ == "__main__":
    train_classifier()

