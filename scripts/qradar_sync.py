import requests
import json
import os
import urllib3

# SSL xəbərdarlıqlarını söndürmək üçün
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_IP = os.getenv('QRADAR_IP')
API_TOKEN = os.getenv('QRADAR_API_TOKEN')

HEADERS = {
    'SEC': API_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def create_or_update_rule(file_path):
    with open(file_path, 'r') as f:
        rule_data = json.load(f)
    
    # QAYDA YARATMAQ ÜÇÜN ƏSAS ENDPOINT (ID OLMADAN)
    base_url = f"https://{QRADAR_IP}/api/analytics/rules"

    print(f"Pushing rule: {rule_data['name']}...")
    
    # Yeni qayda yaratmaq üçün POST istifadə edirik
    response = requests.post(base_url, headers=HEADERS, data=json.dumps(rule_data), verify=False)

    if response.status_code == 201:
        print("Uğurla yaradıldı (Created)!")
    elif response.status_code == 409:
        print("Bu adda qayda artıq var. Yeniləmə (Update) rejiminə keçilir...")
        # Burada artıq mövcud olan qaydanı yeniləmək üçün PUT metodundan istifadə edə bilərsiniz.
    else:
        print(f"Xəta: {response.status_code} - {response.text}")

if __name__ == "__main__":
    rule_dir = "rules/"
    for filename in os.listdir(rule_dir):
        if filename.endswith(".json"):
            create_or_update_rule(os.path.join(rule_dir, filename))
