# Imports
from pathlib import Path



# Creating the paths for files
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

DATA_DIR.mkdir(exist_ok = True)
LOGS_DIR.mkdir(exist_ok = True)