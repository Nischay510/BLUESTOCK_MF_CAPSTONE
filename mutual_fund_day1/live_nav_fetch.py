import os
import requests
import pandas as pd

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

schemes = {
    "HDFC_Top_100_Direct": "125497",
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841"
}

def fetch_nav(scheme_name, scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"

    print(f"\nFetching NAV for {scheme_name} ({scheme_code})")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    meta = data.get("meta", {})
    nav_data = data.get("data", [])

    df = pd.DataFrame(nav_data)

    if df.empty:
        print(f"No data found for {scheme_name}")
        return

    df["scheme_code"] = scheme_code
    df["scheme_name"] = meta.get("scheme_name", scheme_name)
    df["fund_house"] = meta.get("fund_house", "")
    df["scheme_category"] = meta.get("scheme_category", "")
    df["scheme_type"] = meta.get("scheme_type", "")

    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    df = df[[
        "scheme_code",
        "scheme_name",
        "fund_house",
        "scheme_category",
        "scheme_type",
        "date",
        "nav"
    ]]

    file_name = f"live_nav_{scheme_code}_{scheme_name}.csv"
    file_path = os.path.join(RAW_DIR, file_name)

    df.to_csv(file_path, index=False)

    print(f"Saved: {file_path}")
    print("Shape:", df.shape)
    print(df.head())

for scheme_name, scheme_code in schemes.items():
    try:
        fetch_nav(scheme_name, scheme_code)
    except Exception as e:
        print(f"Error fetching {scheme_name}: {e}")