import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PHASE1_ROOT = Path(__file__).parent


DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DATABASE_DIR = DATA_DIR / "database"


for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, DATABASE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


DATASET_NAME = "ManikaSaini/zomato-restaurant-recommendation"
DATASET_SPLIT = "train"  # Default split to load


DATABASE_PATH = DATABASE_DIR / "zomato.db"
DATABASE_TABLE_NAME = "restaurants"


REQUIRED_COLUMNS = [
    "name",
    "city",
    "cuisines",
    "average_cost_for_two",
    "aggregate_rating",
    "votes"
]


PRICE_CATEGORIES = {
    "budget": (0, 500),
    "mid-range": (500, 1500),
    "premium": (1500, float('inf'))
}


MIN_VOTES_THRESHOLD = 10  
MIN_RATING = 0.0
MAX_RATING = 5.0

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
