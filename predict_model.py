import os
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from tensorflow.keras.models import load_model


# Firebase bilgileri
FIREBASE_HOST = "ecg-classification-0312-default-rtdb.firebaseio.com"
FIREBASE_AUTH = "AIzaSyB5cMhO7ZYEpRsHHNTNMxhghVwKZOS9yXQ"

# Firebase URL'sini oluştur
FIREBASE_URL = f"https://{FIREBASE_HOST}/EKG_DATA.json?auth={FIREBASE_AUTH}"

# Modeli yükleme fonksiyonu
def load_trained_model(model_path="ekg_5class_model.h5"):
    if os.path.exists(model_path):
        print(f"Kaydedilmiş model bulundu. Yükleniyor: {model_path}")
        return load_model(model_path)
    else:
        print("Kaydedilmiş model bulunamadı!")
        return None
def get_latest_ecg_values():

    response = requests.get(FIREBASE_URL)
    
    if response.status_code != 200:
        raise ValueError(f"Veri alınamadı, HTTP Kodu: {response.status_code}")

    data = response.json()
    
    if not data:
        raise ValueError("EKG_DATA altında herhangi bir veri bulunamadı.")


    # Anahtarları filtrele (sayıyla bitenleri al)
    valid_keys = [k for k in data.keys() if k.startswith("data_") and k.split('_')[-1].isdigit()]
    
    if not valid_keys:
        raise ValueError("Geçerli data_X formatında veri bulunamadı.")

    # En son eklenen data_X'i bul
    latest_key = max(valid_keys, key=lambda x: int(x.split('_')[-1]))

    # "values" olup olmadığını kontrol et
    latest_key= "data_05"
    latest_values = data[latest_key].get('values', None)
    print("*******************************")
    print(latest_key)
    print("*******************************")
    if not latest_values:
        raise ValueError(f"'{latest_key}' içinde 'values' bulunamadı veya boş.")

    return np.array(latest_values)

# Sinyali normalize etme
def normalize_signal(signal):
    return (signal - np.min(signal)) / (np.max(signal) - np.min(signal))

# R-R İnterval hesaplama
def calculate_rr_intervals(signal, sampling_rate):
    peaks, _ = find_peaks(signal, height=0.5, distance=sampling_rate * 0.5)
    rr_intervals = np.diff(peaks) / sampling_rate
    if len(rr_intervals) < 10:
        mean_interval = np.mean(rr_intervals)
        rr_intervals = np.append(rr_intervals, mean_interval)
    return peaks, rr_intervals

# EKG sinyalini ve R dalgalarını görselleştirme
def plot_signal_with_peaks(signal, peaks):
    plt.figure(figsize=(10, 6))
    plt.plot(signal, label='EKG Sinyali', color='blue')
    plt.scatter(peaks, signal[peaks], color='red', label='R Dalgaları')
    plt.title('EKG Sinyali ve R Dalgaları')
    plt.xlabel('Örnek (Sample)')
    plt.ylabel('Genlik')
    plt.legend()
    plt.show()

# Modeli yükle
model_path = "ekg_model.h5"
model = load_trained_model(model_path)

# Tahmin yapmak için JSON'dan veri oku
ekg_signal = get_latest_ecg_values()
normalized_signal = normalize_signal(ekg_signal)
sampling_rate = 390.32
peaks, rr_intervals = calculate_rr_intervals(normalized_signal, sampling_rate)

# Modelin tahmin yapması
threshold = 0.20
rr_intervals_array = np.array(rr_intervals).reshape(1, -1)
prediction = model.predict(rr_intervals_array)
predicted_class = (prediction > threshold).astype(int)

# Sonuçları ekrana yazdırma
print("Tahmin sonucu:", prediction)
print("Tahmin edilen sınıf:", predicted_class[0])
print("R-R İntervaller (saniye):", rr_intervals)
print("Ortalama R-R Interval (saniye):", np.mean(rr_intervals))
print("Kalp Atış Hızı (BPM):", 60 / np.mean(rr_intervals))

# Sinyali çizdirme
plot_signal_with_peaks(normalized_signal, peaks)
