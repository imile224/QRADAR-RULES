import os
import requests
import json

# Bu məlumatları GitHub Secrets-dən götürəcəyik (Təhlükəsizlik üçün)
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
    
    # QRadar API-yə müraciət (nümunə endpoint)
    url = f"https://{QRADAR_IP}/api/analytics/rules"
    
    # Qeyd: Real mühitdə əvvəl rule-un varlığını yoxlayıb sonra POST və ya PUT edirik
    response = requests.post(url, headers=headers, json=rule_content, verify=False)
    
    if response.status_code == 201:
        print(f"Success: {file_path} QRadar-a əlavə edildi.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Rules qovluğundakı bütün JSON-ları yoxla
for filename in os.listdir('rules'):
    if filename.endswith('.json'):
        sync_rule(f'rules/{filename}')
