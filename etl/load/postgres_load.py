"""
Script loading transformed dataframes into the  local database
"""



# Imports
import sys
import os
import pandas as pd
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.dialects.postgresql import insert
from utils.logger import get_logger
from dotenv import load_dotenv


# Primary keys for each table in 'public' schema
PRIMARY_KEYS = {
    "clients":          "client_id",
    "client_addresses": "address_id",
    "products":         "product_id",
    "orders":           "order_id",
    "order_items":      "order_item_id",
}



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
            if_exists = "replace",
            index = False
        )

        logger.info("Table loading successfully completed '%s': %s", schema_name, table_name)

    except Exception as e:
        logger.error("Error while loading data into table %s: %s", table_name, e)
        sys.exit(1)





# Upserting a pandas DataFrame into a specific table in the PostgreSQL database
def upsert_dataframe_to_postgres(df: pd.DataFrame, table_name: str, engine, schema_name: str) -> None:
    pk = PRIMARY_KEYS.get(table_name)
    if not pk:
        logger.error("No primary key defined for table '%s'. Skipping upsert.", table_name)
        sys.exit(1)

    try:
        logger.info("Started upserting %s rows into '%s.%s'", len(df), schema_name, table_name)

        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine, schema=schema_name)

        records = df.to_dict(orient = "records")

        update_columns = {col: table.c[col] for col in df.columns if col != pk}

        with engine.begin() as conn:
            stmt = insert(table).values(records)
            stmt = stmt.on_conflict_do_update(
                index_elements = [pk],
                set_ = {col: stmt.excluded[col] for col in update_columns}
            )
            conn.execute(stmt)

        logger.info("Upsert completed successfully for '%s.%s'", schema_name, table_name)

    except Exception as e:
        logger.error("Error while upserting data into table '%s': %s", table_name, e)
        sys.exit(1)