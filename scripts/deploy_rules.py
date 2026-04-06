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
    """QRadar-ın tələb etdiyi XML manifesti ilə birgə ZIP yaradır"""
    zip_buffer = io.BytesIO()
    
    # QRadar-ın 422 xətası verməməsi üçün lazım olan XML strukturu
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <content-extension>
        <name>GitHub-Detections</name>
        <description>Rules deployed from GitHub Actions</description>
        <version>1.0</version>
    </content-extension>
    """

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        # 1. Vacib olan XML faylını əlavə edirik
        zip_file.writestr("extension.xml", xml_content)
        
        # 2. Sənin JSON qaydalarını əlavə edirik
        for file_path in rule_files:
            zip_file.write(file_path, os.path.basename(file_path))
            
    return zip_buffer.getvalue()

def deploy_as_extension():
    url = f"https://{QRADAR_IP}/api/config/extension_management/extensions"
    
    rule_folder = "detections/"
    if not os.path.exists(rule_folder):
        print(f"Xəta: {rule_folder} qovluğu tapılmadı.")
        return

    rule_files = [os.path.join(rule_folder, f) for f in os.listdir(rule_folder) if f.endswith(".json")]
    
    if not rule_files:
        print("JSON faylı tapılmadı.")
        return

    print("Paket hazırlanır...")
    zip_data = create_extension_zip(rule_files)
    
    files = {'file': ('extension.zip', zip_data, 'application/zip')}
    
    try:
        # timeout-u bir az artıraq çünki extension emalı vaxt aparır
        response = requests.post(url, headers=HEADERS, files=files, verify=False, timeout=60)
        
        if response.status_code in [200, 201, 202]:
            print("✅ UĞURLU: QRadar paketi qəbul etdi və emal edir.")
        else:
            print(f"❌ XƏTA {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Bağlantı xətası: {str(e)}")

if __name__ == "__main__":
    deploy_as_extension()
