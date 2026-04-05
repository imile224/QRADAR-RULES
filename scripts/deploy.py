import requests
import os

QRADAR_IP = os.getenv("QRADAR_IP")
TOKEN = os.getenv("QRADAR_API_TOKEN")

url = f"https://{QRADAR_IP}/api/config/extension_management/extensions"

headers = {
    "SEC": TOKEN,
    "Version": "27.0"
}

for file_name in os.listdir("rules"):
    if file_name.endswith(".xml"):
        file_path = f"rules/{file_name}"
        
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(url, headers=headers, files=files, verify=False)
            
            print(f"{file_name} -> {response.status_code}")
            print(response.text)
