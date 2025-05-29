from azure.eventhub import EventHubConsumerClient
import json
import csv
from datetime import datetime

count = 0
total_temp = 0.0
total_humidity = 0.0

CONNECTION_STR = "Endpoint=sb://iothub-ns-smartcityi-55647820-1682284e47.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=9o9yOoi9vBWd+AdTCRd4xqhXd5Jyj5BoqAIoTGXqTC4=;EntityPath=smartcityiot"
CONSUMER_GROUP = "$Default"
EVENTHUB_NAME = "smartcityiot"

csv_file = "iot_data.csv"

MAX_TEMPERATURE = 30.0  # derece
MAX_HUMIDITY = 60.0     # yüzde

# CSV dosyası başlıklarını ekle (dosya yoksa oluştur)
try:
    with open(csv_file, "x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "temperature", "humidity"])
except FileExistsError:
    pass  # Dosya zaten varsa geç


def on_event(partition_context, event):
    global count, total_temp, total_humidity

    try:
        data = event.body_as_str()
        print(f"Partition: {partition_context.partition_id} | Data: {data}")

        payload = json.loads(data)
        temperature = payload.get("temperature")
        humidity = payload.get("humidity")
        timestamp = event.enqueued_time.isoformat()

        # CSV dosyasına yaz
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, temperature, humidity])

        # Ortalama hesaplama
        total_temp += temperature
        total_humidity += humidity
        count += 1

        avg_temp = total_temp / count
        avg_humidity = total_humidity / count

        print(f"Ortalama Sıcaklık: {avg_temp:.2f} °C, Ortalama Nem: {avg_humidity:.2f} %")

        partition_context.update_checkpoint(event)

    except Exception as e:
        print(f"Hata oluştu: {e}")

def main():
    client = EventHubConsumerClient.from_connection_string(
        CONNECTION_STR,
        consumer_group=CONSUMER_GROUP,
        eventhub_name=EVENTHUB_NAME
    )
    print("Veri dinleniyor... Ctrl+C ile durdurabilirsiniz.")
    with client:
        client.receive(
            on_event=on_event,
            starting_position="-1"  # En baştan dinlemeye başla
        )

if __name__ == "__main__":
    main()