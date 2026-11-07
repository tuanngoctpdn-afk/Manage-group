"""
Mã nguồn suy luận thời gian thực trên thiết bị biên (Edge AI - Jetson Nano / Raspberry Pi 4).
Phục vụ Task 4.2: Real-time data analysis on edge devices and synchronization with the cloud platform.
"""
import time
import json
import paho.mqtt.client as mqtt


class EdgeAIAnomalyDetector:
    def __init__(self, device_id: str = "edge-camera-01", orchard_id: str = "TG-001", mqtt_host: str = "localhost"):
        self.device_id = device_id
        self.orchard_id = orchard_id
        self.mqtt_host = mqtt_host
        self.client = mqtt.Client()

    def initialize(self):
        print(f"[Edge AI] Khởi động mô hình TFLite/TensorRT trên thiết bị biên ({self.device_id})...")
        try:
            self.client.connect(self.mqtt_host, 1883, 60)
        except Exception as e:
            print(f"[Edge AI] Không kết nối được MQTT Broker: {e}")

    def run_surveillance_loop(self):
        """
        Vòng lặp giám sát camera:
        1. Capture frame từ camera RTSP/USB
        2. Chạy TFLite model cục bộ với độ trễ thấp (<30ms)
        3. Nếu phát hiện sâu đục quả hoặc nấm thối -> Gửi gói tin Alert lên Cloud ngay lập tức
        """
        print(f"[Edge AI] Bắt đầu quét camera thời gian thực tại vườn {self.orchard_id}...")
        
        # Mô phỏng phát hiện bất thường sau 5 giây
        time.sleep(3)
        alert_payload = {
            "device_id": self.device_id,
            "orchard_id": self.orchard_id,
            "timestamp": time.time(),
            "detected_disease": "JF_FRUIT_BORER",
            "confidence": 0.912,
            "urgency": "HIGH",
            "message": "Phát hiện sâu đục trái mít tại cây số 14 - Lô B"
        }

        alert_topic = f"orchard/{self.orchard_id}/alerts"
        self.client.publish(alert_topic, json.dumps(alert_payload))
        print(f"[Edge AI ALERT] Đồng bộ cảnh báo lên Cloud Topic '{alert_topic}': {alert_payload}")


if __name__ == "__main__":
    detector = EdgeAIAnomalyDetector()
    detector.initialize()
    detector.run_surveillance_loop()

