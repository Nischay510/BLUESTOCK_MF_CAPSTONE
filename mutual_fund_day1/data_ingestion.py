import os
import pandas as pd

RAW_DIR = "data/raw"
REPORTS_DIR = "reports"

os.makedirs(REPORTS_DIR, exist_ok=True)

csv_files = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

summary = []

for file in csv_files:
    path = os.path.join(RAW_DIR, file)

    print("\n" + "=" * 80)
    print(f"Loading file: {file}")

    try:
        df = pd.read_csv(path)

        print("Shape:", df.shape)
        print("\nData Types:")
        print(df.dtypes)
        print("\nHead:")
        print(df.head())

        nulls = df.isnull().sum().sum()
        duplicates = df.duplicated().sum()

        summary.append({
            "file": file,
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing_values": nulls,
            "duplicate_rows": duplicates
        })

    except FileNotFoundError:
        print(f"File not found: {path}")
        summary.append({
            "file": file,
            "rows": "File Missing",
            "columns": "File Missing",
            "missing_values": "File Missing",
            "duplicate_rows": "File Missing"
        })

summary_df = pd.DataFrame(summary)
summary_df.to_csv(os.path.join(REPORTS_DIR, "data_quality_summary.csv"), index=False)

print("\nData Quality Summary saved to reports/data_quality_summary.csv")


# Fund master exploration
fund_master_path = os.path.join(RAW_DIR, "01_fund_master.csv")
nav_history_path = os.path.join(RAW_DIR, "02_nav_history.csv")

fund_master = pd.read_csv(fund_master_path)
nav_history = pd.read_csv(nav_history_path)

print("\n" + "=" * 80)
print("FUND MASTER EXPLORATION")

for col in ["fund_house", "category", "sub_category", "risk_grade"]:
    if col in fund_master.columns:
        print(f"\nUnique values in {col}:")
        print(fund_master[col].dropna().unique())


# AMFI code validation
print("\n" + "=" * 80)
print("AMFI CODE VALIDATION")

fund_master["amfi_code"] = fund_master["amfi_code"].astype(str)
nav_history["amfi_code"] = nav_history["amfi_code"].astype(str)

master_codes = set(fund_master["amfi_code"])
nav_codes = set(nav_history["amfi_code"])

missing_codes = master_codes - nav_codes

if len(missing_codes) == 0:
    print("All AMFI codes in fund_master exist in nav_history.")
else:
    print("Missing AMFI codes in nav_history:")
    print(missing_codes)

with open(os.path.join(REPORTS_DIR, "data_quality_report.txt"), "w") as f:
    f.write("DATA QUALITY REPORT\n")
    f.write("=" * 50 + "\n\n")
    f.write(summary_df.to_string(index=False))
    f.write("\n\nAMFI CODE VALIDATION\n")
    f.write("=" * 50 + "\n")

    if len(missing_codes) == 0:
        f.write("\nAll AMFI codes in fund_master exist in nav_history.\n")
    else:
        f.write("\nMissing AMFI codes in nav_history:\n")
        f.write(str(missing_codes))

print("Detailed report saved to reports/data_quality_report.txt")