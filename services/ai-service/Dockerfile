FROM python:3.10-slim

WORKDIR /workspace

# Cài đặt các thư viện hệ thống cần thiết cho OpenCV/Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY services/ai-service/requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY shared /workspace/shared
COPY services/ai-service /workspace/services/ai-service

ENV PYTHONPATH=/workspace

EXPOSE 8001

CMD ["uvicorn", "services.ai-service.app.main:app", "--host", "0.0.0.0", "--port", "8001"]

