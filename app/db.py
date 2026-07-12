"""
Script connecting the app to the database
"""



# Imports
import sys
import os
from sqlalchemy import create_engine
from utils.logger import get_logger
from dotenv import load_dotenv



# Setting up the logger
logger = get_logger("db_app")



# Loading environment variables from an .env file
load_dotenv()



# Creating an engine to the database
def get_db_engine():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        logger.error('Environment variable missing. Check your .env file')
        sys.exit(1)

    return create_engine(db_url)

engine = get_db_engine()