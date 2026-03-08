import unittest
from unittest.mock import MagicMock, patch
from phase2.models import UserInput
from phase4.recommender import LLMRecommender
from phase3.models import RecommendationResponse, RestaurantRecommendation

class TestLLMRecommender(unittest.TestCase):
    
    def setUp(self):
        self.mock_groq = MagicMock()
        self.mock_engine = MagicMock()
        self.recommender = LLMRecommender(groq_client=self.mock_groq, engine=self.mock_engine)

    def test_get_reasoned_recommendations_success(self):
        
        user_input = UserInput(city="Whitefield", price_range="mid-range", cuisine="Cafe", min_rating=3.0)
        
        
        mock_rec = RestaurantRecommendation(
            name="Test Cafe", city="Whitefield", address="123 St", cuisines="Cafe",
            average_cost=500, price_category="mid-range", rating=4.5, votes=100, match_score=9.5
        )
        self.mock_engine.get_recommendations.return_value = RecommendationResponse(
            user_city="Whitefield", count=1, recommendations=[mock_rec]
        )
        
        
        self.mock_groq.get_completion.return_value = "AI Reasoned Recommendation Text"
        
        result = self.recommender.get_reasoned_recommendations(user_input)
        
        self.assertEqual(result, "AI Reasoned Recommendation Text")
        self.mock_groq.get_completion.assert_called_once()
        self.mock_engine.get_recommendations.assert_called_once_with(user_input, limit=5)

    def test_get_reasoned_recommendations_no_results(self):
       
        user_input = UserInput(city="Unknown", price_range="budget", min_rating=0.0)
        
        self.mock_engine.get_recommendations.return_value = RecommendationResponse(
            user_city="Unknown", count=0, recommendations=[]
        )
        
        result = self.recommender.get_reasoned_recommendations(user_input)
        
        self.assertIn("couldn't find any restaurants", result)
        self.mock_groq.get_completion.assert_not_called()

if __name__ == "__main__":
    unittest.main()
