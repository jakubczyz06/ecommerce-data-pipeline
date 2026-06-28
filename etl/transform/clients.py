"""
Script transforming data for "clients" table
"""



# Imports
import pandas as pd
from utils.logger import get_logger



# Setting up the logger
logger = get_logger("transform_etl")





# Function transforming data with pandas
def transform_clients(df: pd.DataFrame) -> pd.DataFrame:

    logger.info("Transforming 'clients' dataframe - %s rows", len(df))

    # Casting types
    df["client_id"] = df["client_id"].astype(int)
    df["registration_date"] = pd.to_datetime(df["registration_date"])

    # Standardizing
    df["full_name"] = df["full_name"].astype(str).rstrip().title()
    df["gender"] = df["gender"].astype(str).strip().capitalize()
    df["phone_number"] = df["phone_number"].astype(str).rstrip()
    df["email"] = df["email"].astype(str).strip()

    # Male/Female -> M/F
    gender_mapping = {
        "Male": "M",
        "M": "M",
        "Female": "F",
        "F": "F",
    }
    df["gender"] = df["gender"].map(gender_mapping)


    # Deleting duplicates
    df = df.drop_duplicates(subset = "client_id")

    # Checking for NULLs
    critical = ["client_id", "full_name", "email", "registration_date"]
    nulls = df[critical].isnull().sum()
    if nulls.any():
        logger.warning("NULLs found in 'clients' \n%s", nulls[nulls > 0])


    logger.info("Transforming 'clients' table dataframe - %s rows", len(df))
    return df
