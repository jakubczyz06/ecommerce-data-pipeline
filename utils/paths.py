from pathlib import Path

# utils/paths.py jest w:  ecommerce_web_app/utils/paths.py
# parents[0] = utils/
# parents[1] = ecommerce_web_app/   ← PROJECT_ROOT
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)