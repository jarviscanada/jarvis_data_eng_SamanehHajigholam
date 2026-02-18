import dlt
from pyspark.sql.functions import col

# =========================
# BRONZE LAYER
# =========================

@dlt.table(
    name="bronze_stock_data",
    comment="Raw stock data ingested from Alpha Vantage"
)
def bronze_stock_data():
    return (
        spark.readStream
        .table("finance.stock_dlt.raw_stock_data")
    )


@dlt.table(
    name="bronze_company_info",
    comment="Raw company metadata from Alpha Vantage"
)
def bronze_company_info():
    return (
        spark.readStream
        .table("finance.stock_dlt.raw_company_info")
    )


# =========================
# SILVER LAYER
# =========================

@dlt.table(
    name="silver_stock_data",
    comment="Cleaned stock data with calculated metrics"
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


@dlt.table(
    name="silver_company_info",
    comment="Company metadata (SCD Type 1)"
)
def silver_company_info():
    return dlt.read_stream("bronze_company_info").dropDuplicates(["symbol"])


# =========================
# GOLD LAYER
# =========================

@dlt.table(
    name="gold_daily_stock_summary",
    comment="Daily stock summary joined with company metadata"
)
def gold_daily_stock_summary():
    stock_df = dlt.read("silver_stock_data")
    company_df = dlt.read("silver_company_info")

    return (
        stock_df
        .join(company_df, "symbol", "left")
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
