import logging
import math
from typing import Dict, List, Any

from phase1.config import PRICE_CATEGORIES, MIN_VOTES_THRESHOLD


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureEngineer:
  
    def __init__(self, data: List[Dict[str, Any]]):
      
        self.data = data
    
    def create_price_category(self) -> List[Dict[str, Any]]:
       
        logger.info("Creating price category feature...")
        
        for item in self.data:
            try:
                cost = float(item.get('average_cost_for_two', 0))
                
               
                category = 'premium'  # Default
                for cat_name, (min_price, max_price) in PRICE_CATEGORIES.items():
                    if min_price <= cost < max_price:
                        category = cat_name
                        break
                
                item['price_category'] = category
            except (ValueError, TypeError):
                item['price_category'] = 'unknown'
        
        
        categories = [item.get('price_category') for item in self.data]
        from collections import Counter
        distribution = Counter(categories)
        logger.info(f"Price category distribution: {dict(distribution)}")
        
        return self.data
    
    def create_popularity_score(self) -> List[Dict[str, Any]]:
       
        logger.info("Creating popularity score feature...")
        
        
        max_votes = max((int(item.get('votes', 0)) for item in self.data), default=1)
        
        for item in self.data:
            try:
                rating = float(item.get('aggregate_rating', 0))
                votes = int(item.get('votes', 0))
                
               
                normalized_rating = rating / 5.0
                
                
                if max_votes > 0:
                    normalized_votes = math.log1p(votes) / math.log1p(max_votes)
                else:
                    normalized_votes = 0
                
                
                popularity = (0.7 * normalized_rating) + (0.3 * normalized_votes)
                item['popularity_score'] = round(popularity, 4)
                
            except (ValueError, TypeError):
                item['popularity_score'] = 0.0
        
        logger.info("Popularity score created")
        return self.data
    
    def create_cuisine_diversity_index(self) -> List[Dict[str, Any]]:
       
        logger.info("Creating cuisine diversity index...")
        
        for item in self.data:
            cuisines_str = item.get('cuisines', '')
            
            if not cuisines_str or cuisines_str == 'Unknown':
                item['cuisine_diversity'] = 0
            else:
               
                cuisines_list = [c.strip() for c in str(cuisines_str).split(',') if c.strip()]
                item['cuisine_diversity'] = len(cuisines_list)
        
        logger.info("Cuisine diversity index created")
        return self.data
    
    def create_has_online_delivery(self) -> List[Dict[str, Any]]:
        
        logger.info("Creating online delivery feature...")
        
        for item in self.data:
            online_order = str(item.get('online_order', '')).lower()
            item['has_online_delivery'] = 1 if online_order in ['yes', 'true', '1'] else 0
        
        count = sum(item.get('has_online_delivery', 0) for item in self.data)
        logger.info(f"Restaurants with online delivery: {count}/{len(self.data)}")
        
        return self.data
    
    def create_has_table_booking(self) -> List[Dict[str, Any]]:
       
        logger.info("Creating table booking feature...")
        
        for item in self.data:
            book_table = str(item.get('book_table', '')).lower()
            item['has_table_booking'] = 1 if book_table in ['yes', 'true', '1'] else 0
        
        count = sum(item.get('has_table_booking', 0) for item in self.data)
        logger.info(f"Restaurants with table booking: {count}/{len(self.data)}")
        
        return self.data
    
    def create_is_popular(self) -> List[Dict[str, Any]]:
        
        logger.info("Creating is_popular feature...")
        
        for item in self.data:
            try:
                votes = int(item.get('votes', 0))
                item['is_popular'] = 1 if votes >= MIN_VOTES_THRESHOLD else 0
            except (ValueError, TypeError):
                item['is_popular'] = 0
        
        count = sum(item.get('is_popular', 0) for item in self.data)
        logger.info(f"Popular restaurants: {count}/{len(self.data)}")
        
        return self.data
    
    def engineer_features(self) -> List[Dict[str, Any]]:
        
        logger.info("Starting feature engineering pipeline...")
        logger.info(f"Input dataset size: {len(self.data)}")
        
   
        self.create_price_category()
        self.create_popularity_score()
        self.create_cuisine_diversity_index()
        self.create_has_online_delivery()
        self.create_has_table_booking()
        self.create_is_popular()
        
        logger.info(f"Feature engineering complete. Final dataset size: {len(self.data)}")
        
        return self.data
    
    def get_feature_summary(self) -> Dict:
        
        from collections import Counter
        
        summary = {}
        
       
        if self.data and 'price_category' in self.data[0]:
            categories = [item.get('price_category') for item in self.data]
            summary['price_category'] = dict(Counter(categories))
        
        
        if self.data and 'popularity_score' in self.data[0]:
            scores = [item.get('popularity_score', 0) for item in self.data]
            summary['popularity_score'] = {
                'min': min(scores) if scores else 0,
                'max': max(scores) if scores else 0,
                'avg': sum(scores) / len(scores) if scores else 0
            }
    
        if self.data and 'cuisine_diversity' in self.data[0]:
            diversities = [item.get('cuisine_diversity', 0) for item in self.data]
            summary['cuisine_diversity'] = {
                'min': min(diversities) if diversities else 0,
                'max': max(diversities) if diversities else 0,
                'avg': sum(diversities) / len(diversities) if diversities else 0
            }
        
        return summary


def main():
   
    pass


if __name__ == "__main__":
    main()
