import unittest

from phase1.feature_engineer import FeatureEngineer


class TestFeatureEngineer(unittest.TestCase):
       
    def setUp(self):
       
        self.sample_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian, Chinese', 'average_cost_for_two': 400, 'aggregate_rating': 4.5, 'votes': 1000, 'online_order': 'Yes', 'book_table': 'Yes'},
            {'name': 'Restaurant B', 'city': 'Delhi', 'cuisines': 'Indian', 'average_cost_for_two': 1200, 'aggregate_rating': 3.8, 'votes': 50, 'online_order': 'No', 'book_table': 'Yes'},
            {'name': 'Restaurant C', 'city': 'Bangalore', 'cuisines': 'Mexican, Thai, Japanese', 'average_cost_for_two': 2000, 'aggregate_rating': 4.2, 'votes': 500, 'online_order': 'Yes', 'book_table': 'No'}
        ]
    
    def test_create_price_category(self):
        
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_price_category()
        
        
        self.assertIn('price_category', result[0])
        
        
        self.assertEqual(result[0]['price_category'], 'budget')  # 400
        self.assertEqual(result[1]['price_category'], 'mid-range')  # 1200
        self.assertEqual(result[2]['price_category'], 'premium')  # 2000
    
    def test_create_popularity_score(self):
        
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_popularity_score()
        
       
        self.assertIn('popularity_score', result[0])
        
       
        for item in result:
            score = item['popularity_score']
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 1)
        
       
        scores = [item['popularity_score'] for item in result]
        max_score_idx = scores.index(max(scores))
        self.assertEqual(result[max_score_idx]['name'], 'Restaurant A')
    
    def test_create_cuisine_diversity_index(self):
        
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_cuisine_diversity_index()
        
        
        self.assertIn('cuisine_diversity', result[0])
        
     
        self.assertEqual(result[0]['cuisine_diversity'], 2)  # Italian, Chinese
        self.assertEqual(result[1]['cuisine_diversity'], 1)  # Indian
        self.assertEqual(result[2]['cuisine_diversity'], 3)  # Mexican, Thai, Japanese
    
    def test_create_has_online_delivery(self):
      
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_has_online_delivery()
        
        
        self.assertIn('has_online_delivery', result[0])
        

        self.assertEqual(result[0]['has_online_delivery'], 1)  # Yes
        self.assertEqual(result[1]['has_online_delivery'], 0)  # No
    
    def test_create_has_table_booking(self):
      
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_has_table_booking()
        
        
        self.assertIn('has_table_booking', result[0])
        
       
        self.assertEqual(result[0]['has_table_booking'], 1)  # Yes
        self.assertEqual(result[2]['has_table_booking'], 0)  # No
    
    def test_create_is_popular(self):
        
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.create_is_popular()
        
        
        self.assertIn('is_popular', result[0])
        
       
        self.assertEqual(result[0]['is_popular'], 1)
        self.assertEqual(result[2]['is_popular'], 1)
    
    def test_complete_feature_engineering_pipeline(self):
       
        engineer = FeatureEngineer(self.sample_data)
        result = engineer.engineer_features()
        
        
        expected_features = [
            'price_category',
            'popularity_score',
            'cuisine_diversity',
            'has_online_delivery',
            'has_table_booking',
            'is_popular'
        ]
        
        for feature in expected_features:
            self.assertIn(feature, result[0])
    
    def test_get_feature_summary(self):
       
        engineer = FeatureEngineer(self.sample_data)
        engineer.engineer_features()
        summary = engineer.get_feature_summary()
        
        
        self.assertIsInstance(summary, dict)
        self.assertIn('price_category', summary)
        self.assertIn('popularity_score', summary)


class TestFeatureEngineerEdgeCases(unittest.TestCase):
   
    
    def test_missing_columns(self):
      
        minimal_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai'}
        ]
        
        engineer = FeatureEngineer(minimal_data)
        result = engineer.engineer_features()
        
    
        self.assertIsInstance(result, list)
    
    def test_unknown_cuisines(self):
        
        data_with_unknown = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Unknown', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100},
            {'name': 'Restaurant B', 'city': 'Delhi', 'cuisines': None, 'average_cost_for_two': 1000, 'aggregate_rating': 3.8, 'votes': 50}
        ]
        
        engineer = FeatureEngineer(data_with_unknown)
        result = engineer.create_cuisine_diversity_index()
        
        
        self.assertEqual(result[0]['cuisine_diversity'], 0)
    
    def test_zero_votes(self):
        
        data_with_zero_votes = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 0}
        ]
        
        engineer = FeatureEngineer(data_with_zero_votes)
        result = engineer.create_popularity_score()
        
        self.assertIn('popularity_score', result[0])
        self.assertGreaterEqual(result[0]['popularity_score'], 0)


if __name__ == '__main__':
    unittest.main()
