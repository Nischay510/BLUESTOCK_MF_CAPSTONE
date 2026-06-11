# Data Dictionary

## Source
Raw CSV files from `data/raw/`, cleaned CSV files stored in `data/processed/`, and SQLite database stored as `bluestock_mf.db`.

## clean_dim_date.csv

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| date | str | Date field used for mutual fund analytics | clean_dim_date.csv |
| date_id | int64 | Date Id field used for mutual fund analytics | clean_dim_date.csv |
| year | int64 | Year field used for mutual fund analytics | clean_dim_date.csv |
| month | int64 | Month field used for mutual fund analytics | clean_dim_date.csv |
| month_name | str | Month Name field used for mutual fund analytics | clean_dim_date.csv |
| quarter | int64 | Quarter field used for mutual fund analytics | clean_dim_date.csv |
| is_weekday | bool | Is Weekday field used for mutual fund analytics | clean_dim_date.csv |

## clean_industry_folio_count.csv

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| month | str | Month field used for mutual fund analytics | clean_industry_folio_count.csv |
| total_folios_crore | float64 | Total Folios Crore field used for mutual fund analytics | clean_industry_folio_count.csv |
| equity_folios_crore | float64 | Equity Folios Crore field used for mutual fund analytics | clean_industry_folio_count.csv |
| debt_folios_crore | float64 | Debt Folios Crore field used for mutual fund analytics | clean_industry_folio_count.csv |
| hybrid_folios_crore | float64 | Hybrid Folios Crore field used for mutual fund analytics | clean_industry_folio_count.csv |
| others_folios_crore | float64 | Others Folios Crore field used for mutual fund analytics | clean_industry_folio_count.csv |

## clean_aum_by_fund_house.csv

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| date | str | Date field used for mutual fund analytics | clean_aum_by_fund_house.csv |
| fund_house | str | Fund House field used for mutual fund analytics | clean_aum_by_fund_house.csv |
| aum_lakh_crore | float64 | Aum Lakh Crore field used for mutual fund analytics | clean_aum_by_fund_house.csv |
| aum_crore | int64 | Aum Crore field used for mutual fund analytics | clean_aum_by_fund_house.csv |
| num_schemes | int64 | Num Schemes field used for mutual fund analytics | clean_aum_by_fund_house.csv |

## clean_scheme_performance.csv

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| amfi_code | int64 | Amfi Code field used for mutual fund analytics | clean_scheme_performance.csv |
| scheme_name | str | Scheme Name field used for mutual fund analytics | clean_scheme_performance.csv |
| fund_house | str | Fund House field used for mutual fund analytics | clean_scheme_performance.csv |
| category | str | Category field used for mutual fund analytics | clean_scheme_performance.csv |
| plan | str | Plan field used for mutual fund analytics | clean_scheme_performance.csv |
| return_1yr_pct | float64 | Return 1Yr Pct field used for mutual fund analytics | clean_scheme_performance.csv |
| return_3yr_pct | float64 | Return 3Yr Pct field used for mutual fund analytics | clean_scheme_performance.csv |
| return_5yr_pct | float64 | Return 5Yr Pct field used for mutual fund analytics | clean_scheme_performance.csv |
| benchmark_3yr_pct | float64 | Benchmark 3Yr Pct field used for mutual fund analytics | clean_scheme_performance.csv |
| alpha | float64 | Alpha field used for mutual fund analytics | clean_scheme_performance.csv |
| beta | float64 | Beta field used for mutual fund analytics | clean_scheme_performance.csv |
| sharpe_ratio | float64 | Sharpe Ratio field used for mutual fund analytics | clean_scheme_performance.csv |
| sortino_ratio | float64 | Sortino Ratio field used for mutual fund analytics | clean_scheme_performance.csv |
| std_dev_ann_pct | float64 | Std Dev Ann Pct field used for mutual fund analytics | clean_scheme_performance.csv |
| max_drawdown_pct | float64 | Max Drawdown Pct field used for mutual fund analytics | clean_scheme_performance.csv |
| aum_crore | int64 | Aum Crore field used for mutual fund analytics | clean_scheme_performance.csv |
| expense_ratio_pct | float64 | Expense Ratio Pct field used for mutual fund analytics | clean_scheme_performance.csv |
| morningstar_rating | int64 | Morningstar Rating field used for mutual fund analytics | clean_scheme_performance.csv |
| risk_grade | str | Risk Grade field used for mutual fund analytics | clean_scheme_performance.csv |
| return_1yr_pct_anomaly | bool | Return 1Yr Pct Anomaly field used for mutual fund analytics | clean_scheme_performance.csv |
| return_3yr_pct_anomaly | bool | Return 3Yr Pct Anomaly field used for mutual fund analytics | clean_scheme_performance.csv |
| return_5yr_pct_anomaly | bool | Return 5Yr Pct Anomaly field used for mutual fund analytics | clean_scheme_performance.csv |

## clean_benchmark_indices.csv

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| date | str | Date field used for mutual fund analytics | clean_benchmark_indices.csv |
| index_name | str | Index Name field used for mutual fund analytics | clean_benchmark_indices.csv |
| close_value | float64 | Close Value field used for mutual fund analytics | clean_benchmark_indices.csv |

## clean_fund_master.csv

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| amfi_code | int64 | Amfi Code field used for mutual fund analytics | clean_fund_master.csv |
| fund_house | str | Fund House field used for mutual fund analytics | clean_fund_master.csv |
| scheme_name | str | Scheme Name field used for mutual fund analytics | clean_fund_master.csv |
| category | str | Category field used for mutual fund analytics | clean_fund_master.csv |
| sub_category | str | Sub Category field used for mutual fund analytics | clean_fund_master.csv |
| plan | str | Plan field used for mutual fund analytics | clean_fund_master.csv |
| launch_date | str | Launch Date field used for mutual fund analytics | clean_fund_master.csv |
| benchmark | str | Benchmark field used for mutual fund analytics | clean_fund_master.csv |
| expense_ratio_pct | float64 | Expense Ratio Pct field used for mutual fund analytics | clean_fund_master.csv |
| exit_load_pct | float64 | Exit Load Pct field used for mutual fund analytics | clean_fund_master.csv |
| min_sip_amount | int64 | Min Sip Amount field used for mutual fund analytics | clean_fund_master.csv |
| min_lumpsum_amount | int64 | Min Lumpsum Amount field used for mutual fund analytics | clean_fund_master.csv |
| fund_manager | str | Fund Manager field used for mutual fund analytics | clean_fund_master.csv |
| risk_category | str | Risk Category field used for mutual fund analytics | clean_fund_master.csv |
| sebi_category_code | str | Sebi Category Code field used for mutual fund analytics | clean_fund_master.csv |

## clean_monthly_sip_inflows.csv

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| month | str | Month field used for mutual fund analytics | clean_monthly_sip_inflows.csv |
| sip_inflow_crore | int64 | Sip Inflow Crore field used for mutual fund analytics | clean_monthly_sip_inflows.csv |
| active_sip_accounts_crore | float64 | Active Sip Accounts Crore field used for mutual fund analytics | clean_monthly_sip_inflows.csv |
| new_sip_accounts_lakh | float64 | New Sip Accounts Lakh field used for mutual fund analytics | clean_monthly_sip_inflows.csv |
| sip_aum_lakh_crore | float64 | Sip Aum Lakh Crore field used for mutual fund analytics | clean_monthly_sip_inflows.csv |
| yoy_growth_pct | float64 | Yoy Growth Pct field used for mutual fund analytics | clean_monthly_sip_inflows.csv |

## clean_category_inflows.csv

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| month | str | Month field used for mutual fund analytics | clean_category_inflows.csv |
| category | str | Category field used for mutual fund analytics | clean_category_inflows.csv |
| net_inflow_crore | float64 | Net Inflow Crore field used for mutual fund analytics | clean_category_inflows.csv |

## clean_investor_transactions.csv

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| investor_id | str | Investor Id field used for mutual fund analytics | clean_investor_transactions.csv |
| date | str | Date field used for mutual fund analytics | clean_investor_transactions.csv |
| amfi_code | int64 | Amfi Code field used for mutual fund analytics | clean_investor_transactions.csv |
| transaction_type | str | Transaction Type field used for mutual fund analytics | clean_investor_transactions.csv |
| amount | int64 | Amount field used for mutual fund analytics | clean_investor_transactions.csv |
| state | str | State field used for mutual fund analytics | clean_investor_transactions.csv |
| city | str | City field used for mutual fund analytics | clean_investor_transactions.csv |
| city_tier | str | City Tier field used for mutual fund analytics | clean_investor_transactions.csv |
| age_group | str | Age Group field used for mutual fund analytics | clean_investor_transactions.csv |
| gender | str | Gender field used for mutual fund analytics | clean_investor_transactions.csv |
| annual_income_lakh | float64 | Annual Income Lakh field used for mutual fund analytics | clean_investor_transactions.csv |
| payment_mode | str | Payment Mode field used for mutual fund analytics | clean_investor_transactions.csv |
| kyc_status | str | Kyc Status field used for mutual fund analytics | clean_investor_transactions.csv |
| kyc_valid_flag | bool | Kyc Valid Flag field used for mutual fund analytics | clean_investor_transactions.csv |

## clean_portfolio_holdings.csv

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| amfi_code | int64 | Amfi Code field used for mutual fund analytics | clean_portfolio_holdings.csv |
| stock_symbol | str | Stock Symbol field used for mutual fund analytics | clean_portfolio_holdings.csv |
| stock_name | str | Stock Name field used for mutual fund analytics | clean_portfolio_holdings.csv |
| sector | str | Sector field used for mutual fund analytics | clean_portfolio_holdings.csv |
| weight_pct | float64 | Weight Pct field used for mutual fund analytics | clean_portfolio_holdings.csv |
| market_value_cr | float64 | Market Value Cr field used for mutual fund analytics | clean_portfolio_holdings.csv |
| current_price_inr | float64 | Current Price Inr field used for mutual fund analytics | clean_portfolio_holdings.csv |
| portfolio_date | str | Portfolio Date field used for mutual fund analytics | clean_portfolio_holdings.csv |

## clean_nav_history.csv

| Column | Data Type | Business Definition | Source |
|---|---|---|---|
| amfi_code | int64 | Amfi Code field used for mutual fund analytics | clean_nav_history.csv |
| date | str | Date field used for mutual fund analytics | clean_nav_history.csv |
| nav | float64 | Nav field used for mutual fund analytics | clean_nav_history.csv |

