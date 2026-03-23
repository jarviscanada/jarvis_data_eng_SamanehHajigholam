from src.utils.config import Paths
from pyspark.sql.functions import regexp_extract, input_file_name
from src.utils.spark_session import get_spark


def ingest_prices():
    spark = get_spark()
    paths = Paths()

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(f"{paths.RAW_PRICES_DIR}/*.csv")  # Read all CSVs
        .withColumn(
            "ticker",
            regexp_extract(input_file_name(), r"([^/]+)\.csv$", 1)
        )
    )

    (
        df.write
        .mode("overwrite")
        .partitionBy("ticker")
        .parquet(paths.BRONZE_PRICES_DIR)
    )

    spark.stop()
