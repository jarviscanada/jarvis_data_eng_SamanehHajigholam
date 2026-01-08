#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  source venv/bin/activate
  echo "Virtual environment activated"
else
  echo "Warning: venv not found"
fi

export PROJECT_ROOT="$(pwd)"
export AIRFLOW_HOME="$PROJECT_ROOT/airflow"
export PYTHONPATH="$PROJECT_ROOT"

echo "Airflow environment activated"
echo "AIRFLOW_HOME=$AIRFLOW_HOME"
echo "PYTHONPATH=$PYTHONPATH"
