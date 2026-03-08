import logging
from pathlib import Path

from phase1.data_loader import DataLoader
from phase1.data_cleaner import DataCleaner
from phase1.feature_engineer import FeatureEngineer
from phase1.database_setup import DatabaseManager
from phase1.config import PROCESSED_DATA_DIR


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Phase1Pipeline:
        
    def __init__(self):
        
        self.loader = DataLoader()
        self.cleaner = None
        self.engineer = None
        self.db_manager = DatabaseManager()
        self.processed_data = None
    
    def run(self, save_intermediate: bool = True):
        
        logger.info("=" * 80)
        logger.info("Starting Phase 1 Pipeline: Zomato Data Input and Processing")
        logger.info("=" * 80)
        
        
        logger.info("\n[STEP 1/5] Loading dataset from Hugging Face...")
        self.loader.load_dataset()
        data = self.loader.to_list()
        logger.info(f"✓ Dataset loaded: {len(data)} records")
        
        
        logger.info("\n[STEP 2/5] Cleaning data...")
        self.cleaner = DataCleaner(data)
        cleaned_data = self.cleaner.clean()
        cleaning_report = self.cleaner.get_cleaning_report()
        logger.info(f"✓ Data cleaned: {cleaning_report}")
        
        
        logger.info("\n[STEP 3/5] Engineering features...")
        self.engineer = FeatureEngineer(cleaned_data)
        processed_data = self.engineer.engineer_features()
        feature_summary = self.engineer.get_feature_summary()
        logger.info(f"✓ Features engineered: {list(feature_summary.keys())}")
        
        self.processed_data = processed_data
        
       
        if save_intermediate:
            logger.info("\n[STEP 4/5] Saving processed data...")
            processed_file = PROCESSED_DATA_DIR / "processed_restaurants.csv"
            self._save_to_csv(processed_data, processed_file)
            logger.info(f"✓ Processed data saved to: {processed_file}")
        else:
            logger.info("\n[STEP 4/5] Skipping intermediate save...")
        
        
        logger.info("\n[STEP 5/5] Storing data in database...")
        self.db_manager.connect()
        self.db_manager.insert_data(processed_data, if_exists='replace')
        
        db_stats = self.db_manager.get_database_stats()
        logger.info(f"✓ Data stored in database: {db_stats}")
        
        self.db_manager.close()
        
        
        logger.info("\n" + "=" * 80)
        logger.info("Phase 1 Pipeline Completed Successfully!")
        logger.info("=" * 80)
        logger.info(f"Total records processed: {len(processed_data)}")
        logger.info(f"Total cities: {db_stats.get('total_cities', 'N/A')}")
        logger.info(f"Database location: {self.db_manager.db_path}")
        logger.info("=" * 80)
        
        return processed_data
    
    def _save_to_csv(self, data: list, filepath: Path):
        
        import csv
        
        if not data:
            logger.warning("No data to save")
            return
        
        
        columns = list(data[0].keys())
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)


def main():
   
    pipeline = Phase1Pipeline()
    pipeline.run(save_intermediate=True)


if __name__ == "__main__":
    main()
