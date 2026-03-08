import logging
import sqlite3
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

from phase1.config import DATABASE_PATH, DATABASE_TABLE_NAME


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    
    def __init__(self, db_path: Path = DATABASE_PATH):
        
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.table_name = DATABASE_TABLE_NAME
    
    def connect(self) -> sqlite3.Connection:
        
        if self.connection is None:
            db_dir = os.path.dirname(self.db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            logger.info(f"Connecting to database: {self.db_path}")
        
        assert self.connection is not None
        return self.connection
    
    def close(self):
        
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")
    
    def create_table(self):
        
        if not self.connection:
            self.connect()
        
        assert self.connection is not None  # Type hint for IDE
        logger.info(f"Creating table: {self.table_name}")
        
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            cuisines TEXT,
            average_cost_for_two REAL,
            aggregate_rating REAL,
            votes INTEGER,
            price_category TEXT,
            popularity_score REAL,
            cuisine_diversity INTEGER,
            has_online_delivery INTEGER,
            has_table_booking INTEGER,
            is_popular INTEGER,
            address TEXT,
            locality TEXT,
            online_order TEXT,
            book_table TEXT,
            rating_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor = self.connection.cursor()
        cursor.execute(create_table_query)
        self.connection.commit()
        logger.info(f"Table '{self.table_name}' created successfully")
    
    def create_indexes(self):
      
        if not self.connection:
            self.connect()
        
        assert self.connection is not None  # Type hint for IDE
        logger.info("Creating indexes...")
        cursor = self.connection.cursor()
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_city ON {self.table_name} (city)")
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_price ON {self.table_name} (price_category)")
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_city_price ON {self.table_name} (city, price_category)")
        self.connection.commit()
        logger.info("Database indexes created successfully")
    
    def insert_data(self, data: List[Dict[str, Any]], if_exists: str = 'replace'):
        
        if not self.connection:
            self.connect()
        
        assert self.connection is not None  # Type hint for IDE
        
        
        if if_exists == 'replace':
            cursor = self.connection.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            self.connection.commit()
            self.create_table()
            self.create_indexes()
        
        if not data:
            logger.warning("No data to insert")
            return
        
        logger.info(f"Inserting {len(data)} records into database...")
        
       
        allowed_columns = [
            "name", "city", "cuisines", "average_cost_for_two", "aggregate_rating", 
            "votes", "price_category", "popularity_score", "cuisine_diversity", 
            "has_online_delivery", "has_table_booking", "is_popular", "address", 
            "locality", "online_order", "book_table", "rating_text"
        ]
        
        
        columns = [col for col in data[0].keys() if col in allowed_columns]
        if not columns:
            logger.error("No valid columns found in data to insert")
            return
            
        placeholders = ','.join(['?' for _ in columns])
        column_names = ','.join(columns)
        
        insert_query = f"INSERT INTO {self.table_name} ({column_names}) VALUES ({placeholders})"
        
        # Insert data in batches
        cursor = self.connection.cursor()
        batch_size = 1000
        
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            values = [tuple(item.get(col) for col in columns) for item in batch]
            cursor.executemany(insert_query, values)
        
        self.connection.commit()
        logger.info(f"Data inserted successfully into '{self.table_name}'")
    
    def get_record_count(self) -> int:
       
        if not self.connection:
            self.connect()
        
        assert self.connection is not None  # Type hint for IDE
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        count = cursor.fetchone()[0]
        
        return count
    
    def get_cities(self) -> List[str]:
       
        if not self.connection:
            self.connect()
        
        assert self.connection is not None  # Type hint for IDE
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT DISTINCT city FROM {self.table_name} ORDER BY city")
        cities = [row[0] for row in cursor.fetchall()]
        
        return cities
    
    def get_cuisines(self) -> List[str]:
        
        if not self.connection:
            self.connect()
        
        assert self.connection is not None  # Type hint for IDE
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT cuisines FROM {self.table_name}")
        
        all_cuisines = set()
        for row in cursor.fetchall():
            cuisines_str = row[0]
            if cuisines_str:
                # Split by comma and add each cuisine to the set
                parts = [c.strip() for c in cuisines_str.split(',') if c.strip()]
                all_cuisines.update(parts)
        
        return sorted(list(all_cuisines))
    
    def get_sample_data(self, limit: int = 10) -> List[Dict[str, Any]]:
        
        if not self.connection:
            self.connect()
        
        assert self.connection is not None  # Type hint for IDE
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} LIMIT {limit}")
        
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        
        return data
    
    def query_by_city(self, city: str) -> List[Dict[str, Any]]:
        
        if not self.connection:
            self.connect()
        
        assert self.connection is not None  # Type hint for IDE
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE city = ?", (city,))
        
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        
        return data
    
    def query_by_city_and_price(self, city: str, price_category: str) -> List[Dict[str, Any]]:
        
        if not self.connection:
            self.connect()
        
        assert self.connection is not None  # Type hint for IDE
        cursor = self.connection.cursor()
        query = f"""
        SELECT * FROM {self.table_name} 
        WHERE city = ? AND price_category = ?
        ORDER BY popularity_score DESC
        """
        cursor.execute(query, (city, price_category))
        
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        
        return data
    
    def get_database_stats(self) -> dict:
      
        if not self.connection:
            self.connect()
        
        assert self.connection is not None  # Type hint for IDE
        stats: Dict[str, Any] = {
            "total_records": self.get_record_count(),
            "cities": len(self.get_cities()),
            "cuisines": len(self.get_cuisines()),
            "database_size_mb": self.db_path.stat().st_size / (1024 * 1024) if self.db_path.exists() else 0
        }
        
        # Get price category distribution
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT price_category, COUNT(*) FROM {self.table_name} GROUP BY price_category")
        stats["price_distribution"] = dict(cursor.fetchall())
        
        return stats


def main():
    
    db_manager = DatabaseManager()
    
    
    db_manager.connect()
    
 
    db_manager.create_table()
    
    
    db_manager.create_indexes()
    
   
    stats = db_manager.get_database_stats()
    logger.info(f"Database stats: {stats}")
    
    # Close connection
    db_manager.close()


if __name__ == "__main__":
    main()
