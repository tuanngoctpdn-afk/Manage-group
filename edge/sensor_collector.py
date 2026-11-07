"""
Mã nguồn thu thập dữ liệu cảm biến môi trường tại vườn mít (IoT Node).
Phục vụ Task 4.1: Implementation of the data ingestion pipeline from IoT devices.
"""
import time
import json
import random
import yaml
import paho.mqtt.client as mqtt


def load_config(config_file: str = "edge/config.yaml"):
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return {
            "device_id": "edge-node-01",
            "orchard_id": "TG-001",
            "mqtt_broker": "localhost",
            "mqtt_port": 1883,
            "sensor_interval_sec": 10
        }


def read_physical_sensors():
    """
    Đọc dữ liệu từ cảm biến thực tế (ví dụ: DHT22, Cảm biến độ ẩm đất RS485 Modbus).
    Ở môi trường dev, mô phỏng giá trị môi trường vườn mít nhiệt đới.
    """
    return {
        "temperature_celsius": round(random.uniform(26.0, 34.0), 2),
        "air_humidity_percent": round(random.uniform(70.0, 92.0), 2),
        "soil_moisture_percent": round(random.uniform(55.0, 80.0), 2),
        "rainfall_detected": random.choice([False, False, True])
    }


def main():
    config = load_config()
    client = mqtt.Client()
    
    print(f"[Sensor Collector] Đang kết nối tới MQTT Broker: {config['mqtt_broker']}:{config['mqtt_port']}...")
    try:
        client.connect(config["mqtt_broker"], config["mqtt_port"], 60)
    except Exception as e:
        print(f"[Sensor Collector Error] Không thể kết nối MQTT: {e}")
        return

    topic = f"orchard/{config['orchard_id']}/sensors"
    print(f"[Sensor Collector] Bắt đầu truyền dữ liệu vào Topic: {topic}")

    while True:
        sensor_data = read_physical_sensors()
        payload = {
            "device_id": config["device_id"],
            "orchard_id": config["orchard_id"],
            "timestamp": time.time(),
            **sensor_data
        }
        client.publish(topic, json.dumps(payload))
        print(f"-> Đã gửi telemetry: Nhiệt độ={sensor_data['temperature_celsius']}°C, Ẩm={sensor_data['air_humidity_percent']}%")
        time.sleep(config["sensor_interval_sec"])


if __name__ == "__main__":
    main()

