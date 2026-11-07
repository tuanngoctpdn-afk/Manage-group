FROM python:3.10-slim

WORKDIR /workspace

COPY services/core-api-service/requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY shared /workspace/shared
COPY services/core-api-service /workspace/services/core-api-service

ENV PYTHONPATH=/workspace

EXPOSE 8003

CMD ["uvicorn", "services.core-api-service.app.main:app", "--host", "0.0.0.0", "--port", "8003"]

