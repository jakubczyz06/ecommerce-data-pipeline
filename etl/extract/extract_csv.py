"""
Script extracting CSV files.
"""



# Imports
import pandas as pd
from utils.logger import get_logger
from utils.paths import DATA_DIR



# Setting up the logger
logger = get_logger("extract_etl")



# Subdirectory for generated files
GENERATED_DIR = DATA_DIR / "generated"





# Extracting all CSV files from "generated_data" directory
def extract_csv() -> dict[str, pd.DataFrame]:
    dataframes = {}

    for file in GENERATED_DIR.glob("*.csv"):
        table_name = file.stem
        dataframes[table_name] = pd.read_csv(file)
        logger.info("Extracted %s - %s rows", table_name, len(dataframes[table_name]))

    return dataframes






