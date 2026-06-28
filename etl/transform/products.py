"""
Script transforming data for "products" table
"""



# Imports
import pandas as pd
from utils.logger import get_logger



# Setting up the logger
logger = get_logger("transform_etl")





# Function transforming data with pandas
def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transforming 'products' dataframe - %s rows", len(df))

    # Casting types
    df["product_id"] = df["product_id"].astype(int)

    # Standardizing
    df["product_name"] = df["product_name"].astype(str).rstrip()
    df["brand"] = df["brand"].astype(str).title().rstrip()
    df["screen_size"] = df["screen_size"].str.strip()
    df["unit_price"] = df["unit_price"].astype(float).round(2)
    df["created_at"] = pd.to_datetime(df["created_at"])

    # Deleting duplicates
    df = df.drop_duplicates(subset = "product_id")

    # Checking for NULLs
    critical = ["product_id", "product_name", "unit_price", "created_at"]
    nulls = df[critical].isnull().sum()
    if nulls.any():
        logger.warning("NULLs found in 'products' \n%s", nulls[nulls > 0])

    logger.info("Transforming 'products' dataframe - %s rows", len(df))
    return df