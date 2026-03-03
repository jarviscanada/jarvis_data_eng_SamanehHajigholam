-- KPI - Total Fraud Loss
USE ws_banking_etl2.gold;

SELECT 
    SUM(total_fraud_loss) AS total_fraud_loss
FROM daily_fraud_losses;

-- Monthly Fraud Trends
SELECT 
    year,
    date_format(to_date(concat(year, '-', lpad(month, 2, '0'), '-01')), 'MMM') AS month,
    fraud_rate,
    total_fraud_amount
FROM monthly_fraud_trends
ORDER BY year, month;

-- Top Fraud Users
SELECT *
FROM top_fraud_users
ORDER BY fraud_transaction_count DESC
LIMIT 10;

-- Fraud by Value Segment
SELECT *
FROM fraud_by_value_segment
ORDER BY fraud_rate DESC;

-- Trend - Fraud Rate
SELECT 
    transaction_date,
    fraud_rate
FROM fraud_rate_trend
ORDER BY transaction_date;

-- Fraud by Weekday
SELECT *
FROM fraud_by_weekday
ORDER BY fraud_transaction_count DESC;

-- Average Daily Return
SELECT
    symbol,
    AVG(price_change_pct) AS avg_daily_return
FROM finance.stock_dlt.gold_daily_stock_summary
GROUP BY symbol
