import json
import logging
import os
from datetime import datetime
from typing import List, Any, Optional

logger = logging.getLogger(__name__)

class Exporter:
   
    def __init__(self, export_dir: str = "data/exports"):
        self.export_dir = export_dir
        os.makedirs(self.export_dir, exist_ok=True)

    def export_to_json(self, recommendations: List[Any], filename: Optional[str] = None) -> str:
        
        if not filename:
            filename = f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.export_dir, filename)
        
        
        serializable_data = [
            {
                "name": r.name,
                "rating": r.rating,
                "votes": r.votes,
                "cuisines": r.cuisines,
                "average_cost": r.average_cost,
                "address": r.address
            } for r in recommendations
        ]
        
        with open(filepath, 'w') as f:
            json.dump(serializable_data, f, indent=4)
        
        return filepath

    def export_to_csv(self, recommendations: List[Any], filename: Optional[str] = None) -> str:
        
        if not filename:
            filename = f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        header = "Name,Rating,Votes,Cuisines,Average Cost,Address\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header)
            for r in recommendations:
                # Basic escaping for CSV
                clean_name = f'"{r.name}"' if ',' in r.name else r.name
                clean_addr = f'"{r.address}"' if ',' in r.address else r.address
                f.write(f"{clean_name},{r.rating},{r.votes},{r.cuisines},{r.average_cost},{clean_addr}\n")
        
        return filepath
