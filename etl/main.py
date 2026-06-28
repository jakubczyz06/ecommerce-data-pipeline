"""
Main orchestration script for the ETL process
"""



# Imports
import sys
from utils.logger import get_logger

# Extract
from etl.extract.extract_csv import extract_csv

# Transform
from etl.transform.clients import transform_clients
from etl.transform.client_addresses import transform_client_addresses
from etl.transform.products import transform_products
from etl.transform.orders import transform_orders
from etl.transform.order_items import transform_order_items

# Load
from etl.load.postgres_load import get_db_engine, load_dataframe_to_postgres, upsert_dataframe_to_postgres



# Setting up the logger
logger = get_logger("main_etl")





def main():
    logger.info("Starting the ETL pipeline...")


    engine = get_db_engine()


    logger.info("Extracting CSVs")
    raw_dataframes = extract_csv()
    if not raw_dataframes:
        logger.error("No data extracted. Terminating ETL.")
        sys.exit(1)


    logger.info("Loading to 'raw' schema")
    for table_name, df in raw_dataframes.items():
        df_raw = df.astype(str)
        load_dataframe_to_postgres(df_raw, table_name, engine, schema_name = "raw")


    logger.info("Transforming data")
    clean_dataframes = {}
    try:
        if "clients" in raw_dataframes:
            clean_dataframes["clients"] = transform_clients(raw_dataframes["clients"])

        if "client_addresses" in raw_dataframes:
            clean_dataframes["client_addresses"] = transform_client_addresses(raw_dataframes["client_addresses"])

        if "products" in raw_dataframes:
            clean_dataframes["products"] = transform_products(raw_dataframes["products"])

        if "orders" in raw_dataframes:
            clean_dataframes["orders"] = transform_orders(raw_dataframes["orders"])

        if "order_items" in raw_dataframes:
            clean_dataframes["order_items"] = transform_order_items(raw_dataframes["order_items"])
    except Exception as e:
        logger.error("Error during transformation: %s", e)
        sys.exit(1)


    logger.info("Loading to 'public' schema (upsert)")
    tables_order = [
        "clients",
        "client_addresses",
        "products",
        "orders",
        "order_items"
    ]
    for table in tables_order:
        if table in clean_dataframes:
            upsert_dataframe_to_postgres(clean_dataframes[table], table, engine, schema_name = "public")


    logger.info("ETL pipeline successfully finished.")





if __name__ == "__main__":
    main()