import dlt
import requests
import time
from pyspark.sql.functions import col
from datetime import datetime, timezone

# =========================
# CONFIG
# =========================
# API_KEY = dbutils.secrets.get("dlt-scope", "alpha-key")

SYMBOLS = ["AAPL", "MSFT", "GOOGL", "TSLA"]
BASE_URL = "https://www.alphavantage.co/query"


# =========================
# BRONZE - STOCK DATA
# =========================
def fetch_stock_data():
    records = []

    for symbol in SYMBOLS:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact",
            "apikey": "RVPR7AZ4VY4ZKUKX"
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "Time Series (Daily)" not in data:
            print(f"Error for {symbol}: {data}")
            continue

        for date, values in data["Time Series (Daily)"].items():
            records.append({
                "symbol": symbol,
                "trading_date": date,
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": int(values["5. volume"]),
                "ingestion_timestamp": datetime.now(timezone.utc)
            })

        time.sleep(12)  # API limit

    return records


@dlt.table(
    name="bronze_stock_data",
    comment="Raw stock data from Alpha Vantage API"
)
def bronze_stock_data():
    df = spark.createDataFrame(fetch_stock_data())
    return df.withColumn("trading_date", col("trading_date").cast("date"))


# =========================
# BRONZE - COMPANY DATA
# =========================
def fetch_company_data():
    records = []

    for symbol in SYMBOLS:
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": "RVPR7AZ4VY4ZKUKX"
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "Symbol" not in data:
            continue

        records.append({
            "symbol": data.get("Symbol"),
            "name": data.get("Name"),
            "sector": data.get("Sector"),
            "exchange": data.get("Exchange"),
            "ingestion_timestamp": datetime.now(timezone.utc)
        })

        time.sleep(12)

    return records


@dlt.table(
    name="bronze_company_info",
    comment="Raw company metadata from API"
)
def bronze_company_info():
    return spark.createDataFrame(fetch_company_data())


# =========================
# SILVER - STOCK DATA (STREAMING)
# =========================
@dlt.table(
    name="silver_stock_data",
    comment="Cleaned stock data with metrics"
)
@dlt.expect("valid_price", "open > 0 AND close > 0")
@dlt.expect("valid_volume", "volume >= 0")
def silver_stock_data():
    return (
        dlt.read_stream("bronze_stock_data")
        .dropDuplicates(["symbol", "trading_date"])
        .withColumn("price_change", col("close") - col("open"))
        .withColumn(
            "price_change_pct",
            (col("close") - col("open")) / col("open") * 100
        )
    )


# =========================
# SILVER - COMPANY (SCD TYPE 2)
# =========================
dlt.create_streaming_table("silver_company_info")

dlt.apply_changes(
    target="silver_company_info",
    source="bronze_company_info",
    keys=["symbol"],
    sequence_by=col("ingestion_timestamp"),
    stored_as_scd_type=2
)


# =========================
# GOLD - MATERIALIZED VIEW
# =========================
@dlt.table(
    name="gold_daily_stock_summary",
    comment="Daily stock summary enriched with company data"
)
def gold_daily_stock_summary():
    return (
        dlt.read("silver_stock_data")   # batch read
        .join(dlt.read("silver_company_info"), "symbol", "left")
        .select(
            "symbol",
            "name",
            "sector",
            "exchange",
            "trading_date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "price_change",
            "price_change_pct"
        )
    )