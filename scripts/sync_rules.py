import os
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_IP = os.getenv('QRADAR_IP')
API_TOKEN = os.getenv('QRADAR_API_TOKEN')

headers = {
    'SEC': API_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def sync_rule(file_path):
    with open(file_path, 'r') as f:
        rule_content = json.load(f)
    
    # Yeni endpoint: analytics deyil, config/event_rules olmalıdır
    url = f"https://{QRADAR_IP}/api/config/event_rules"
    
    try:
        response = requests.post(url, headers=headers, json=rule_content, verify=False)
        print(f"Fayl: {file_path} | Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("Uğurla QRadar-a əlavə edildi!")
        else:
            print(f"Xəta mesajı: {response.text}")
            
    except Exception as e:
        print(f"Bağlantı xətası: {str(e)}")

for filename in os.listdir('rules'):
    if filename.endswith('.json'):
        sync_rule(f'rules/{filename}')
