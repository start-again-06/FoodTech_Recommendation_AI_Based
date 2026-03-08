import unittest
import sqlite3
from pathlib import Path
import tempfile
import os

from phase1.database_setup import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
   
    def setUp(self):
        
       
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db_path = Path(self.temp_db.name)
        self.temp_db.close()
        
        self.db_manager = DatabaseManager(db_path=self.temp_db_path)
        
       
        self.sample_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100, 'price_category': 'budget', 'popularity_score': 0.8, 'cuisine_diversity': 1, 'has_online_delivery': 1, 'has_table_booking': 1, 'is_popular': 1},
            {'name': 'Restaurant B', 'city': 'Delhi', 'cuisines': 'Indian', 'average_cost_for_two': 1000, 'aggregate_rating': 3.8, 'votes': 50, 'price_category': 'mid-range', 'popularity_score': 0.6, 'cuisine_diversity': 1, 'has_online_delivery': 0, 'has_table_booking': 1, 'is_popular': 1},
            {'name': 'Restaurant C', 'city': 'Mumbai', 'cuisines': 'Chinese', 'average_cost_for_two': 1500, 'aggregate_rating': 4.2, 'votes': 200, 'price_category': 'premium', 'popularity_score': 0.9, 'cuisine_diversity': 1, 'has_online_delivery': 1, 'has_table_booking': 0, 'is_popular': 1}
        ]
    
    def tearDown(self):
        
        if self.db_manager.connection:
            self.db_manager.close()
        

        if self.temp_db_path.exists():
            os.unlink(self.temp_db_path)
    
    def test_connect(self):
        
        connection = self.db_manager.connect()
        
       
        self.assertIsInstance(connection, sqlite3.Connection)
        self.assertIsNotNone(self.db_manager.connection)
    
    def test_create_table(self):
       
        self.db_manager.connect()
        self.db_manager.create_table()
        
        
        cursor = self.db_manager.connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (self.db_manager.table_name,)
        )
        result = cursor.fetchone()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], self.db_manager.table_name)
    
    def test_create_indexes(self):
       
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.create_indexes()
        
       
        cursor = self.db_manager.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        
        
        self.assertIn('idx_city', indexes)
        self.assertIn('idx_price', indexes)
        self.assertIn('idx_city_price', indexes)
    
    def test_insert_data(self):
        
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data, if_exists='replace')
        
        
        count = self.db_manager.get_record_count()
        self.assertEqual(count, len(self.sample_data))
    
    def test_get_record_count(self):
        
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        count = self.db_manager.get_record_count()
        self.assertEqual(count, 3)
    
    def test_get_cities(self):
       
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        cities = self.db_manager.get_cities()
        
        
        self.assertIn('Mumbai', cities)
        self.assertIn('Delhi', cities)
        self.assertEqual(len(cities), 2)  # Mumbai and Delhi
    
    def test_get_sample_data(self):
        """
        Test getting sample data
        """
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        sample = self.db_manager.get_sample_data(limit=2)
        
     
        self.assertIsInstance(sample, list)
        self.assertEqual(len(sample), 2)
    
    def test_query_by_city(self):

        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        mumbai_restaurants = self.db_manager.query_by_city('Mumbai')
        
       
        self.assertEqual(len(mumbai_restaurants), 2)
        for restaurant in mumbai_restaurants:
            self.assertEqual(restaurant['city'], 'Mumbai')
    
    def test_query_by_city_and_price(self):
        
        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        results = self.db_manager.query_by_city_and_price('Mumbai', 'budget')
        
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Restaurant A')
    
    def test_get_database_stats(self):

        self.db_manager.connect()
        self.db_manager.create_table()
        self.db_manager.insert_data(self.sample_data)
        
        stats = self.db_manager.get_database_stats()
        
       
        self.assertIn('total_records', stats)
        self.assertIn('cities', stats)
        self.assertIn('price_distribution', stats)
        self.assertEqual(stats['total_records'], 3)
    
    def test_close_connection(self):
        
        self.db_manager.connect()
        self.db_manager.close()
        
       
        self.assertIsNone(self.db_manager.connection)
        
       
        with self.assertRaises(AttributeError):
            cursor = self.db_manager.connection.cursor()
            cursor.execute("SELECT 1")


class TestDatabaseManagerEdgeCases(unittest.TestCase):
    
    
    def setUp(self):
        
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db_path = Path(self.temp_db.name)
        self.temp_db.close()
        self.db_manager = DatabaseManager(db_path=self.temp_db_path)
    
    def tearDown(self):
        
        if self.db_manager.connection:
            self.db_manager.close()
        if self.temp_db_path.exists():
            os.unlink(self.temp_db_path)
    
    def test_empty_database(self):
        
        self.db_manager.connect()
        self.db_manager.create_table()
        
        count = self.db_manager.get_record_count()
        self.assertEqual(count, 0)
        
        cities = self.db_manager.get_cities()
        self.assertEqual(len(cities), 0)
    
    def test_query_nonexistent_city(self):
        
        self.db_manager.connect()
        self.db_manager.create_table()
        
        
        sample_data = [
            {'name': 'Restaurant A', 'city': 'Mumbai', 'cuisines': 'Italian', 'average_cost_for_two': 500, 'aggregate_rating': 4.5, 'votes': 100, 'price_category': 'budget', 'popularity_score': 0.8, 'cuisine_diversity': 1, 'has_online_delivery': 1, 'has_table_booking': 1, 'is_popular': 1}
        ]
        self.db_manager.insert_data(sample_data)
        
        
        results = self.db_manager.query_by_city('NonExistentCity')
        self.assertEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()
