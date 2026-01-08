from pyspark.sql.functions import (
    col,
    to_date,
    trim,
    upper,
    regexp_replace,
    when
)
from src.utils.spark_session import get_spark
from src.utils.config import Paths
from pyspark.sql.types import DoubleType, LongType


def transform_companies_bronze_to_silver() -> None:
    """
    Cleans and standardizes company reference data
    from bronze → silver layer.
    """
    spark = get_spark()
    paths = Paths()

    df = spark.read.parquet(paths.BRONZE_COMPANIES_DIR)

    # Normalize column names (bronze CSV has spaces)
    df = (
        df
        .withColumnRenamed("company name", "company_name")
        .withColumnRenamed("short name", "short_name")
        .withColumnRenamed("market cap", "market_cap")
    )

    # Select analytical columns only
    df = df.select(
        "ticker",
        "company_name",
        "short_name",
        "sector",
        "industry",
        "exchange",
        "market_cap",
        "website",
    )

    # Normalize text fields
    df = (
        df
        .withColumn("ticker", upper(trim(col("ticker"))))
        .withColumn("company_name", trim(col("company_name")))
        .withColumn("short_name", trim(col("short_name")))
        .withColumn("sector", trim(col("sector")))
        .withColumn("industry", trim(col("industry")))
        .withColumn("exchange", trim(col("exchange")))
    )

    # Safely convert market cap to numeric
    df = df.withColumn(
        "market_cap",
        when(
            regexp_replace(col("market_cap"), ",", "").rlike("^[0-9]+(\\.[0-9]+)?$"),
            regexp_replace(col("market_cap"), ",", "").cast(DoubleType())
        ).otherwise(None)
    )

    # Drop invalid records
    df = df.dropna(subset=["ticker", "sector", "industry"])

    # One row per company
    df = df.dropDuplicates(["ticker"])

    df.write.mode("overwrite").parquet(paths.SILVER_COMPANIES_DIR)

    spark.stop()


def transform_prices_bronze_to_silver() -> None:
    """
    Cleans and validates historical price data
    from bronze → silver layer.
    """
    spark = get_spark()
    paths = Paths()

    df = spark.read.parquet(paths.BRONZE_PRICES_DIR)

    # Normalize column names
    df = (
        df
        .withColumnRenamed("Date", "date")
        .withColumnRenamed("Open", "open")
        .withColumnRenamed("High", "high")
        .withColumnRenamed("Low", "low")
        .withColumnRenamed("Close", "close")
        .withColumnRenamed("Adj Close", "adj_close")
        .withColumnRenamed("Volume", "volume")
    )

    # Enforce correct data types
    df = (
        df
        .withColumn("date", to_date(col("date")))
        .withColumn("open", col("open").cast(DoubleType()))
        .withColumn("high", col("high").cast(DoubleType()))
        .withColumn("low", col("low").cast(DoubleType()))
        .withColumn("close", col("close").cast(DoubleType()))
        .withColumn("adj_close", col("adj_close").cast(DoubleType()))
        .withColumn("volume", col("volume").cast(LongType()))
    )

    # Drop rows missing critical fields
    df = df.dropna(subset=["ticker", "date", "adj_close", "volume"])

    # Financial sanity checks
    df = df.filter(
        (col("open") >= 0) &
        (col("high") >= 0) &
        (col("low") >= 0) &
        (col("close") >= 0) &
        (col("adj_close") > 0) &
        (col("volume") > 0) &
        (col("high") >= col("low"))
    )

    # Ensure uniqueness per trading day
    df = df.dropDuplicates(["ticker", "date"])

    df.write.mode("overwrite").partitionBy("ticker").parquet(paths.SILVER_PRICES_DIR)

    spark.stop()
