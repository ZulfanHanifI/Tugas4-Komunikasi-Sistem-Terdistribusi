import os
# import paho.mqtt.client: library utama untuk menggunakan protokol MQTT
import paho.mqtt.client as mqtt

# Konstanta harus sama dengan yang ada di program Sender
BROKER_ADDRESS = os.environ.get("BROKER_ADDRESS", "test.mosquitto.org")
BROKER_PORT = 1883
TOPIC = os.environ.get("TOPIC", "tugas4/sensor/kelompok_kamu")

# Fungsi callback yang akan otomatis dipanggil setiap kali program berhasil terhubung ke broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[V] Berhasil terhubung ke MQTT Broker!")
        # Melakukan subscribe (berlangganan) ke topik setelah berhasil connect
        client.subscribe(TOPIC)
        print(f"[*] Berlangganan (subscribe) pada topik: {TOPIC}")
        print("[i] Menunggu data masuk... Tekan Ctrl+C untuk keluar.\n")
    else:
        print(f"[X] Gagal terhubung, kode error: {rc}")

# Fungsi callback yang akan otomatis dipanggil setiap kali ada pesan baru masuk dari topik yang di-subscribe
def on_message(client, userdata, msg):
    print("=" * 50)
    print("            [DATA BARU DITERIMA]            ")
    print("=" * 50)
    print(f"Topik       : {msg.topic}")
    # Pesan MQTT dikirim dalam bentuk bytes, jadi harus di-decode menjadi string (utf-8)
    print(f"Isi Pesan   : {msg.payload.decode('utf-8')}")
    print("=" * 50 + "\n")

def main():
    print("=" * 50)
    print("     PROGRAM RECEIVER (MQTT SUBSCRIBER)    ")
    print("=" * 50)
    
    # Inisialisasi MQTT Client
    client = mqtt.Client("Sensor_Receiver")
    
    # Memasang fungsi callback yang sudah dibuat di atas ke event milik paho-mqtt
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        print(f"[*] Mencoba terhubung ke {BROKER_ADDRESS}...")
        # Menghubungkan client ke broker MQTT
        client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
        
        # loop_forever() adalah fungsi blocking yang menahan program agar terus berjalan 
        # dan memproses semua lalu lintas jaringan (termasuk memanggil on_message saat ada pesan)
        client.loop_forever()
        
    except KeyboardInterrupt:
        # Menangani saat user menekan Ctrl+C
        print("\n[*] Program Receiver dihentikan oleh pengguna.")
        # Memutuskan koneksi secara rapi sebelum keluar
        client.disconnect()

if __name__ == "__main__":
    main()