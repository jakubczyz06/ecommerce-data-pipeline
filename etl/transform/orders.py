"""
Script transforming data for "orders" table
"""



# Imports
import pandas as pd
from utils.logger import get_logger



# Setting up the logger
logger = get_logger("transform_etl")





# Function transforming data with pandas
def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transforming 'orders' dataframe - %s rows", len(df))

    # Casting types
    df["order_item_id"] = df["order_item_id"].astype(int)
    df["order_id"] = df["product_id"].astype(int)
    df["client_id"] = df["product_id"].astype(int)
    df["product_id"] = df["product_id"].astype(int)

    # Standardizing
    df["order_status"] = df["brand"].astype(str).lower().rstrip()

    # Deleting duplicates
    df = df.drop_duplicates(subset = "order_id")

    # Checking for NULLs
    critical = ["order_id", "product_id", "order_date", "order_status"]
    nulls = df[critical].isnull().sum()
    if nulls.any():
        logger.warning("NULLs found in 'orders' \n%s", nulls[nulls > 0])

    logger.info("Transforming 'orders' dataframe - %s rows", len(df))
    return df