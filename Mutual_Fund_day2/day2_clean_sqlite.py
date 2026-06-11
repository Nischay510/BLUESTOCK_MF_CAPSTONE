import os
import sqlite3
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
SQL_DIR = "sql"
REPORTS_DIR = "reports"

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(SQL_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

DB_PATH = "bluestock_mf.db"
engine = create_engine(f"sqlite:///{DB_PATH}")


def clean_columns(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def find_col(df, possible_names):
    for col in possible_names:
        if col in df.columns:
            return col
    return None


files = {
    "fund_master": "01_fund_master.csv",
    "nav_history": "02_nav_history.csv",
    "aum": "03_aum_by_fund_house.csv",
    "sip": "04_monthly_sip_inflows.csv",
    "category_inflows": "05_category_inflows.csv",
    "folio": "06_industry_folio_count.csv",
    "performance": "07_scheme_performance.csv",
    "transactions": "08_investor_transactions.csv",
    "portfolio": "09_portfolio_holdings.csv",
    "benchmark": "10_benchmark_indices.csv"
}

data = {}

for name, file in files.items():
    path = os.path.join(RAW_DIR, file)
    df = pd.read_csv(path)
    df = clean_columns(df)
    data[name] = df
    print(f"{name}: {df.shape}")


# -------------------------
# Clean Fund Master
# -------------------------
fund = data["fund_master"]

if "afmi_code" in fund.columns:
    fund = fund.rename(columns={"afmi_code": "amfi_code"})

fund["amfi_code"] = fund["amfi_code"].astype(str)

fund = fund.drop_duplicates(subset=["amfi_code"])

fund.to_csv(f"{PROCESSED_DIR}/clean_fund_master.csv", index=False)


# -------------------------
# Clean NAV History
# -------------------------
nav = data["nav_history"]

if "afmi_code" in nav.columns:
    nav = nav.rename(columns={"afmi_code": "amfi_code"})

date_col = find_col(nav, ["date", "nav_date"])
nav_col = find_col(nav, ["nav", "net_asset_value"])

nav["amfi_code"] = nav["amfi_code"].astype(str)
nav[date_col] = pd.to_datetime(nav[date_col], errors="coerce")
nav[nav_col] = pd.to_numeric(nav[nav_col], errors="coerce")

nav = nav.dropna(subset=["amfi_code", date_col])
nav = nav.sort_values(["amfi_code", date_col])
nav = nav.drop_duplicates(subset=["amfi_code", date_col], keep="last")

nav[nav_col] = nav.groupby("amfi_code")[nav_col].ffill()
nav = nav[nav[nav_col] > 0]

nav = nav.rename(columns={date_col: "date", nav_col: "nav"})
nav.to_csv(f"{PROCESSED_DIR}/clean_nav_history.csv", index=False)


# -------------------------
# Clean Investor Transactions
# -------------------------
tx = data["transactions"]

tx["amfi_code"] = tx["amfi_code"].astype(str)
tx["transaction_date"] = pd.to_datetime(tx["transaction_date"], errors="coerce")
tx["amount_inr"] = pd.to_numeric(tx["amount_inr"], errors="coerce")

tx["transaction_type"] = (
    tx["transaction_type"]
    .astype(str)
    .str.strip()
    .str.lower()
    .replace({
        "sip": "SIP",
        "lumpsum": "Lumpsum",
        "lump sum": "Lumpsum",
        "redemption": "Redemption"
    })
)

tx = tx[tx["transaction_type"].isin(["SIP", "Lumpsum", "Redemption"])]

tx["kyc_status"] = tx["kyc_status"].astype(str).str.strip().str.title()
tx["kyc_valid_flag"] = tx["kyc_status"].isin(["Verified", "Pending", "Rejected"])

tx = tx.dropna(subset=["transaction_date", "amount_inr"])
tx = tx[tx["amount_inr"] > 0]

tx = tx.rename(columns={
    "transaction_date": "date",
    "amount_inr": "amount"
})

tx.to_csv(f"{PROCESSED_DIR}/clean_investor_transactions.csv", index=False)


# -------------------------
# Clean Scheme Performance
# -------------------------
perf = data["performance"]

if "afmi_code" in perf.columns:
    perf = perf.rename(columns={"afmi_code": "amfi_code"})

perf["amfi_code"] = perf["amfi_code"].astype(str)

numeric_keywords = [
    "return", "sharpe", "sortino", "alpha", "beta",
    "drawdown", "std", "expense"
]

for col in perf.columns:
    if any(key in col for key in numeric_keywords):
        perf[col] = (
            perf[col]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace(",", "", regex=False)
        )
        perf[col] = pd.to_numeric(perf[col], errors="coerce")

expense_col = find_col(perf, ["expense_ratio", "expense_ratio_%"])

if expense_col:
    perf["expense_ratio_anomaly"] = ~perf[expense_col].between(0.1, 2.5)

return_cols = [c for c in perf.columns if "return" in c]
for col in return_cols:
    perf[f"{col}_anomaly"] = perf[col].isna() | (perf[col] < -100) | (perf[col] > 200)

perf.to_csv(f"{PROCESSED_DIR}/clean_scheme_performance.csv", index=False)


# -------------------------
# Save Other Cleaned CSVs
# -------------------------
other_names = {
    "aum": "clean_aum_by_fund_house.csv",
    "sip": "clean_monthly_sip_inflows.csv",
    "category_inflows": "clean_category_inflows.csv",
    "folio": "clean_industry_folio_count.csv",
    "portfolio": "clean_portfolio_holdings.csv",
    "benchmark": "clean_benchmark_indices.csv"
}

for key, out_file in other_names.items():
    df = data[key]

    if "afmi_code" in df.columns:
        df = df.rename(columns={"afmi_code": "amfi_code"})

    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    df = df.drop_duplicates()
    df.to_csv(f"{PROCESSED_DIR}/{out_file}", index=False)


# -------------------------
# Create dim_date
# -------------------------
date_min = nav["date"].min()
date_max = nav["date"].max()

dim_date = pd.DataFrame({
    "date": pd.date_range(date_min, date_max, freq="D")
})

dim_date["date_id"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
dim_date["year"] = dim_date["date"].dt.year
dim_date["month"] = dim_date["date"].dt.month
dim_date["month_name"] = dim_date["date"].dt.month_name()
dim_date["quarter"] = dim_date["date"].dt.quarter
dim_date["is_weekday"] = dim_date["date"].dt.weekday < 5

dim_date.to_csv(f"{PROCESSED_DIR}/clean_dim_date.csv", index=False)


# -------------------------
# Create schema.sql
# -------------------------
schema_sql = """
DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_fund;

CREATE TABLE dim_fund (
    amfi_code TEXT PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    risk_grade TEXT,
    expense_ratio REAL,
    fund_manager TEXT
);

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date DATE UNIQUE,
    year INTEGER,
    month INTEGER,
    month_name TEXT,
    quarter INTEGER,
    is_weekday BOOLEAN
);

CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT,
    date DATE,
    nav REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_transactions (
    transaction_id TEXT PRIMARY KEY,
    investor_id TEXT,
    amfi_code TEXT,
    date DATE,
    amount REAL,
    transaction_type TEXT,
    state TEXT,
    city_tier TEXT,
    age_group TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT,
    return_1yr REAL,
    return_3yr REAL,
    return_5yr REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    alpha REAL,
    beta REAL,
    max_drawdown REAL,
    std_dev REAL,
    expense_ratio REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house TEXT,
    date DATE,
    year INTEGER,
    quarter TEXT,
    aum_crore REAL,
    num_schemes INTEGER
);
"""

with open(f"{SQL_DIR}/schema.sql", "w") as f:
    f.write(schema_sql)


# -------------------------
# Load into SQLite
# -------------------------
with sqlite3.connect(DB_PATH) as conn:
    conn.executescript(schema_sql)

fund_dim = fund[[
    "amfi_code",
    "scheme_name",
    "fund_house",
    "category",
    "sub_category",
    "expense_ratio_pct",
    "fund_manager",
    "risk_category"
]].copy()

fund_dim = fund_dim.rename(columns={
    "expense_ratio_pct": "expense_ratio",
    "risk_category": "risk_grade"
})

fund_dim.to_sql("dim_fund", engine, if_exists="append", index=False)
dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
nav.to_sql("fact_nav", engine, if_exists="append", index=False)
tx_db = tx[[
    "investor_id",
    "amfi_code",
    "date",
    "amount",
    "transaction_type",
    "state",
    "city_tier",
    "age_group",
    "kyc_status"
]].copy()

tx_db.insert(0, "transaction_id", range(1, len(tx_db) + 1))

tx_db.to_sql("fact_transactions", engine, if_exists="append", index=False)
perf_db = perf[[
    "amfi_code",
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "sharpe_ratio",
    "sortino_ratio",
    "alpha",
    "beta",
    "max_drawdown_pct",
    "std_dev_ann_pct",
    "expense_ratio_pct"
]].copy()

perf_db = perf_db.rename(columns={
    "return_1yr_pct": "return_1yr",
    "return_3yr_pct": "return_3yr",
    "return_5yr_pct": "return_5yr",
    "max_drawdown_pct": "max_drawdown",
    "std_dev_ann_pct": "std_dev",
    "expense_ratio_pct": "expense_ratio"
})

perf_db.to_sql("fact_performance", engine, if_exists="append", index=False)
aum_db = data["aum"][[
    "fund_house",
    "date",
    "aum_crore",
    "num_schemes"
]].copy()

aum_db["year"] = pd.to_datetime(aum_db["date"], errors="coerce").dt.year
aum_db["quarter"] = pd.to_datetime(aum_db["date"], errors="coerce").dt.quarter

aum_db.to_sql("fact_aum", engine, if_exists="append", index=False)


# -------------------------
# Verify Row Counts
# -------------------------
tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

print("\nSQLite Row Counts:")
with sqlite3.connect(DB_PATH) as conn:
    for table in tables:
        count = pd.read_sql(f"SELECT COUNT(*) AS rows FROM {table}", conn)
        print(table, count.iloc[0]["rows"])


# -------------------------
# Create queries.sql
# -------------------------
queries_sql = """
-- 1. Top 5 fund houses by AUM
SELECT fund_house, SUM(aum_crore) AS total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC
LIMIT 5;

-- 2. Average NAV per month
SELECT 
    amfi_code,
    strftime('%Y-%m', date) AS month,
    AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, strftime('%Y-%m', date)
ORDER BY month;

-- 3. SIP YoY growth
SELECT 
    year,
    SUM(sip_inflow_crore) AS total_sip_inflow
FROM clean_monthly_sip_inflows
GROUP BY year
ORDER BY year;

-- 4. Transactions by state
SELECT 
    state,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- 5. Funds with expense ratio less than 1%
SELECT 
    amfi_code,
    expense_ratio
FROM fact_performance
WHERE expense_ratio < 1;

-- 6. Top 10 funds by Sharpe ratio
SELECT 
    amfi_code,
    sharpe_ratio
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 10;

-- 7. Funds with negative alpha
SELECT 
    amfi_code,
    alpha
FROM fact_performance
WHERE alpha < 0
ORDER BY alpha ASC;

-- 8. Average transaction amount by transaction type
SELECT 
    transaction_type,
    COUNT(*) AS total_transactions,
    AVG(amount) AS avg_amount
FROM fact_transactions
GROUP BY transaction_type;

-- 9. NAV date range by fund
SELECT 
    amfi_code,
    MIN(date) AS start_date,
    MAX(date) AS end_date,
    COUNT(*) AS nav_records
FROM fact_nav
GROUP BY amfi_code;

-- 10. Highest AUM fund house by year
SELECT 
    year,
    fund_house,
    MAX(aum_crore) AS max_aum
FROM fact_aum
GROUP BY year
ORDER BY year;
"""

with open(f"{SQL_DIR}/queries.sql", "w") as f:
    f.write(queries_sql)


# -------------------------
# Create Data Dictionary
# -------------------------
dictionary = "# Data Dictionary\n\n"
dictionary += "## Source\n"
dictionary += "Raw CSV files from `data/raw/`, cleaned CSV files stored in `data/processed/`, and SQLite database stored as `bluestock_mf.db`.\n\n"

for file in os.listdir(PROCESSED_DIR):
    if file.endswith(".csv"):
        path = os.path.join(PROCESSED_DIR, file)
        df = pd.read_csv(path, nrows=5)

        dictionary += f"## {file}\n\n"
        dictionary += "| Column | Data Type | Business Definition | Source |\n"
        dictionary += "|---|---|---|---|\n"

        for col in df.columns:
            dictionary += f"| {col} | {df[col].dtype} | {col.replace('_', ' ').title()} field used for mutual fund analytics | {file} |\n"

        dictionary += "\n"

with open("data_dictionary.md", "w") as f:
    f.write(dictionary)

print("\nDay 2 completed successfully.")
print("Cleaned CSVs saved in data/processed/")
print("Database created: bluestock_mf.db")
print("SQL files saved in sql/")
print("Data dictionary created: data_dictionary.md")