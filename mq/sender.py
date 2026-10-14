# import time: modul bawaan Python untuk mengatur jeda waktu (delay)
import os
import time
# import json: untuk mengubah format data dictionary Python menjadi string JSON
import json
# import random: untuk menghasilkan angka acak (data sensor dummy)
import random
# import paho.mqtt.client: library utama untuk menggunakan protokol MQTT
import paho.mqtt.client as mqtt

# Konstanta untuk konfigurasi MQTT
# Menggunakan public broker gratis untuk testing. Nanti bisa diganti dengan IP lokal/container jika diperlukan.
BROKER_ADDRESS = os.environ.get("BROKER_ADDRESS", "test.mosquitto.org")
BROKER_PORT = 1883
# Topik yang akan digunakan untuk mengirim pesan. Harus spesifik agar tidak bentrok dengan pengguna public broker lain.
TOPIC = os.environ.get("TOPIC", "tugas4/sensor/kelompok_kamu")

def main():
    print("=" * 50)
    print("      PROGRAM SENDER (MQTT PUBLISHER)      ")
    print("=" * 50)
    
    # Inisialisasi MQTT Client
    client = mqtt.Client("Sensor_Sender")
    
    try:
        # Menghubungkan client ke broker MQTT
        print(f"[*] Menghubungkan ke broker {BROKER_ADDRESS}...")
        client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
        
        # loop_start() menjalankan thread terpisah untuk menangani trafik jaringan MQTT di background
        client.loop_start()
        print("[V] Berhasil terhubung! Mulai mengirim data sensor...\n")
        
        # Loop utama untuk mengirim data secara periodik
        while True:
            # Membuat data sensor dummy menggunakan angka acak
            # Suhu antara 25.0 hingga 35.0 derajat Celcius
            suhu = round(random.uniform(25.0, 35.0), 2)
            # Kelembapan antara 40.0 hingga 80.0 persen
            kelembapan = round(random.uniform(40.0, 80.0), 2)
            
            # Membungkus data ke dalam dictionary
            data_sensor = {
                "sensor_id": "sensor_ruangan_01",
                "suhu_celcius": suhu,
                "kelembapan_persen": kelembapan
            }
            
            # Mengubah dictionary menjadi format string JSON (payload)
            payload = json.dumps(data_sensor)
            
            # Mengirimkan (publish) pesan ke broker pada topik yang sudah ditentukan
            client.publish(TOPIC, payload)
            
            # Menampilkan log di layar sender
            print(f"[+] Data terkirim pada topik '{TOPIC}':")
            print(f"    -> {payload}")
            print(f"[i] Menunggu 60 detik untuk pengiriman berikutnya...\n")
            
            # Jeda 60 detik (1 menit) sesuai permintaan soal
            time.sleep(60)

    except KeyboardInterrupt:
        # Menangani saat user menekan Ctrl+C untuk keluar dari program
        print("\n[*] Program Sender dihentikan oleh pengguna.")
    finally:
        # Menghentikan background thread dan memutuskan koneksi dari broker dengan rapi
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()