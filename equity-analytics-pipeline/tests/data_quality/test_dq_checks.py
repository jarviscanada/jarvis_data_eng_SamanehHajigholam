import os
import pytest
from src.validation.data_quality_checks import bronze_checks, silver_checks, gold_checks
from src.utils.config import Paths

paths = Paths()

@pytest.mark.skipif(not os.path.exists(paths.BRONZE_COMPANIES_DIR), reason="Bronze layer not built yet")
def test_bronze_checks():
    bronze_checks()

@pytest.mark.skipif(not os.path.exists(paths.SILVER_COMPANIES_DIR), reason="Silver layer not built yet")
def test_silver_checks():
    silver_checks()

@pytest.mark.skipif(not os.path.exists(paths.GOLD_ENRICHED_DIR), reason="Gold layer not built yet")
def test_gold_checks():
    gold_checks()
