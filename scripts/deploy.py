import os, requests, json, sys

QRADAR_IP = os.getenv('QRADAR_IP')
API_KEY = os.getenv('QRADAR_API_KEY')

headers = {
    'SEC': f"{API_KEY}",
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Version': '27.0'
}

def sync_rules():
    rules_path = 'rules/'
    for filename in os.listdir(rules_path):
        if filename.endswith('.json'):
            with open(os.path.join(rules_path, filename), 'r') as f:
                rule_data = json.load(f)
            
            rule_name = rule_data['name']
            print(f"İşlənir: {rule_name}")

            # 1. Mövcud qaydanı tapmaq üçün yoxlama (Search)
            search_url = f"https://{QRADAR_IP}/api/analytics/rules?filter=name%3D%22{rule_name}%22"
            res = requests.get(search_url, headers=headers, verify=False)
            
            if res.status_code == 200 and len(res.json()) > 0:
                # 2. Varsa UPDATE (PUT) et
                rule_id = res.json()[0]['id']
                put_url = f"https://{QRADAR_IP}/api/analytics/rules/{rule_id}"
                update_res = requests.put(put_url, headers=headers, json=rule_data, verify=False)
                print(f"Update olundu: {update_res.status_code}")
            else:
                # 3. Yoxdursa YARAT (POST)
                post_url = f"https://{QRADAR_IP}/api/analytics/rules"
                create_res = requests.post(post_url, headers=headers, json=rule_data, verify=False)
                print(f"Yeni yaradıldı: {create_res.status_code}")

if __name__ == "__main__":
    sync_rules()
