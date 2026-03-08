import unittest
from unittest.mock import MagicMock, patch
from phase2.models import UserInput
from phase3.models import RecommendationResponse, RestaurantRecommendation
from phase5.exporter import Exporter
from phase5.feedback_collector import FeedbackCollector
import os
import json

class TestPhase5Integration(unittest.TestCase):
    
    def setUp(self):
        self.test_export_dir = "data/test_exports"
        self.test_feedback_file = "data/test_feedback/test_feedback.json"
        self.exporter = Exporter(export_dir=self.test_export_dir)
        self.collector = FeedbackCollector(feedback_file=self.test_feedback_file)
        
        self.mock_recs = [
            RestaurantRecommendation(
                name="Integration Rest", city="Bangalore", address="123 Road", 
                cuisines="Cafe", average_cost=500, price_category="mid-range", 
                rating=4.5, votes=100, match_score=9.0
            )
        ]

    def tearDown(self):
       
        if os.path.exists(self.test_export_dir):
            for f in os.listdir(self.test_export_dir):
                os.remove(os.path.join(self.test_export_dir, f))
            os.rmdir(self.test_export_dir)
            
        if os.path.exists(self.test_feedback_file):
            os.remove(self.test_feedback_file)
            if os.path.exists(os.path.dirname(self.test_feedback_file)):
                os.rmdir(os.path.dirname(self.test_feedback_file))

    def test_export_and_collect_feedback(self):
        
        json_path = self.exporter.export_to_json(self.mock_recs, "test.json")
        self.assertTrue(os.path.exists(json_path))
        with open(json_path, 'r') as f:
            data = json.load(f)
            self.assertEqual(data[0]['name'], "Integration Rest")
            
        
        self.collector.collect_feedback("Integration Rest", 5, "Great place!")
        with open(self.test_feedback_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['restaurant'], "Integration Rest")
            self.assertEqual(data[0]['rating'], 5)

if __name__ == "__main__":
    unittest.main()
