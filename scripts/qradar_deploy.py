import os, json, sys, time, requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_IP = os.getenv("QRADAR_IP", "")
API_TOKEN = os.getenv("QRADAR_API_KEY", "")
RULES_PATH = "rules/"
HEADERS = {"SEC": API_TOKEN, "Accept": "application/json", "Version": "12.0", "Content-Type": "application/x-www-form-urlencoded"}
BASE_URL = f"https://{QRADAR_IP}/api"

def main():
    if not QRADAR_IP or not API_TOKEN:
        print("[ERROR] QRADAR_IP ve QRADAR_API_KEY teleb olunur.")
        sys.exit(1)
    ok = err = skip = 0
    for filename in sorted(os.listdir(RULES_PATH)):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(RULES_PATH, filename), "r", encoding="utf-8") as f:
            rule = json.load(f)
        name = rule.get("name", filename)
        aql = ""
        for expr in rule.get("filter_expressions", []):
            if expr.get("expression_type") == "AQL":
                aql = expr.get("expression", "")
                break
        if not aql:
            print(f"  [SKIP] {name}")
            skip += 1
            continue
        r = requests.post(f"{BASE_URL}/ariel/searches", headers=HEADERS, data=f"query_expression={requests.utils.quote(aql)}", verify=False)
        if r.status_code in (200, 201):
            print(f"  [OK] {name}")
            ok += 1
        else:
            print(f"  [ERROR] {name} -> {r.status_code}: {r.text[:150]}")
            err += 1
        time.sleep(0.5)
    print(f"\n[RESULT] OK: {ok} | SKIP: {skip} | XETA: {err}")
    if err: sys.exit(1)

if __name__ == "__main__":
    main()
