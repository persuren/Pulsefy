import json
import matplotlib.pyplot as plt

# JSON dosyasını oku
def read_json(file_name, key_name):
    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data[key_name]["values"]  # İlgili anahtarın altındaki "values" verisini döndür

# Grafiği çizdir
def plot_ekg(data):
    plt.figure(figsize=(10, 4))  # Grafik boyutu
    plt.plot(data, color="black", linewidth=1)  # EKG çizgisi (siyah ince çizgi)
    plt.title("EKG Grafiği")
    plt.xlabel("Zaman")
    plt.ylabel("Gerilim (mV)")
    plt.grid(True, linestyle="--", alpha=0.6)  # Hafif grid çizgileri
    plt.show()

# Kullanım
file_name = "ekg_data12.json"  # Buraya dosya adını yaz
key_name = "data_05"  # JSON dosyasındaki anahtar adı
values = read_json(file_name, key_name)  # JSON'dan verileri oku
plot_ekg(values)  # Grafiği çizdir



#1,4,6,11,12 olanlar iyi
