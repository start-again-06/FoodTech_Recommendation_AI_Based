import unittest
from phase1.data_cleaner import DataCleaner
class TestDataCleaner(unittest.TestCase):
       
    def setUp(self):
        
        self.sample_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian, Chinese', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
            {'name': 'Restaurant B', 'city': 'delhi', 'cuisines': 'Indian', 'average_cost_for_two': 1000, 'aggregate_rating': 3.8, 'votes': 50},
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian, Chinese', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},  # Duplicate
            {'name': 'Restaurant C', 'city': 'Bangalore', 'cuisines': 'Mexican', 'average_cost_for_two': -100, 'aggregate_rating': 6.0, 'votes': 200},  # Invalid
            {'name': None, 'city': 'Chennai', 'cuisines': 'Thai', 'average_cost_for_two': 2000, 'aggregate_rating': 2.5, 'votes': -10}  # Missing name
        ]
    
    def test_remove_duplicates(self):
      
        cleaner = DataCleaner(self.sample_data)
        result = cleaner.remove_duplicates()
        
        self.assertLess(len(result), len(self.sample_data))
        
        self.assertGreater(cleaner.cleaning_report['duplicates_removed'], 0)
    
    def test_handle_missing_values(self):
        
        cleaner = DataCleaner(self.sample_data)
        result = cleaner.handle_missing_values()
        
        for item in result:
            self.assertIsNotNone(item.get('name'))
            self.assertTrue(item.get('name'))
    
    def test_standardize_text_fields(self):
        
        cleaner = DataCleaner(self.sample_data)
        result = cleaner.standardize_text_fields()
        
        cities = [item['city'] for item in result]
        self.assertIn('Delhi', cities)
        self.assertNotIn('delhi', cities)
    
    def test_remove_invalid_entries(self):
        
        cleaner = DataCleaner(self.sample_data)
        result = cleaner.remove_invalid_entries()
        
        
        for item in result:
            self.assertGreater(float(item.get('average_cost_for_two', 0)), 0)
        
        
        for item in result:
            rating = float(item.get('aggregate_rating', 0))
            self.assertLessEqual(rating, 5.0)
        
        
        for item in result:
            self.assertGreaterEqual(int(item.get('votes', 0)), 0)
    
    def test_complete_cleaning_pipeline(self):
        
        cleaner = DataCleaner(self.sample_data)
        result = cleaner.clean()
        
        
        self.assertIsInstance(result, list)
        
        
        self.assertLessEqual(len(result), len(self.sample_data))
        
        
        report = cleaner.get_cleaning_report()
        self.assertIn('original_records', report)
        self.assertIn('final_records', report)
    
    def test_cleaning_report(self):
        
        cleaner = DataCleaner(self.sample_data)
        cleaner.clean()
        report = cleaner.get_cleaning_report()
        
        self.assertIn('original_records', report)
        self.assertIn('duplicates_removed', report)
        self.assertIn('missing_values_handled', report)
        self.assertIn('invalid_records_removed', report)
        self.assertIn('final_records', report)


class TestDataCleanerEdgeCases(unittest.TestCase):
    
    
    def test_empty_list(self):
        
        empty_data = []
        cleaner = DataCleaner(empty_data)
        result = cleaner.clean()
        
        self.assertEqual(len(result), 0)
    
    def test_all_valid_data(self):
        
        clean_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
            {'name': 'Restaurant B', 'city': 'Delhi', 'cuisines': 'Indian', 'average_cost_for_two': 1000, 'aggregate_rating': 3.8, 'votes': 50}
        ]
        
        cleaner = DataCleaner(clean_data)
        result = cleaner.clean()
        
        
        self.assertEqual(len(result), len(clean_data))
    
    def test_all_duplicates(self):
        
        duplicate_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
        ]
        
        cleaner = DataCleaner(duplicate_data)
        result = cleaner.clean()
        
        
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
