import requests
import json
import os
import zipfile
import io

# GitHub Secrets-dən sənin təyin etdiyin adlarla oxuyuruq
QRADAR_IP = os.getenv("QRADAR_IP")
API_TOKEN = os.getenv("QRADAR_API_KEY") # Secret adına uyğun dəyişdirildi

HEADERS = {
    "SEC": API_TOKEN,
    "Accept": "application/json"
}

def create_extension_zip(rule_files):
    """JSON fayllarını QRadar Extension formatında ZIP-ləyir"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_path in rule_files:
            zip_file.write(file_path, os.path.basename(file_path))
    return zip_buffer.getvalue()

def deploy_as_extension():
    # Extension management endpoint-i
    url = f"https://{QRADAR_IP}/api/config/extension_management/extensions"
    
    rule_folder = "detections/"
    if not os.path.exists(rule_folder):
        print(f"Xəta: {rule_folder} qovluğu tapılmadı.")
        return

    rule_files = [os.path.join(rule_folder, f) for f in os.listdir(rule_folder) if f.endswith(".json")]
    
    if not rule_files:
        print("Heç bir qayda (.json) faylı tapılmadı.")
        return

    print(f"Paketlənməyə hazır fayllar: {rule_files}")
    zip_data = create_extension_zip(rule_files)
    
    files = {'file': ('extension.zip', zip_data, 'application/zip')}
    
    # QRadar-a göndəririk
    try:
        response = requests.post(url, headers=HEADERS, files=files, verify=False, timeout=30)
        
        if response.status_code in [200, 201, 202]:
            print("✅ UĞURLU: Qaydalar QRadar-a Extension olaraq yükləndi.")
            print(f"Cavab: {response.text}")
        elif response.status_code == 401:
            print("❌ XƏTA 401: Unauthorized. API Key yanlışdır və ya Token-in 'Admin' yetkisi yoxdur.")
        else:
            print(f"❌ XƏTA {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Bağlantı xətası: {str(e)}")

if __name__ == "__main__":
    deploy_as_extension()
