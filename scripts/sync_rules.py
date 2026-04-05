import os
import requests
import json
import urllib3

# Təhlükəsizlik xəbərdarlıqlarını gizlət
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_IP = os.getenv('QRADAR_IP')
API_TOKEN = os.getenv('QRADAR_API_TOKEN')

headers = {
    'SEC': API_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Version': '27.0' # Şəkildəki API versiyası
}

def sync_rule(file_path):
    with open(file_path, 'r') as f:
        rule_content = json.load(f)
    
    # JSON-dan QRadar qayda ID-sini götürürük
    rule_id = rule_content.get('id')
    
    if not rule_id:
        print(f"Xəta: {file_path} faylında qayda 'id' nömrəsi qeyd edilməyib.")
        return

    # Sənədə tam uyğun endpoint: /analytics/rules/{id}
    url = f"https://{QRADAR_IP}/api/analytics/rules/{rule_id}"
    
    # Yalnız QRadar-ın icazə verdiyi dəyişənləri göndəririk
    update_data = {
        "enabled": rule_content.get("enabled", True),
        "owner": rule_content.get("owner", "admin")
    }
    
    try:
        response = requests.post(url, headers=headers, json=update_data, verify=False)
        print(f"Fayl: {file_path} | Status Kodu: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print(f"UĞUR: {rule_id} nömrəli qaydanın statusu QRadar-da uğurla yeniləndi!")
        else:
            print(f"Xəta Mesajı: {response.text}")
            
    except Exception as e:
        print(f"Bağlantı xətası: {str(e)}")

# 'rules' qovluğundakı bütün JSON fayllarını işlət
for filename in os.listdir('rules'):
    if filename.endswith('.json'):
        sync_rule(f'rules/{filename}')
