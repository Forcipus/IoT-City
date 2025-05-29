import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

csv_file = "iot_data.csv"
TEMP_THRESHOLD = 30
HUMIDITY_THRESHOLD = 65

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

temp_text = fig.text(0.85, 0.75, "", fontsize=12, color='red', ha='left')

def animate(i):
    timestamps = []
    temperatures = []
    humidities = []

    try:
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            rows = rows[-20:]
            for row in rows:
                try:
                    time_str = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
                except:
                    time_str = row["timestamp"]
                timestamps.append(time_str)
                temperatures.append(float(row["temperature"]))
                humidities.append(float(row["humidity"]))
    except Exception as e:
        ax1.cla()
        ax2.cla()
        ax1.text(0.5, 0.5, "Veri bulunamadı veya okunamadı", ha='center', va='center')
        ax2.text(0.5, 0.5, "Veri bulunamadı veya okunamadı", ha='center', va='center')
        return

    ax1.cla()
    ax2.cla()

    if timestamps:
        # Ortalama değerleri hesapla
        avg_temp = sum(temperatures) / len(temperatures)  # Ortalama sıcaklık
        avg_humidity = sum(humidities) / len(humidities)  # Ortalama nem

        # Sıcaklık grafiği
        ax1.plot(timestamps, temperatures, color='red')
        ax1.set_title("Sıcaklık (°C)")
        ax1.set_ylabel("°C")
        ax1.set_ylim(0, 50)
        ax1.set_xticks([])

        # Ortalama sıcaklık çizgisi (turuncu, kesikli)
        ax1.axhline(avg_temp, color='orange', linestyle='--', label=f"Ortalama: {avg_temp:.1f} °C")
        ax1.legend(loc='upper left', fontsize=8)

        if temperatures[-1] > TEMP_THRESHOLD:
            ax1.axhline(TEMP_THRESHOLD, color='darkred', linestyle='--')
            ax1.text(0.5, 0.9, f"⚠️ Yüksek Sıcaklık: {temperatures[-1]:.1f} °C",
                     transform=ax1.transAxes, ha='center', fontsize=9, color='darkred')

        # Nem grafiği
        ax2.plot(timestamps, humidities, color='blue')
        ax2.set_title("Nem (%)")
        ax2.set_ylabel("%")
        ax2.set_xlabel("Zaman (HH:MM)")
        ax2.set_ylim(0, 100)

        # Ortalama nem çizgisi (turkuaz, kesikli)
        ax2.axhline(avg_humidity, color='deepskyblue', linestyle='--', label=f"Ortalama: {avg_humidity:.1f} %")
        ax2.legend(loc='upper left', fontsize=8)

        # Çok kalabalık olmaması için 5 aralıkla göster
        step = max(1, len(timestamps)//5)
        ax2.set_xticks(timestamps[::step])
        ax2.set_xticklabels(timestamps[::step], rotation=45, ha='right')

        if humidities[-1] > HUMIDITY_THRESHOLD:
            ax2.axhline(HUMIDITY_THRESHOLD, color='darkblue', linestyle='--')
            ax2.text(0.5, 0.9, f"⚠️ Yüksek Nem: {humidities[-1]:.1f} %",
                     transform=ax2.transAxes, ha='center', fontsize=9, color='darkblue')

        # Sağda sıcaklığı figür text ile göster
        temp_text.set_text(f"Son Sıcaklık: {temperatures[-1]:.1f} °C")

        # Nem değerini nem grafiğinin sağ kenarına yaz
        ax2.text(1.02, 0.5, f"Son Nem: {humidities[-1]:.1f} %",
                 transform=ax2.transAxes, fontsize=12, color='blue',
                 verticalalignment='center', ha='left')

    else:
        ax1.text(0.5, 0.5, "Veri yok", ha='center', va='center')
        ax2.text(0.5, 0.5, "Veri yok", ha='center', va='center')
        temp_text.set_text("")

    plt.subplots_adjust(left=0.1, right=0.82, top=0.95, bottom=0.15, hspace=0.4)

ani = FuncAnimation(fig, animate, interval=2000)
plt.show()



