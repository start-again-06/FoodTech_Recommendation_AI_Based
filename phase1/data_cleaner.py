import logging
from typing import List, Dict, Any
from collections import Counter

from phase1.config import MIN_RATING, MAX_RATING

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCleaner:
    
    def __init__(self, data: List[Dict[str, Any]]):
        
        self.data = [dict(item) for item in data]  # Deep copy
        self.original_count = len(self.data)
        self.cleaning_report = {
            "original_records": self.original_count,
            "duplicates_removed": 0,
            "missing_values_handled": 0,
            "invalid_records_removed": 0,
            "final_records": 0
        }
    
    def remove_duplicates(self) -> List[Dict[str, Any]]:
        
        logger.info("Removing duplicates...")
        initial_count = len(self.data)
        
       
        seen = set()
        unique_data = []
        
        for item in self.data:
           
            name = item.get('name', '')
            city = item.get('city', '')
            key = (str(name).strip().lower(), str(city).strip().lower())
            
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        self.data = unique_data
        duplicates_removed = initial_count - len(self.data)
        self.cleaning_report["duplicates_removed"] = duplicates_removed
        logger.info(f"Removed {duplicates_removed} duplicate records")
        
        return self.data
    
    def handle_missing_values(self) -> List[Dict[str, Any]]:
        
        logger.info("Handling missing values...")
        initial_missing: int = 0
        cleaned_data: List[Dict[str, Any]] = []
        
        for item in self.data:
            
            if not item.get('name') or not item.get('city'):
                initial_missing = initial_missing + 1
                continue
            
            
            if not item.get('cuisines'):
                item['cuisines'] = 'Unknown'
            
           
            if not item.get('aggregate_rating'):
                item['aggregate_rating'] = 0
            
            
            if not item.get('votes'):
                item['votes'] = 0
            
           
            if not item.get('average_cost_for_two'):
                # Use a default value
                item['average_cost_for_two'] = 500
            
            cleaned_data.append(item)
        
        self.data = cleaned_data
        self.cleaning_report["missing_values_handled"] = initial_missing
        logger.info(f"Handled {initial_missing} records with missing critical values")
        
        return self.data
    
    def standardize_text_fields(self) -> List[Dict[str, Any]]:
        
        logger.info("Standardizing text fields...")
        
        for item in self.data:
           
            if item.get('city'):
                item['city'] = str(item['city']).strip().title()
            

            if item.get('name'):
                item['name'] = str(item['name']).strip()
            
            
            if item.get('cuisines'):
                item['cuisines'] = str(item['cuisines']).strip()
        
        logger.info("Text fields standardized")
        return self.data
    
    def remove_invalid_entries(self) -> List[Dict[str, Any]]:
        
        logger.info("Removing invalid entries and parsing numeric strings...")
        initial_count = len(self.data)
        valid_data = []
        
        for item in self.data:
            try:
                
                rating_raw = item.get('aggregate_rating')
                rating = 0.0
                if rating_raw and isinstance(rating_raw, str):
                    if '/' in rating_raw:
                        rating_part = rating_raw.split('/')[0].strip()
                        rating = float(rating_part) if rating_part.replace('.', '', 1).isdigit() else 0.0
                    elif rating_raw.replace('.', '', 1).isdigit():
                        rating = float(rating_raw)
                    else:
                        rating = 0.0
                elif rating_raw is not None:
                    rating = float(rating_raw)
                
                
                item['aggregate_rating'] = rating
                
                
                cost_raw = item.get('average_cost_for_two')
                cost = 0.0
                if cost_raw and isinstance(cost_raw, str):
                    cost_clean = cost_raw.replace(',', '').strip()
                    cost = float(cost_clean) if cost_clean.replace('.', '', 1).isdigit() else 0.0
                elif cost_raw is not None:
                    cost = float(cost_raw)
                
                item['average_cost_for_two'] = cost
                
                
                votes_raw = item.get('votes', 0)
                votes = int(str(votes_raw).replace(',', '')) if votes_raw else 0
                item['votes'] = votes
                
                
                if rating < MIN_RATING or rating > MAX_RATING:
                    continue
                
                if cost < 0:
                    continue
                
                if votes < 0:
                    continue
                
                valid_data.append(item)
            except (ValueError, TypeError):
                continue
        
        invalid_removed = initial_count - len(valid_data)
        self.data = valid_data
        self.cleaning_report["invalid_records_removed"] = invalid_removed
        logger.info(f"Removed {invalid_removed} invalid or null records after numeric parsing")
        
        return self.data
    
    def clean(self) -> List[Dict[str, Any]]:
        
        logger.info("Starting data cleaning pipeline...")
        logger.info(f"Original dataset size: {self.original_count}")
        
       
        self.remove_duplicates()
        self.handle_missing_values()
        self.standardize_text_fields()
        self.remove_invalid_entries()
        
        
        self.cleaning_report["final_records"] = len(self.data)
        
        logger.info(f"Cleaning complete. Final dataset size: {len(self.data)}")
        logger.info(f"Cleaning report: {self.cleaning_report}")
        
        return self.data
    
    def get_cleaning_report(self) -> dict:
        
        return self.cleaning_report


def main():
    
    pass


if __name__ == "__main__":
    main()
