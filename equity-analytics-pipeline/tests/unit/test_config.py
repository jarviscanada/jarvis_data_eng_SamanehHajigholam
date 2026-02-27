from src.utils.config import Paths, PipelineConfig

def test_default_paths_exist_format():
    p = Paths()
    assert p.RAW_PRICES_DIR.startswith("/opt/data")or p.RAW_PRICES_DIR.startswith("/")
    assert p.RAW_COMPANIES_CSV.endswith(".csv")


def test_pipeline_config_defaults():
    """
    Validate default Spark configuration values.
    """
    cfg = PipelineConfig()

    assert cfg.APP_NAME == "equity-market-etl"
    assert cfg.SPARK_MASTER.startswith("local")
    assert int(cfg.SHUFFLE_PARTITIONS) > 0