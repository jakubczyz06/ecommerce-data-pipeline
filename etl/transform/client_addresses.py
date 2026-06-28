"""
Script transforming data for "client_addresses" table
"""



# Imports
import pandas as pd
from utils.logger import get_logger



# Setting up the logger
logger = get_logger("transform_etl")




# Function transforming data with pandas
def transform_client_addresses(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transforming 'client addresses' dataframe - %s rows", len(df))

    # Casting types
    df["address_id"] = df["address_id"].astype(int)
    df["client_id"] = df["client_id"].astype(int)

    # Standardizing
    df["country"] = df["country"].astype(str).str.strip().str.title()
    df["state"] = df["state"].astype(str).str.strip().str.upper()
    df["city"] = df["city"].astype(str).str.strip().str.title()
    df["postal_code"] = df["postal_code"].astype(str).str.strip()
    df["street"] = df["street"].astype(str).str.strip()
    df["building_number"] = df["building_number"].astype(str).str.strip()
    df["apartment_number"] = df["apartment_number"].astype(str).str.strip().replace("nan", None)
    df["address_type"] = df["address_type"].astype(str).str.strip()

    # Deleting duplicates
    df = df.drop_duplicates(subset="address_id")

    # Checking for NULLs
    critical = ["client_id", "address_id"]
    nulls = df[critical].isnull().sum()
    if nulls.any():
        logger.warning("NULLs found in 'client_addresses' \n%s", nulls[nulls > 0])

    logger.info("Transforming 'client_addresses' dataframe - %s rows", len(df))
    return df
