import requests
import json

# Firebase bilgileri
FIREBASE_HOST = "testnew-2fe14-default-rtdb.firebaseio.com"
FIREBASE_AUTH = "tTRV2j8JpaTYxgr5TzNxAiwYElQWygX7VIuvhcrv"

# Firebase URL'sini oluştur
url = f"https://{FIREBASE_HOST}/.json?auth={FIREBASE_AUTH}"

# Veriyi çek
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # JSON verisini dosyaya kaydet
    with open("firebase_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    print("Veri başarıyla kaydedildi: firebase_data.json")
else:
    print(f"Hata oluştu! HTTP {response.status_code}: {response.text}")
