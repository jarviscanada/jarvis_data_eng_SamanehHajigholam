from src.utils.config import Paths
from src.utils.spark_session import get_spark


def ingest_companies():
    spark = get_spark()

    paths = Paths()

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(paths.RAW_COMPANIES_CSV)
    )

    df.write.mode("overwrite").parquet(paths.BRONZE_COMPANIES_DIR)

    spark.stop()

