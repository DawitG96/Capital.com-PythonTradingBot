import requests
import pandas as pd
import json
import os
import time
from dotenv import load_dotenv
import sys

# Carica variabili da .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = "https://api-capital.backend-capital.com"

EPICS = os.getenv("EPICS").split(",")
RESOLUTIONS = os.getenv("RESOLUTIONS").split(",")

HEADERS = {"X-CAP-API-KEY": API_KEY, "Content-Type": "application/json"}
SESSION_TOKEN = None

def start_new_session():
    global SESSION_TOKEN, SECURITY_TOKEN
    url = f"{BASE_URL}/api/v1/session"
    payload = json.dumps({"identifier": EMAIL, "password": PASSWORD})
    response = requests.post(url, headers=HEADERS, data=payload)

    if response.status_code == 200:
        SESSION_TOKEN = response.headers.get("CST")
        SECURITY_TOKEN = response.headers.get("X-SECURITY-TOKEN")
        HEADERS["CST"] = SESSION_TOKEN
        HEADERS["X-SECURITY-TOKEN"] = SECURITY_TOKEN
    else:
        print(f"❌ ERRORE {response.status_code}: {response.text}")
        sys.exit(1)

def fetch_historical_data(epic, resolution, max_bars=1000):
    url = f"{BASE_URL}/api/v1/prices/{epic}?resolution={resolution}&max={max_bars}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()["prices"]
        df = pd.DataFrame(data)
        df["snapshotTime"] = pd.to_datetime(df["snapshotTime"])
        return df
    else:
        print(f"❌ Errore EPIC {epic} ({resolution}): {response.json()}")
        return None

def process_epic(epic):
    os.makedirs("datasets", exist_ok=True)
    for resolution in RESOLUTIONS:
        print(f"📊 Scaricando dati per {epic} ({resolution})...")
        df = fetch_historical_data(epic, resolution)
        if df is not None:
            filename = f"datasets/{epic}_{resolution}.csv"
            df.to_csv(filename, index=False)
            print(f"✅ Salvato {filename}")
        time.sleep(2)

if __name__ == "__main__":
    start_new_session()
    epic = sys.argv[1]  # Riceve l'EPIC come argomento
    process_epic(epic)
