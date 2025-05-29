import time
import random
from azure.iot.device import IoTHubDeviceClient, Message
import os

# Azure IoT Hub bağlantı dizesi
conn_str = "HostName=smartcityiot.azure-devices.net;DeviceId=device001;SharedAccessKey=7Fd6VC4uyOlCSHDpn90JE+vGb68D+rgCt1sfeLAMnjQ="

# Cihaz istemcisini oluştur
device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

# Azure IoT Hub’a bağlan
device_client.connect()

try:
    while True:
        # Sahte sıcaklık ve nem verisi üret
        temperature = round(random.uniform(20.0, 35.0), 2)
        humidity = round(random.uniform(30.0, 70.0), 2)

        message = Message(f'{{"temperature": {temperature}, "humidity": {humidity}}}')
        print(f"Gönderiliyor: {message}")

        # Mesajı gönder
        device_client.send_message(message)

        # 5 saniye bekle
        time.sleep(5)

except KeyboardInterrupt:
    print("Simülasyon durduruldu")

finally:
    device_client.disconnect()