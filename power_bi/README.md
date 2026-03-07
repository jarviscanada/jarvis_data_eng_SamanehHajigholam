# Data Professionals Survey 2022

## Overview

A Power BI dashboards built from a 2022 online survey of **630 data professionals**. The reports transform raw survey responses into visual insights covering career trends, compensation, satisfaction, and more. An overview of the 2022 survey results, showing who responded, what they earn, and how satisfied they are in their roles.

**Use Case:** Useful for students entering the field or teams benchmarking against industry norms.

**Data Shown:** Job title distribution, average salary by role, favorite programming languages, work-life balance and salary satisfaction scores, difficulty breaking into the field, and respondent demographics (age, country).

**Transformations:** Blank rows removed via Power Query; data loaded from `Data Professionals Survey 2022.xlsx`.

## Future Improvements
- Add slicers for experience level, gender, and education for deeper filtering
- Normalize salary data by cost of living for fairer cross-country comparisons

---

# Stocks Dashboard

## Overview
An interactive Power BI dashboard that provides a quick and insightful 
glance at key stock data for a chosen ticker. Built using Alpha Vantage's 
API as the data source and Power Query M queries for data ingestion. This dashboard is useful for 
anyone looking to monitor key metrics, historical price trends, volume 
activity, and upcoming earnings estimates without navigating multiple 
financial platforms.

## Data
All data is sourced from the **Alpha Vantage API** using Power Query M queries:
- **Time Series Daily**: daily OHLCV (open, high, low, close, volume) 
  data for the selected ticker
- **Company Overview**: key financial metadata including market cap, P/E 
  ratio, forward P/E, price-to-book, price-to-sales, dividend yield, 
  analyst target price, and company description
- **Earnings Calendar**: upcoming EPS estimates for AAPL, MSFT, META, 
  GOOG, and AMZN pulled from a 3-month earnings calendar

## Visuals
- **Name card**: displays the company name from the Overview table
- **Description card**: displays the full company description
- **KPI metrics**: today's close, analyst target price, 52W high/low, 
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
- Data refresh is **manual**: the dashboard does not auto-refresh
- The dashboard currently tracks a focused set of tickers for the 
  earnings comparison chart and would need to be updated to add more

## Future Improvements
- Automate daily data refresh using Power BI Service scheduled refresh
- Upgrade to a premium Alpha Vantage key to remove API rate limit constraints
- Expand the earnings comparison chart to include more tickers

---

# Coca-Cola Sales & Financials Dashboard
An interactive dashboard built on a made up Coca-Cola dataset loaded from Excel via Power Query, analyzing sales performance, profitability, pricing, and regional distribution across brands and time periods. Useful for practicing financial analysis and exploring how sales and margins vary across brands and regions.

**Data Shown:**
- **AI-powered Q&A visual** — allows users to ask natural language questions directly about the data
- **Key Influencers visual** — identifies what factors most drive profit margins per brand
- **Scatter chart** — uses to visualize sales by region (map visual unavailable)
- **Matrix** — breaks down financials including price per unit and operating profit
- **Dynamic timeline slicer** — lets users filter all visuals by a custom date range

**Improvements:** 
- Replace scatter chart with map visual — Once access is available, swap the scatter chart for a proper map visual to better visualisation
- Add brand/product slicers so users can isolate performance metrics per product line
