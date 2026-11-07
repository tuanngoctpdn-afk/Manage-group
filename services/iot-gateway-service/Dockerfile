FROM python:3.10-slim

WORKDIR /workspace

COPY services/iot-gateway-service/requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY shared /workspace/shared
COPY services/iot-gateway-service /workspace/services/iot-gateway-service

ENV PYTHONPATH=/workspace

EXPOSE 8004

CMD ["uvicorn", "services.iot-gateway-service.app.main:app", "--host", "0.0.0.0", "--port", "8004"]

