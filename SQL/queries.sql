
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
