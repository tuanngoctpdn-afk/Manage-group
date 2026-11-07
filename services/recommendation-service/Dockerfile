FROM python:3.10-slim

WORKDIR /workspace

COPY services/recommendation-service/requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY shared /workspace/shared
COPY services/recommendation-service /workspace/services/recommendation-service

ENV PYTHONPATH=/workspace

EXPOSE 8002

CMD ["uvicorn", "services.recommendation-service.app.main:app", "--host", "0.0.0.0", "--port", "8002"]

