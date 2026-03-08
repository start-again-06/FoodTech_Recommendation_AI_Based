import unittest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from phase6.api_server import app
import json

client = TestClient(app)

class TestAPI(unittest.TestCase):
    

    def test_root_endpoint(self):
        
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "active")

    @patch('phase6.api_server.LLMRecommender')
    def test_recommend_endpoint_success(self, mock_recommender_class):
       
        mock_recommender = MagicMock()
        mock_recommender_class.return_value = mock_recommender
        
        
        mock_engine_res = MagicMock()
        mock_engine_res.count = 1
        
        mock_rest = MagicMock()
        mock_rest.name = "API Test Rest"
        mock_rest.rating = 4.0
        mock_rest.votes = 50
        mock_rest.cuisines = "Testing"
        mock_rest.average_cost = 200
        mock_rest.address = "123 API St"
        
        mock_engine_res.recommendations = [mock_rest]
        mock_recommender.engine.get_recommendations.return_value = mock_engine_res
        
        mock_recommender.get_reasoned_recommendations.return_value = "AI Reasoning Summary"
        mock_recommender.get_individual_reasoning.return_value = "Why you'll like it: Granular"

        
        payload = {
            "city": "Bangalore",
            "price_range": "budget",
            "cuisine": "Testing",
            "min_rating": 3.0
        }
        
        response = client.post("/api/recommend", json=payload)
        
      
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["recommendations"][0]["name"], "API Test Rest")
        self.assertEqual(data["recommendations"][0]["reasoning"], "Why you'll like it: Granular")
        self.assertIn("AI Reasoning", data["ai_reasoning_summary"])

    @patch('phase6.api_server.FeedbackCollector')
    def test_feedback_endpoint_success(self, mock_collector_class):
        
        mock_collector = MagicMock()
        mock_collector_class.return_value = mock_collector
        
        payload = {
            "restaurant_name": "API Test Rest",
            "rating": 5,
            "comment": "Highly recommended!"
        }
        
        response = client.post("/api/feedback", json=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        mock_collector.collect_feedback.assert_called_once()

if __name__ == "__main__":
    unittest.main()
