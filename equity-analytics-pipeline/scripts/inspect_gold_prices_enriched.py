from src.utils.spark_session import get_spark
from pathlib import Path
from pyspark.sql.functions import col

project_root = Path(__file__).resolve().parents[1]
path = project_root / "data" / "gold" / "prices_enriched"

spark = get_spark("inspect_prices_enriched")

df = spark.read.parquet(str(path))

df.printSchema()

df.show(5, truncate=False)

df.filter(col("company_name").isNull()).select("ticker").distinct().show()

spark.stop()