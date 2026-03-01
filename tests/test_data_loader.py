import unittest
from unittest.mock import Mock, patch, MagicMock
from datasets import Dataset

from phase1.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):

    
    def setUp(self):
        """
        Set up test fixtures
        """
        self.loader = DataLoader()
    
    @patch('phase1.data_loader.load_dataset')
    def test_load_dataset_success(self, mock_load_dataset):
       
        mock_data = {'train': Dataset.from_dict({'name': ['Restaurant A'], 'city': ['City A']})}
        mock_load_dataset.return_value = mock_data
        

        dataset = self.loader.load_dataset()
        
       
        self.assertIsNotNone(dataset)
        mock_load_dataset.assert_called_once()
    
    @patch('phase1.data_loader.load_dataset')
    def test_load_dataset_with_different_split(self, mock_load_dataset):
        
        mock_data = {'test': Dataset.from_dict({'name': ['Restaurant A'], 'city': ['City A']})}
        mock_load_dataset.return_value = mock_data
        
        
        dataset = self.loader.load_dataset()
        
        
        self.assertIsNotNone(dataset)
    
    def test_to_list_without_loading(self):
        
        with self.assertRaises(ValueError):
            self.loader.to_list()
    
    @patch('phase1.data_loader.load_dataset')
    def test_to_list_success(self, mock_load_dataset):
        
        mock_data = {'train': Dataset.from_dict({
            'name': ['Restaurant A', 'Restaurant B'],
            'city': ['City A', 'City B']
        })}
        mock_load_dataset.return_value = mock_data
     
        self.loader.load_dataset()
        data = self.loader.to_list()
   
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertIsInstance(data[0], dict)
        self.assertIn('name', data[0])
        self.assertIn('city', data[0])
    
    @patch('phase1.data_loader.load_dataset')
    def test_get_dataset_info(self, mock_load_dataset):
       
        mock_data = {'train': Dataset.from_dict({
            'name': ['Restaurant A'],
            'city': ['City A'],
            'rating': [4.5]
        })}
        mock_load_dataset.return_value = mock_data
        
        
        self.loader.load_dataset()
        self.loader.to_list()
        info = self.loader.get_dataset_info()
        
      
        self.assertIn('num_records', info)
        self.assertIn('num_columns', info)
        self.assertIn('columns', info)
        self.assertEqual(info['num_records'], 1)
        self.assertEqual(info['num_columns'], 3)
    
    @patch('phase1.data_loader.load_dataset')
    @patch('builtins.open', new_callable=lambda: MagicMock())
    def test_save_raw_data(self, mock_open, mock_load_dataset):
      
        mock_data = {'train': Dataset.from_dict({
            'name': ['Restaurant A'],
            'city': ['City A']
        })}
        mock_load_dataset.return_value = mock_data
        
        self.loader.load_dataset()
        self.loader.to_list()
        
    
        filepath = self.loader.save_raw_data('test.csv')
        
       
        self.assertTrue(mock_open.called)


class TestDataLoaderEdgeCases(unittest.TestCase):
    
    @patch('phase1.data_loader.load_dataset')
    def test_empty_dataset(self, mock_load_dataset):

        mock_data = {'train': Dataset.from_dict({'name': [], 'city': []})}
        mock_load_dataset.return_value = mock_data
        
        loader = DataLoader()
        loader.load_dataset()
        data = loader.to_list()
        
    
        self.assertEqual(len(data), 0)
    
    @patch('phase1.data_loader.load_dataset')
    def test_load_dataset_failure(self, mock_load_dataset):
        
        mock_load_dataset.side_effect = Exception("Network error")
        
        loader = DataLoader()
        
        
        with self.assertRaises(Exception):
            loader.load_dataset()


if __name__ == '__main__':
    unittest.main()
