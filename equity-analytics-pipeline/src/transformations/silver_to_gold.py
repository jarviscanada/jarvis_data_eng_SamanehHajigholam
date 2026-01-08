from pyspark.sql import Window
from pyspark.sql.functions import col, lag, avg, stddev, upper, trim
from pyspark.sql.types import DoubleType
from src.utils.spark_session import get_spark
from src.utils.config import Paths


def create_gold_enriched() -> None:
    """
    Create gold enriched table by joining silver prices and companies,
    and calculate daily returns per ticker.
    """
    p = Paths()
    spark = get_spark()

    # Read silver layer
    prices = spark.read.parquet(p.SILVER_PRICES_DIR)
    companies = spark.read.parquet(p.SILVER_COMPANIES_DIR)

    # Join prices with company metadata
    enriched = prices.join(companies, on="ticker", how="left").filter(col("sector").isNotNull())

    # Daily returns using adj_close (robust for corporate actions)
    w = Window.partitionBy("ticker").orderBy("date")
    enriched = enriched.withColumn("prev_adj_close", lag(col("adj_close"), 1).over(w))
    enriched = enriched.withColumn(
        "daily_return",
        ((col("adj_close") / col("prev_adj_close")) - 1).cast(DoubleType())
    ).drop("prev_adj_close")

    # Save enriched gold
    enriched.write.mode("overwrite").partitionBy("ticker").parquet(p.GOLD_ENRICHED_DIR)

    spark.stop()


def create_gold_analytics() -> None:
    """
    Create gold analytics tables, e.g.:
    - sector_daily_avg_return
    - industry_20d_volatility
    """
    p = Paths()
    spark = get_spark()

    df = spark.read.parquet(p.GOLD_ENRICHED_DIR).dropna(
        subset=["daily_return", "sector", "industry", "date"]
    )

    # -----------------------------
    # Sector daily average return
    # -----------------------------
    sector_daily = df.groupBy("date", "sector").agg(
        avg(col("daily_return")).alias("avg_daily_return")
    )
    sector_daily.write.mode("overwrite").parquet(
        f"{p.GOLD_ANALYTICS_DIR}/sector_daily_avg_return"
    )

    # -----------------------------
    # Industry 20-day rolling volatility
    # -----------------------------
    w20 = Window.partitionBy("industry", "ticker").orderBy("date").rowsBetween(-19, 0)
    industry_vol = df.withColumn("rolling_volatility_20", stddev("daily_return").over(w20))
    industry_vol = industry_vol.groupBy("industry").agg(
        avg(col("rolling_volatility_20")).alias("avg_20d_volatility")
    )
    industry_vol.write.mode("overwrite").parquet(
        f"{p.GOLD_ANALYTICS_DIR}/industry_20d_volatility"
    )

    spark.stop()
