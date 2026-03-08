import logging
import csv
from typing import Optional, Dict, Any, List

from datasets import load_dataset, Dataset

from phase1.config import DATASET_NAME, DATASET_SPLIT, RAW_DATA_DIR


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    
    
    def __init__(self, dataset_name: str = DATASET_NAME, split: str = DATASET_SPLIT):
        
        self.dataset_name = dataset_name
        self.split = split
        self.dataset: Optional[Dataset] = None
        self.data: List[Dict[str, Any]] = []
    
    def load_dataset(self) -> Dataset:
        
        try:
            logger.info(f"Loading dataset: {self.dataset_name}, split: {self.split}")
            ds = load_dataset(self.dataset_name)
            
            if self.split in ds:
                self.dataset = ds[self.split]
            else:
                available_splits = list(ds.keys())
                logger.warning(
                    f"Split '{self.split}' not found. Available splits: {available_splits}. "
                    f"Using first available split: {available_splits[0]}"
                )
                self.dataset = ds[available_splits[0]]
            
            if self.dataset is not None:
                logger.info(f"Dataset loaded successfully. Total records: {len(self.dataset)}")
            return self.dataset
            
        except Exception as e:
            logger.error(f"Failed to load dataset: {str(e)}")
            raise
    
    def to_list(self) -> List[Dict[str, Any]]:
        if self.dataset is None:
            raise ValueError("Dataset not loaded. Call load_dataset() first.")
        
        logger.info("Converting dataset to list of dictionaries with column mapping")
        self.data = []
        
        mapping = {
            "listed_in(city)": "city",
            "approx_cost(for two people)": "average_cost_for_two",
            "rate": "aggregate_rating",
            "online_order": "online_order",
            "book_table": "book_table"
        }
        
       
        dataset = self.dataset
        assert dataset is not None  
        for item in dataset:
            mapped_item = dict(item)
            
            
            for raw_col, target_col in mapping.items():
                if raw_col in mapped_item:
                    mapped_item[target_col] = mapped_item.pop(raw_col)
            
            self.data.append(mapped_item)
        
        logger.info(f"Converted {len(self.data)} records with mapping")
        return self.data
    
    def get_dataset_info(self) -> Dict[str, Any]:
        
        if not self.data:
            raise ValueError("Data not converted. Call to_list() first.")
        
        
        columns = list(self.data[0].keys()) if self.data else []
        
        info = {
            "num_records": len(self.data),
            "num_columns": len(columns),
            "columns": columns
        }
        
        return info
    
    def save_raw_data(self, filename: str = "raw_data.csv") -> str:
        
        if not self.data:
            raise ValueError("Data not converted. Call to_list() first.")
        
        filepath = RAW_DATA_DIR / filename
        logger.info(f"Saving raw data to: {filepath}")
        
        
        if not self.data:
            logger.warning("No data to save")
            return str(filepath)
        
        columns = list(self.data[0].keys())
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(self.data)
        
        logger.info("Raw data saved successfully")
        return str(filepath)
    
    def load_from_csv(self, filepath: str) -> List[Dict[str, Any]]:
        
        logger.info(f"Loading data from CSV: {filepath}")
        self.data = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append(dict(row))
        
        logger.info(f"Data loaded successfully. Records: {len(self.data)}")
        return self.data


def main():

    loader = DataLoader()
    
    
    dataset = loader.load_dataset()
    
 
    data = loader.to_list()
    
    info = loader.get_dataset_info()
    logger.info(f"Dataset Info: {info}")
    
    
    filepath = loader.save_raw_data()
    logger.info(f"Raw data saved to: {filepath}")


if __name__ == "__main__":
    main()
