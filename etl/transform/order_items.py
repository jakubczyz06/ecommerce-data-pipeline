"""
Script transforming data for "order_items" table
"""



# Imports
import pandas as pd
from utils.logger import get_logger



# Setting up the logger
logger = get_logger("transform_etl")





# Function transforming data with pandas
def transform_order_items(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transforming 'order_items' dataframe - %s rows", len(df))

    # Casting types
    df["order_item_id"] = df["order_item_id"].astype(int)
    df["order_id"] = df["order_id"].astype(int)
    df["product_id"] = df["product_id"].astype(int)
    df["quantity"] = df["quantity"].astype(int)

    # Standardizing
    df["unit_price"] = df["unit_price"].astype(float).round(2)

    # Deleting duplicates
    df = df.drop_duplicates(subset = "order_item_id")

    # Checking for NULLs
    critical = ["order_item_id", "order_id", "product_id", "quantity", "unit_price"]
    nulls = df[critical].isnull().sum()
    if nulls.any():
        logger.warning("NULLs found in 'order_items' \n%s", nulls[nulls > 0])

    logger.info("Transforming 'order_items' dataframe - %s rows", len(df))
    return df