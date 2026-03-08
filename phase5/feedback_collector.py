import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class FeedbackCollector:
    
    def __init__(self, feedback_file: str = "data/feedback/user_feedback.json"):
        self.feedback_file = feedback_file
        self._ensure_storage()

    def _ensure_storage(self):
       
        os.makedirs(os.path.dirname(self.feedback_file), exist_ok=True)
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'w') as f:
                json.dump([], f)

    def collect_feedback(self, restaurant_name: str, rating: int, comment: str = ""):
        
        feedback_entry = {
            "timestamp": datetime.now().isoformat(),
            "restaurant": restaurant_name,
            "rating": rating,
            "comment": comment
        }
        
        try:
            with open(self.feedback_file, 'r+') as f:
                data = json.load(f)
                data.append(feedback_entry)
                f.seek(0)
                json.dump(data, f, indent=4)
            logger.info(f"Feedback saved for {restaurant_name}")
        except Exception as e:
            logger.error(f"Failed to save feedback: {e}")
