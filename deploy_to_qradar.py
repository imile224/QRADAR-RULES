import json
import os
import requests
import urllib3

# SSL xəbərdarlıqlarını söndürmək üçün (əgər self-signed sertifikatdırsa)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Config faylını oxumaq
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

QRADAR_URL = config['qradar_url']
SEC_TOKEN = config['sec_token']
HEADERS = {
    'SEC': SEC_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
API_ENDPOINT = f"{QRADAR_URL}/api/analytics/rules"
RULES_DIR = "rules"

def deploy_rules():
    print("QRadar API Rule Deployment Started...\n")
    
    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(RULES_DIR, filename)
            
            with open(file_path, 'r') as rule_file:
                rule_payload = json.load(rule_file)
                
            print(f"Deploying rule: {rule_payload.get('name')}")
            
            response = requests.post(
                API_ENDPOINT,
                headers=HEADERS,
                json=rule_payload,
                verify=False # Mühitinə görə True edə bilərsən
            )
            
            if response.status_code in [200, 201]:
                print(f"[+] UĞURLU: {filename} QRadar-a əlavə edildi.\n")
            else:
                print(f"[-] XƏTA: {filename} əlavə edilə bilmədi.")
                print(f"Status Code: {response.status_code}, Detal: {response.text}\n")

if __name__ == "__main__":
    deploy_rules()
