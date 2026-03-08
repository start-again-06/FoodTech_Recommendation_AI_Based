import unittest
from unittest.mock import MagicMock, patch
from phase2.models import UserInput
from phase3.recommender import RecommendationEngine
from phase3.models import RecommendationResponse

class TestRecommendationEngine(unittest.TestCase):
    
    def setUp(self):
        self.mock_db = MagicMock()
        self.mock_db.table_name = "restaurants"
        self.recommender = RecommendationEngine(db_manager=self.mock_db)

    def test_calculate_match_score_exact_cuisine(self):
        
        user_input = UserInput(city="Mumbai", price_range="budget", cuisine="Italian", min_rating=0.0)
        
        score = self.recommender._calculate_match_score(5.0, 1000, user_input, "Pizza, Italian, Pasta")
        self.assertEqual(score, 10.0)

    def test_calculate_match_score_no_cuisine_match(self):
        
        user_input = UserInput(city="Mumbai", price_range="budget", cuisine="Indonesian", min_rating=0.0)
        
       
        score = self.recommender._calculate_match_score(4.0, 500, user_input, "Pizza, Italian, Pasta")
        self.assertEqual(score, 7.1)

    def test_get_recommendations_success(self):
       
        user_input = UserInput(city="Indiranagar", price_range="mid-range", cuisine="Cafe", min_rating=3.0)
        
        
        self.mock_db.connection.cursor.return_value.fetchall.return_value = [
            ("Cafe Blue", "Indiranagar", "123 Street", "Cafe, Bakery", 800, "mid-range", 4.5, 500),
            ("Coffee House", "Indiranagar", "456 Avenue", "Cafe, Desserts", 600, "mid-range", 4.0, 200)
        ]
        
        response = self.recommender.get_recommendations(user_input, limit=5)
        
        self.assertIsInstance(response, RecommendationResponse)
        self.assertEqual(response.count, 2)
        self.assertEqual(response.recommendations[0].name, "Cafe Blue")
        self.assertTrue(response.recommendations[0].match_score > response.recommendations[1].match_score)

    def test_get_recommendations_no_results(self):
       
        user_input = UserInput(city="Nonexistent", price_range="premium", cuisine=None, min_rating=0.0)
        self.mock_db.connection.cursor.return_value.fetchall.return_value = []
        
        response = self.recommender.get_recommendations(user_input)
        self.assertEqual(response.count, 0)
        self.assertEqual(len(response.recommendations), 0)

if __name__ == '__main__':
    unittest.main()
