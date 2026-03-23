from pyspark.sql import SparkSession
from src.utils.config import PipelineConfig


def get_spark() -> SparkSession:
    config = PipelineConfig()

    spark = (
        SparkSession.builder
        .appName(config.APP_NAME)
        .master(config.SPARK_MASTER)
        .config(
            "spark.sql.shuffle.partitions",
            str(config.SHUFFLE_PARTITIONS)
        )
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")
    return spark
