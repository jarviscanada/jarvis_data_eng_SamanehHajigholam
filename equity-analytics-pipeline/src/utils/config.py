import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Paths:
    # Project root (used for local development defaults)
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    #print(PROJECT_ROOT)

    # Raw data
    RAW_PRICES_DIR: str = os.getenv(
        "RAW_PRICES_DIR", str(PROJECT_ROOT / "data" / "raw" / "us_stocks_etfs")
    )
    RAW_COMPANIES_CSV: str = os.getenv(
        "RAW_COMPANIES_CSV", str(PROJECT_ROOT / "data" / "raw" / "company_info_and_logos" / "companies.csv")
    )

    # Bronze layer
    BRONZE_COMPANIES_DIR: str = os.getenv(
        "BRONZE_COMPANIES_DIR", str(PROJECT_ROOT / "data" / "bronze" / "companies")
    )
    BRONZE_PRICES_DIR: str = os.getenv(
        "BRONZE_PRICES_DIR", str(PROJECT_ROOT / "data" / "bronze" / "prices")
    )

    # Silver layer
    SILVER_COMPANIES_DIR: str = os.getenv(
        "SILVER_COMPANIES_DIR", str(PROJECT_ROOT / "data" / "silver" / "companies")
    )
    SILVER_PRICES_DIR: str = os.getenv(
        "SILVER_PRICES_DIR", str(PROJECT_ROOT / "data" / "silver" / "prices")
    )

    # Gold layer
    GOLD_ENRICHED_DIR: str = os.getenv(
        "GOLD_ENRICHED_DIR", str(PROJECT_ROOT / "data" / "gold" / "prices_enriched")
    )
    GOLD_ANALYTICS_DIR: str = os.getenv(
        "GOLD_ANALYTICS_DIR", str(PROJECT_ROOT / "data" / "gold" / "analytics")
    )


@dataclass(frozen=True)
class PipelineConfig:
    APP_NAME: str = os.getenv("SPARK_APP_NAME", "equity-market-etl")
    SPARK_MASTER: str = os.getenv("SPARK_MASTER", "local[*]")
    SHUFFLE_PARTITIONS: str = os.getenv("SPARK_SHUFFLE_PARTITIONS", "8")

