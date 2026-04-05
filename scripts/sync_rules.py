import os
import requests
import json
import urllib3

# SSL xəbərdarlıqlarını gizlət
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
    
    url = f"https://{QRADAR_IP}/api/analytics/rules"
    
    try:
        response = requests.post(url, headers=headers, json=rule_content, verify=False)
        print(f"Fayl: {file_path}")
        print(f"Status Kodu: {response.status_code}")
        print(f"Cavab: {response.text}")
        
        if response.status_code not in [200, 201]:
            exit(1) # GitHub-da qırmızı yansın deyə xəta ilə bitiririk
            
    except Exception as e:
        print(f"Bağlantı xətası: {str(e)}")
        exit(1)

for filename in os.listdir('rules'):
    if filename.endswith('.json'):
        sync_rule(f'rules/{filename}')
