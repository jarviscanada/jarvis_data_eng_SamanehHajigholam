# a shell-based pipeline runner.
#!/bin/bash
set -e

echo "Starting data pipeline..."

# Set Airflow home and python path
export PROJECT_ROOT="$(pwd)"
export AIRFLOW_HOME="$PROJECT_ROOT/airflow"
export PYTHONPATH="$PROJECT_ROOT"

# Activate virtual environment if exists
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Run ETL stages
echo "Running Bronze layer..."
python -m src.ingestion.ingest_companies
python -m src.ingestion.ingest_prices

echo "Running Silver layer..."
python -m src.transformations.bronze_to_silver

echo "Running Gold layer..."
python -m src.transformations.silver_to_gold

echo "Running tests..."
pytest tests/

echo "Pipeline completed successfully."
