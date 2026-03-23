import pytest
from pyspark.sql.functions import col, isnan
from src.utils.config import Paths

# --------------------------
# Pytest fixture for shared SparkSession
# --------------------------
from src.utils.spark_session import get_spark

@pytest.fixture(scope="session")
def spark():
    spark_session = get_spark()
    yield spark_session
    spark_session.stop()


# --------------------------
# Silver Layer Tests
# --------------------------
def test_silver_companies_created(spark):
    paths = Paths()
    df = spark.read.parquet(paths.SILVER_COMPANIES_DIR)

    # Check required columns
    required_cols = ["ticker", "company_name", "sector", "industry", "exchange", "market_cap"]
    missing = [c for c in required_cols if c not in df.columns]
    assert not missing, f"Missing columns in silver_companies: {missing}"

    # Ensure non-empty
    assert df.count() > 0, "silver_companies is empty"


def test_silver_prices_created(spark):
    paths = Paths()
    df = spark.read.parquet(paths.SILVER_PRICES_DIR)

    # Check required columns
    required_cols = ["date", "ticker", "open", "high", "low", "close", "adj_close", "volume"]
    missing = [c for c in required_cols if c not in df.columns]
    assert not missing, f"Missing columns in silver_prices: {missing}"

    # Ensure no nulls in critical fields
    critical_cols = ["date", "ticker", "adj_close", "volume"]
    for c in critical_cols:
        null_count = df.filter(col(c).isNull()).count()
        assert null_count == 0, f"Found {null_count} nulls in {c}"

    # Financial sanity
    for c in ["open", "high", "low", "close", "adj_close"]:
        neg_count = df.filter(col(c) < 0).count()
        assert neg_count == 0, f"Found {neg_count} negative values in {c}"

    invalid_high_low = df.filter(col("high") < col("low")).count()
    assert invalid_high_low == 0, f"Found {invalid_high_low} rows with high < low"

    vol_count = df.filter(col("volume") <= 0).count()
    assert vol_count == 0, f"Found {vol_count} rows with non-positive volume"

    # Unique (ticker, date)
    dup_count = df.groupBy("ticker", "date").count().filter(col("count") > 1).count()
    assert dup_count == 0, f"Found {dup_count} duplicate (ticker, date) rows"


# --------------------------
# Gold Layer Tests
# --------------------------
def test_gold_prices_enriched_created(spark):
    paths = Paths()
    df = spark.read.parquet(paths.GOLD_ENRICHED_DIR)

    required_cols = [
        "date", "ticker", "open", "high", "low", "close", "adj_close",
        "volume", "daily_return"
    ]
    missing = [c for c in required_cols if c not in df.columns]
    assert not missing, f"Missing columns in gold_prices_enriched: {missing}"
    assert df.count() > 0, "gold_prices_enriched is empty"


def test_gold_prices_enriched_no_nulls(spark):
    paths = Paths()
    df = spark.read.parquet(paths.GOLD_ENRICHED_DIR)

    # Non-numeric columns
    for c in ["date", "ticker"]:
        null_count = df.filter(col(c).isNull()).count()
        assert null_count == 0, f"Found {null_count} nulls in {c}"

    # Check nulls for numeric columns except daily_return
    for c in ["open", "high", "low", "close", "adj_close", "volume"]:
        null_count = df.filter(col(c).isNull() | isnan(col(c))).count()
        assert null_count == 0, f"Found {null_count} nulls in {c}"

    # For daily_return, ignore nulls for first row (or just allow some nulls)
    null_count = df.filter(col("daily_return").isNull()).count()
    # Allow up to 1 null per ticker
    tickers = [row.ticker for row in df.select("ticker").distinct().collect()]
    max_allowed_nulls = len(tickers)
    assert null_count <= max_allowed_nulls, f"Found {null_count} nulls in daily_return (expected <= {max_allowed_nulls})"



def test_gold_prices_enriched_sanity(spark):
    paths = Paths()
    df = spark.read.parquet(paths.GOLD_ENRICHED_DIR)

    price_cols = ["open", "high", "low", "close", "adj_close"]
    for c in price_cols:
        neg_count = df.filter(col(c) < 0).count()
        assert neg_count == 0, f"Found {neg_count} negative values in {c}"

    invalid_high_low = df.filter(col("high") < col("low")).count()
    assert invalid_high_low == 0, f"Found {invalid_high_low} rows with high < low"

    vol_count = df.filter(col("volume") <= 0).count()
    assert vol_count == 0, f"Found {vol_count} rows with non-positive volume"


def test_gold_prices_enriched_unique_rows(spark):
    paths = Paths()
    df = spark.read.parquet(paths.GOLD_ENRICHED_DIR)

    dup_count = df.groupBy("ticker", "date").count().filter(col("count") > 1).count()
    assert dup_count == 0, f"Found {dup_count} duplicate (ticker, date) rows"


def test_gold_analytics_sanity(spark):
    paths = Paths()

    # Test sector daily average return
    sector_df = spark.read.parquet(f"{paths.GOLD_ANALYTICS_DIR}/sector_daily_avg_return")
    required_cols_sector = ["date", "sector", "avg_daily_return"]
    missing_sector = [c for c in required_cols_sector if c not in sector_df.columns]
    assert not missing_sector, f"Missing columns in sector_daily_avg_return: {missing_sector}"
    null_count = sector_df.filter(col("avg_daily_return").isNull() | isnan(col("avg_daily_return"))).count()
    assert null_count == 0, f"Found {null_count} nulls in avg_daily_return"

    # Test industry 20-day volatility
    industry_df = spark.read.parquet(f"{paths.GOLD_ANALYTICS_DIR}/industry_20d_volatility")
    required_cols_industry = ["industry", "avg_20d_volatility"]
    missing_industry = [c for c in required_cols_industry if c not in industry_df.columns]
    assert not missing_industry, f"Missing columns in industry_20d_volatility: {missing_industry}"
    null_count = industry_df.filter(col("avg_20d_volatility").isNull() | isnan(col("avg_20d_volatility"))).count()
    assert null_count == 0, f"Found {null_count} nulls in avg_20d_volatility"

