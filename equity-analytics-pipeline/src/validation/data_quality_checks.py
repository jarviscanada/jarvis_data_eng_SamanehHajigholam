from typing import List
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, isnan
from src.utils.spark_session import get_spark
from src.utils.config import Paths


class DataQualityError(RuntimeError):
    """Custom exception for data quality issues."""
    pass


def _require_columns(df: DataFrame, required: List[str], dataset_name: str) -> None:
    cols = set([c.lower() for c in df.columns])
    missing = [c for c in required if c.lower() not in cols]
    if missing:
        raise DataQualityError(f"[{dataset_name}] Missing required columns: {missing}")


def _fail_if(df: DataFrame, condition, message: str) -> None:
    bad = df.filter(condition).limit(1).count()
    if bad > 0:
        raise DataQualityError(message)


# ------------------------ Bronze Checks ------------------------
def bronze_checks() -> None:
    """
    Structural checks on bronze data (raw ingestion).
    """
    p = Paths()
    spark = get_spark()

    prices = spark.read.parquet(p.BRONZE_PRICES_DIR)
    companies = spark.read.parquet(p.BRONZE_COMPANIES_DIR)

    _require_columns(
        prices,
        ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "ticker"],
        "bronze_prices"
    )

    _require_columns(
        companies,
        ["ticker", "company name", "sector"],
        "bronze_companies"
    )

    # Basic emptiness checks
    if prices.limit(1).count() == 0:
        raise DataQualityError("[bronze_prices] No rows found")

    if companies.limit(1).count() == 0:
        raise DataQualityError("[bronze_companies] No rows found")

    spark.stop()


# ------------------------ Silver Checks ------------------------
def silver_checks() -> None:
    """Business-rule checks on silver layer."""
    p = Paths()
    spark = get_spark()

    prices = spark.read.parquet(p.SILVER_PRICES_DIR)
    companies = spark.read.parquet(p.SILVER_COMPANIES_DIR)

    # Required columns
    _require_columns(prices, ["date", "open", "high", "low", "close", "adj_close", "volume", "ticker"], "silver_prices")
    _require_columns(companies, ["ticker", "company_name", "sector"], "silver_companies")

    # Null checks (non-numeric)
    for c in ["date", "ticker"]:
        _fail_if(prices, col(c).isNull(),
            f"[silver_prices] Null found in {c}"
        )

    # Null / NaN checks (numeric only)
    for c in ["adj_close", "volume"]:
        _fail_if(prices, col(c).isNull() | isnan(col(c)),
            f"[silver_prices] Null/NaN found in {c}"
        )

    # Non-negative prices and volume
    _fail_if(prices, (col("open") < 0) | (col("high") < 0) | (col("low") < 0) |
                      (col("close") < 0) | (col("adj_close") < 0),
             "[silver_prices] Negative price found")
    _fail_if(prices, col("volume") < 0, "[silver_prices] Negative volume found")

    # High >= Low
    _fail_if(prices, col("high") < col("low"), "[silver_prices] Found high < low")

    # Uniqueness check: (ticker, date) should be unique
    dup_count = prices.groupBy("ticker", "date").count().filter(col("count") > 1).limit(1).count()
    if dup_count > 0:
        raise DataQualityError("[silver_prices] Duplicate (ticker, date) rows found")

    spark.stop()


# ------------------------ Gold Checks ------------------------
def gold_checks() -> None:
    """Ensure gold outputs are coherent and join succeeded."""
    p = Paths()
    spark = get_spark()

    enriched = spark.read.parquet(p.GOLD_ENRICHED_DIR)
    _require_columns(enriched, ["ticker", "date", "adj_close", "company_name", "sector", "industry"], "gold_prices_enriched")

    # Join success: sector and industry should not be null
    _fail_if(enriched, col("sector").isNull(), "[gold_prices_enriched] sector is null (join likely failed)")
    _fail_if(enriched, col("industry").isNull(), "[gold_prices_enriched] industry is null (join likely failed)")

    # Daily return sanity range
    _fail_if(enriched, (col("daily_return") < -0.9) | (col("daily_return") > 0.9),
             "[gold_prices_enriched] Extreme daily_return values detected")

    spark.stop()
