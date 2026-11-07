"""
Bộ lắng nghe MQTT Broker từ các thiết bị biên vườn mít (Raspberry Pi/Jetson).
Phục vụ Task 4.1: Implementation of the data ingestion pipeline from IoT devices.
"""
import json
import asyncio
from typing import Dict, Any
import paho.mqtt.client as mqtt


class IoTIngestionSubscriber:
    def __init__(self, broker_host: str = "localhost", broker_port: int = 1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.latest_telemetry_cache: Dict[str, Any] = {}

    def on_connect(self, client, userdata, flags, rc):
        print(f"[MQTT Ingestion] Đã kết nối thành công tới Broker: {self.broker_host}:{self.broker_port} (rc={rc})")
        # Lắng nghe dữ liệu cảm biến và cảnh báo dịch bệnh từ các vườn mít
        self.client.subscribe("orchard/+/sensors")
        self.client.subscribe("orchard/+/alerts")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            orchard_id = topic.split("/")[1]
            print(f"[MQTT Ingestion] Nhận tin nhắn từ '{topic}': {payload}")

            if "sensors" in topic:
                self.latest_telemetry_cache[orchard_id] = payload
            elif "alerts" in topic:
                print(f"[ALERT] Phát hiện cảnh báo sâu bệnh tại vườn {orchard_id}: {payload}")
        except Exception as e:
            print(f"[MQTT Ingestion] Lỗi giải mã gói tin MQTT: {e}")

    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"[MQTT Ingestion Warning] Không thể kết nối MQTT Broker ({self.broker_host}:{self.broker_port}): {e}")

