import requests
import time
import concurrent.futures
import os

def temizle():
    # Terminal ekranını temizlemek için (Windows için cls, Mac/Linux için clear)
    os.system('cls' if os.name == 'nt' else 'clear')

def send_request(url, request_id):
    try:
        # Önbelleği (cache) atlatmak için her isteğe benzersiz parametre ekliyoruz
        url_with_cache_buster = f"{url}?test={request_id}"
        
        start_time = time.time()
        response = requests.get(url_with_cache_buster, timeout=5)
        duration = time.time() - start_time
        
        print(f"[İstek #{request_id:02d}] Durum Kodu: {response.status_code} | Süre: {duration:.2f}s")
        
        if response.status_code == 429:
            print(f"⚠️  [UYARI] Sunucu Rate Limit uyguladı! (429 Too Many Requests)")
        elif response.status_code == 403:
            print(f"🛑 [ENGELLEME] Sunucu veya Firewall seni engelledi! (403 Forbidden)")
            
    except requests.exceptions.Timeout:
        print(f"[İstek #{request_id:02d}] ❌ Zaman aşımı! Korumaya takılmış olabilir.")
    except requests.exceptions.RequestException as e:
        print(f"[İstek #{request_id:02d}] ❌ Hata: {e}")

def main():
    temizle()
    print("="*50)
    print("      DDoS / RATE LIMIT KORUMA TEST MENÜSÜ      ")
    print("="*50)
    
    # 1. URL Sorusu
    target_url = input("🔗 Test edilecek URL adresini gir kanka (Örn: https://siten.com): ").strip()
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url  # Eğer protokol yazmadıysa otomatik ekler

    # 2. Toplam İstek Sayısı Sorusu
    try:
        total_requests = input("📊 Kaç adet istek gönderilsin? (Varsayılan 50): ").strip()
        total_requests = int(total_requests) if total_requests else 50
    except ValueError:
        print("Geçersiz sayı girdin kanka, 50 adet olarak ayarlandı.")
        total_requests = 50

    # 3. Eşzamanlılık (Hız) Sorusu
    try:
        max_workers = input("⚡ Aynı anda kaç istek gitsin? [Hız Ayarı] (Varsayılan 5): ").strip()
        max_workers = int(max_workers) if max_workers else 5
    except ValueError:
        print("Geçersiz sayı girdin kanka, hız 5 olarak ayarlandı.")
        max_workers = 5

    print("\n" + "="*50)
    print(f"🚀 Test başlatılıyor...")
    print(f"🎯 Hedef: {target_url}")
    print(f"📦 Toplam İstek: {total_requests} | ⚡ Hız Katsayısı: {max_workers}")
    print("="*50 + "\n")

    start_total_time = time.time()
    
    # İstekleri eşzamanlı gönderme işlemi
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Fonksiyona sabit URL parametresini göndermek için lambda veya list comprehension kullanıyoruz
        futures = [executor.submit(send_request, target_url, i) for i in range(1, total_requests + 1)]
        concurrent.futures.wait(futures)
        
    end_total_time = time.time()
    print("\n" + "="*50)
    print(f"✅ Test tamamlandı!")
    print(f"⏱️  Toplam geçen süre: {end_total_time - start_total_time:.2f} saniye.")
    print("="*50)

if __name__ == "__main__":
    main()
