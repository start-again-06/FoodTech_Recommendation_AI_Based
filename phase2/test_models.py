import unittest
from phase2.models import UserInput
from pydantic import ValidationError

class TestModels(unittest.TestCase):
    
    def test_valid_input(self):
       
        data = {
            "city": "Mumbai",
            "price_range": "budget",
            "cuisine": "Italian",
            "min_rating": 4.0
        }
        user_input = UserInput(**data)
        self.assertEqual(user_input.city, "Mumbai")
        self.assertEqual(user_input.price_range, "budget")
        self.assertEqual(user_input.cuisine, "Italian")
        self.assertEqual(user_input.min_rating, 4.0)

    def test_city_normalization(self):
       
        user_input = UserInput(city="  bangalore  ", price_range="mid-range")
        self.assertEqual(user_input.city, "Bangalore")

    def test_invalid_price_range(self):
       
        data = {"city": "Delhi", "price_range": "expensive"}
        with self.assertRaises(ValidationError):
            UserInput(**data)

    def test_invalid_rating_range(self):
        
        with self.assertRaises(ValidationError):
            UserInput(city="Delhi", price_range="budget", min_rating=6.0)
        with self.assertRaises(ValidationError):
            UserInput(city="Delhi", price_range="budget", min_rating=-1.0)

    def test_empty_city(self):
       
        with self.assertRaises(ValidationError):
            UserInput(city="", price_range="budget")

if __name__ == "__main__":
    unittest.main()
