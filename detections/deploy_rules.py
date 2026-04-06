import requests
import json
import os

# Məlumatlarını bura daxil et
QRADAR_IP = "54.208.168.148" # Sənin şəkildəki IP-n
API_TOKEN = "59afca94-fddb-42ad-b319-b3385b4676c9"

HEADERS = {
    "SEC": API_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def deploy_rule(json_path):
    url = f"https://{QRADAR_IP}/api/analytics/rules"
    
    with open(json_path, 'r') as f:
        rule_content = json.load(f)
    
    # QRadar-a POST (Yeni yaratmaq) sorğusu göndəririk
    response = requests.post(url, headers=HEADERS, json=rule_content, verify=False)
    
    if response.status_code == 201:
        print(f"Uğurlu: {rule_content['name']} yaradıldı.")
    else:
        print(f"Xəta: {response.status_code} - {response.text}")

# Qovluqdakı bütün rule-ları yoxla
rule_folder = "detections/"
for file_name in os.listdir(rule_folder):
    if file_name.endswith(".json"):
        deploy_rule(os.path.join(rule_folder, file_name))
