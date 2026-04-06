import requests
import json
import os
import zipfile
import io

QRADAR_IP = os.getenv("QRADAR_IP")
API_TOKEN = os.getenv("QRADAR_API_KEY")

HEADERS = {
    "SEC": API_TOKEN,
    "Accept": "application/json"
}

def create_extension_zip(rule_files):
    """JSON fayllarını QRadar Extension formatında ZIP-ləyir"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_path in rule_files:
            # Faylın adını ZIP daxilində saxlayırıq
            zip_file.write(file_path, os.path.basename(file_path))
    return zip_buffer.getvalue()

def deploy_as_extension():
    url = f"https://{QRADAR_IP}/api/config/extension_management/extensions"
    
    # Detections qovluğundakı bütün JSON-ları tapırıq
    rule_folder = "detections/"
    rule_files = [os.path.join(rule_folder, f) for f in os.listdir(rule_folder) if f.endswith(".json")]
    
    if not rule_files:
        print("Heç bir qayda faylı tapılmadı.")
        return

    # ZIP paketini yaradırıq
    zip_data = create_extension_zip(rule_files)
    
    # QRadar-a POST (Multipart form-data ilə)
    files = {'file': ('extension.zip', zip_data, 'application/zip')}
    
    response = requests.post(url, headers=HEADERS, files=files, verify=False)
    
    if response.status_code in [200, 201, 202]:
        print("✅ UĞURLU: Qaydalar Extension kimi yükləndi. QRadar indi onları emal edir.")
        print(f"Status: {response.json().get('status')}")
    else:
        print(f"❌ XƏTA: {response.status_code} - {response.text}")

if __name__ == "__main__":
    deploy_as_extension()
