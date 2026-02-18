-- Daily Trend per Stock
SELECT
    symbol,
    trading_date,
    close,
    price_change_pct
FROM finance.stock_dlt.gold_daily_stock_summary
ORDER BY symbol, trading_date

-- Average Daily Return
SELECT
    symbol,
    AVG(price_change_pct) AS avg_daily_return
FROM finance.stock_dlt.gold_daily_stock_summary
GROUP BY symbol

-- Volume Analysis
SELECT
    symbol,
    trading_date,
    volume
FROM finance.stock_dlt.gold_daily_stock_summary
ORDER BY trading_date DESC
