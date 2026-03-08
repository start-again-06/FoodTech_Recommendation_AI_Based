from phase1.config import DATABASE_PATH

PRICE_CATEGORIES = {
    "budget": (0, 500),
    "mid-range": (500, 1500),
    "premium": (1500, float('inf'))
}


MIN_RATING = 0.0
MAX_RATING = 5.0
MAX_CITIES_SUGGESTIONS = 3
FUZZY_MATCH_THRESHOLD = 0.6

DEFAULT_TOP_N = 10
