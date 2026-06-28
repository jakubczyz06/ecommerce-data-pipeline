"""
Script loading transformed dataframes into the  local database
"""



# Imports
import sys
import os
import pandas as pd
from sqlalchemy import create_engine
from utils.logger import get_logger
from dotenv import load_dotenv



# Setting up the logger
logger = get_logger("load_etl")



# Loading environment variables from an .env file
load_dotenv()



# Creating an engine to the database
def get_db_engine():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        logger.error('Environment variable missing. Check your .env file')
        sys.exit(1)

    return create_engine(db_url)





# Loading a pandas DataFrame into a specific table in the PostgreSQL database
def load_dataframe_to_postgres(df: pd.DataFrame, table_name: str, engine, schema_name: str) -> None:
    try:
        logger.info("Started loading %s rows into '%s' table: %s", len(df), schema_name, table_name)

        df.to_sql(
            name = table_name,
            con = engine,
            schema = schema_name,
            if_exists = "append",
            index = False
        )

        logger.info("Table loading successfully completed '%s': %s", schema_name, table_name)

    except Exception as e:
        logger.error("Error while loading data into table %s: %s", table_name, e)
        sys.exit(1)