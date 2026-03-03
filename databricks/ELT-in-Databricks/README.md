# Fraud Analytics Pipeline on Azure Databricks

This project builds an end-to-end Fraud Analytics **ELT Pipeline** using Microsoft Azure and Azure Databricks, following the Medallion Architecture (Bronze → Silver → Gold).

The solution covers:

- Multi-source data ingestion (SQL + JSON + Cloud Storage)

- ELT pipeline implementation in Databricks

- Workflow orchestration using Databricks Jobs

- Analytical dashboard built in Databricks SQL(screenshot: `Fraud-Analytics-Dashboard.jpg`)

The objective is to transform raw financial transaction data into a structured fraud analytics warehouse and create actionable fraud insights.

## Architecture

![Architecture Diagram](./ELT-pipeline.png)

## Data Ingestion

1. Importing `transactions_data.csv` and `cards_data.csv` into **Azure SQL Database** (using Azure Data Studio to connect to SQL Server and importing data via import wizard)

2. Using **JDBC** to ingest `transactions_data.csv` from Azure Sql DB to Databricks

3. Using **Lakeflow Connect** to connect Databricks to Azure SQL Database for `cards_data.csv`

4. Uploading files(`users_data.csv`, `mcc_codes.json`, `train_fraud_labels.json`) in Azure Data Lake Storage, then creating **External Location** in Unity Catalog, to read directly from cloud storage(storage credential in UC was created to give grant permission to externa; location + config IAM roles in ADLS)

5. Using Azure Data Factory to move `mcc_codes.json` and `train_fraud_labels.json` into Databricks Delta tables.

## Implementation
This project implements a Medallion Architecture in Databricks:

- Bronze Layer: Raw data ingested from Azure SQL and ADLS, stored as Delta tables with minimal transformation.

- Silver Layer: Cleaned and enriched data by casting types, joining transaction, user, card, MCC, and fraud label datasets into a unified transactional model.

- Gold Layer: Aggregated analytics tables built for reporting, including fraud trends, financial losses, user risk metrics, and behavioral insights.

This layered approach ensures data quality, scalability, and clear separation between raw data and business-ready analytics.

## Job Orchestration

A Databricks Job was created to orchestrate the full pipeline. Task flow: Bronze Notebook -> Silver Notebook -> Gold Notebook. The dashboard automatically reflects updated data after Gold tables refresh.

## Future Improvements

- Add streaming ingestion
- Implement Delta Live Tables (DLT)
- Add data quality checks