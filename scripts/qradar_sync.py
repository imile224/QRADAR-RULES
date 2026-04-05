import requests
import json
import os

# GitHub Secrets-dən gələcək məlumatlar
QRADAR_IP = os.getenv('QRADAR_IP')
API_TOKEN = os.getenv('QRADAR_API_TOKEN')

HEADERS = {
    'SEC': API_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def sync_rule(file_path):
    with open(file_path, 'r') as f:
        rule_data = json.load(f)
    
    # Qeyd: Real mühitdə qaydanın ID-sini təyin etmək üçün 
    # əvvəlcə GET ilə axtarış verib sonra ID-yə görə POST/PUT edilir.
    rule_id = "100051"  # Nümunə ID
    url = f"https://{QRADAR_IP}/api/analytics/rules/{rule_id}"

    print(f"Updating rule: {rule_data['name']}...")
    
    # Sizin şəkildəki POST metodundan istifadə edirik
    response = requests.post(url, headers=HEADERS, data=json.dumps(rule_data), verify=False)

    if response.status_code == 200:
        print("Uğurla yeniləndi!")
    else:
        print(f"Xəta baş verdi: {response.status_code} - {response.text}")

if __name__ == "__main__":
    rule_dir = "rules/"
    for filename in os.listdir(rule_dir):
        if filename.endswith(".json"):
            sync_rule(os.path.join(rule_dir, filename))
