import json
import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# GitHub Secrets-dən məlumatları oxuyur
QRADAR_URL = os.getenv('QRADAR_URL')
SEC_TOKEN = os.getenv('SEC_TOKEN')

HEADERS = {
    'SEC': SEC_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
API_ENDPOINT = f"{QRADAR_URL}/api/analytics/rules"
RULES_DIR = "rules"

def deploy():
    if not QRADAR_URL or not SEC_TOKEN:
        print("XƏTA: QRADAR_URL və ya SEC_TOKEN tapılmadı!")
        return

    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(RULES_DIR, filename), 'r') as f:
                rule_data = json.load(f)
                
            print(f"Yüklənir: {filename}...")
            response = requests.post(API_ENDPOINT, headers=HEADERS, json=rule_data, verify=False)
            
            if response.status_code in [200, 201]:
                print(f"UĞURLU: {filename} QRadar-a göndərildi.")
            else:
                print(f"XƏTA ({response.status_code}): {response.text}")

if __name__ == "__main__":
    deploy()
