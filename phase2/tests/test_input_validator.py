import unittest
from unittest.mock import MagicMock
from phase2.input_validator import InputValidator

class TestInputValidator(unittest.TestCase):
       
    def setUp(self):
        
        self.mock_db = MagicMock()
        
        self.mock_db.get_cities.return_value = ["Mumbai", "Bangalore", "Delhi", "Pune"]
        self.mock_db.get_cuisines.return_value = ["Italian", "Chinese", "Indian"]
        self.validator = InputValidator(db_manager=self.mock_db)

    def test_data_refresh(self):
       
        self.assertEqual(len(self.validator.available_cities), 4)
        self.assertEqual(len(self.validator.available_cuisines), 3)
        self.assertIn("Italian", self.validator.available_cuisines)

    def test_validate_city_exact(self):
       
        is_valid, matched, suggestions = self.validator.validate_city("Mumbai")
        self.assertTrue(is_valid)
        self.assertEqual(matched, "Mumbai")
        self.assertEqual(len(suggestions), 0)

    def test_validate_city_fuzzy(self):
       
        is_valid, matched, suggestions = self.validator.validate_city("Mumbay")
        self.assertFalse(is_valid)
        self.assertIsNone(matched)
        self.assertIn("Mumbai", suggestions)

    def test_validate_city_not_found(self):
     
        is_valid, matched, suggestions = self.validator.validate_city("Atlantis")
        self.assertFalse(is_valid)
        self.assertEqual(len(suggestions), 0)

    def test_validate_user_input_success(self):
       
        data = {"city": "Pune", "price_range": "mid-range"}
        user_input, error = self.validator.validate_user_input(data)
        self.assertIsNotNone(user_input)
        self.assertIsNone(error)
        self.assertEqual(user_input.city, "Pune")

    def test_validate_user_input_failure(self):
        
        data = {"city": "New York", "price_range": "budget"}
        user_input, error = self.validator.validate_user_input(data)
        self.assertIsNone(user_input)
        self.assertIsNotNone(error)
        self.assertIn("City 'New York' not found", error)

if __name__ == "__main__":
    unittest.main()
