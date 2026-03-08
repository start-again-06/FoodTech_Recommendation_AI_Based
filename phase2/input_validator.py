import logging
from typing import List, Optional, Tuple, Dict, Any
import difflib

from phase1.database_setup import DatabaseManager
from phase2.models import UserInput
from phase2.config import FUZZY_MATCH_THRESHOLD, MAX_CITIES_SUGGESTIONS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InputValidator:
   
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
       
        self.db_manager = db_manager or DatabaseManager()
        self.available_cities: List[str] = []
        self.available_cuisines: List[str] = []
        self._refresh_data()
        
    def _refresh_data(self):
       
        try:
            self.db_manager.connect()
            self.available_cities = self.db_manager.get_cities()
            self.available_cuisines = self.db_manager.get_cuisines()
            self.db_manager.close()
            logger.info(f"Loaded {len(self.available_cities)} cities and {len(self.available_cuisines)} cuisines from database")
        except Exception as e:
            logger.error(f"Failed to load data from database: {e}")
            self.available_cities = []
            self.available_cuisines = []
            
    def get_valid_localities(self) -> List[str]:
       
        return self.available_cities

    def get_valid_cuisines(self) -> List[str]:
        
        return self.available_cuisines
            
    def validate_city(self, city: str) -> Tuple[bool, Optional[str], List[str]]:
        
        city_clean = city.strip().title()
        
       
        if city_clean in self.available_cities:
            return True, city_clean, []
            
       
        suggestions = difflib.get_close_matches(
            city_clean, 
            self.available_cities, 
            n=MAX_CITIES_SUGGESTIONS, 
            cutoff=FUZZY_MATCH_THRESHOLD
        )
        
        return False, None, suggestions
        
    def validate_user_input(self, data: Dict[str, Any]) -> Tuple[Optional[UserInput], Optional[str]]:
       
        try:
           
            user_input = UserInput(**data)
            
           
            is_valid, matched_city, suggestions = self.validate_city(user_input.city)
            
            if not is_valid:
                error_msg = f"City '{user_input.city}' not found in database."
                if suggestions:
                    error_msg += f" Did you mean: {', '.join(suggestions)}?"
                return None, error_msg
                
            
            user_input.city = matched_city
            
            return user_input, None
            
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            logger.error(f"Unexpected validation error: {e}")
            return None, "An unexpected error occurred during validation."
