import json
import requests

# Firebase bilgileri
FIREBASE_HOST = "ecg-classification-0312-default-rtdb.firebaseio.com"
FIREBASE_AUTH = "AIzaSyB5cMhO7ZYEpRsHHNTNMxhghVwKZOS9yXQ"

# JSON dosya listesi
file_names = [
    "ekg_data12.json",
    
]
""""ekg_data1.json",
    "ekg_data4.json",
    "ekg_data6.json",
    "ekg_data11.json",
    "ekg_data12.json"""
# JSON dosyalarını Firebase'e yükleme fonksiyonu
def upload_json_to_firebase(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)

        # JSON'un ilk anahtarını bul (örneğin: "data_01")
        key_name = list(data.keys())[0]  # İlk anahtar (örneğin: data_01)

        # Firebase URL (key_name'e göre dinamik oluşturuluyor)
        firebase_url = f"https://{FIREBASE_HOST}/EKG_DATA/{key_name}.json?auth={FIREBASE_AUTH}"

        # Veriyi Firebase'e gönder
        response = requests.put(firebase_url, json=data[key_name])  # Sadece içeriği gönderiyoruz

        if response.status_code == 200:
            print(f"✅ {file_name} başarıyla Firebase'e yüklendi!")
        else:
            print(f"⚠️ {file_name} yükleme hatası! Kod: {response.status_code}, Mesaj: {response.text}")
    except Exception as e:
        print(f"❌ {file_name} yüklenirken hata oluştu: {e}")

# Tüm dosyaları sırayla Firebase'e yükleme
for file in file_names:
    upload_json_to_firebase(file)
