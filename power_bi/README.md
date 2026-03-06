# Stocks Dashboard

## Description
An interactive Power BI dashboard that provides a quick and insightful 
glance at key stock data for a chosen ticker. Built using Alpha Vantage's 
API as the data source and Power Query M queries for data ingestion. This dashboard is useful for 
anyone looking to monitor key metrics, historical price trends, volume 
activity, and upcoming earnings estimates without navigating multiple 
financial platforms.

## Data
All data is sourced from the **Alpha Vantage API** using Power Query M queries:
- **Time Series Daily** — daily OHLCV (open, high, low, close, volume) 
  data for the selected ticker
- **Company Overview** — key financial metadata including market cap, P/E 
  ratio, forward P/E, price-to-book, price-to-sales, dividend yield, 
  analyst target price, and company description
- **Earnings Calendar** — upcoming EPS estimates for AAPL, MSFT, META, 
  GOOG, and AMZN pulled from a 3-month earnings calendar

## Visuals
- **Name card** — displays the company name from the Overview table
- **Description card** — displays the full company description
- **KPI metrics** — today's close, analyst target price, 52W high/low, 
  market cap, dividend yield, P/E ratio, forward P/E, price-to-sales, 
  and price-to-book
- **Volume chart** (stacked column) and **Close price chart** (line) 
  stacked on top of each other with a shared date axis
- **Time period slicer** (1mo, 3mo, 6mo, 1yr, 5yr) to dynamically 
  filter both charts
- **Clustered bar chart** comparing upcoming EPS estimates across 
  AAPL, MSFT, META, GOOG, and the selected ticker

## Constraints & Limitations
- The Alpha Vantage free tier is limited to **25 API requests per day**, 
  meaning the dashboard data cannot be refreshed frequently without 
  upgrading to a premium key
- Data refresh is **manual** — the dashboard does not auto-refresh
- The dashboard currently tracks a focused set of tickers for the 
  earnings comparison chart and would need to be updated to add more

## Future Improvements
- Automate daily data refresh using Power BI Service scheduled refresh
- Upgrade to a premium Alpha Vantage key to remove API rate limit constraints
- Expand the earnings comparison chart to include more tickers