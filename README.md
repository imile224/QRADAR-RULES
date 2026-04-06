# QRadar Custom Rules via API

## 📌 Project Overview
This repository contains a collection of Custom Offense Rules for IBM QRadar SIEM. Instead of manually creating rules through the QRadar Web GUI, this project automates the deployment process using QRadar's REST API and Python.

## 🚀 Features
- **Infrastructure as Code (IaC) approach for SIEM rules:** Rules are stored as JSON payloads.
- **Automated Deployment:** Python script reads the JSON rule definitions and deploys them directly to QRadar via API.
- **Sysmon Integration:** Includes rules specifically tailored for advanced threat detection using Windows Sysmon logs.

## 🛠️ Usage Instructions
1. Clone the repository.
2. Edit the `config.json` file with your QRadar IP/FQDN and SEC (Authorized Service) Token.
3. Add your custom rules in JSON format to the `rules/` directory.
4. Run the deployment script:
   ```bash
   python3 deploy_to_qradar.py
