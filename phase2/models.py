from typing import Optional, List, Any
from pydantic import BaseModel, Field, field_validator

class UserInput(BaseModel):
   
    city: str = Field(..., description="City to search for restaurants")
    price_range: str = Field(..., description="Price category (budget, mid-range, premium)")
    
    
    cuisine: Optional[List[str]] = Field(None, description="Preferred cuisines")
    min_rating: float = Field(0.0, ge=0.0, le=5.0, description="Minimum restaurant rating")
    
    @field_validator('cuisine', mode='before')
    @classmethod
    def validate_cuisine(cls, v: Any) -> Optional[List[str]]:
        if v is None:
            return None
        if isinstance(v, str):
            return [v.strip()]
        if isinstance(v, list):
            return [str(item).strip() for item in v if str(item).strip()]
        return None
    
    @field_validator('city')
    @classmethod
    def validate_city(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("City cannot be empty")
        return v.strip().title()
    
    @field_validator('price_range')
    @classmethod
    def validate_price_range(cls, v: str) -> str:
        v = v.strip().lower()
        valid_ranges = ['budget', 'mid-range', 'premium']
        if v not in valid_ranges:
            raise ValueError(f"Price range must be one of: {', '.join(valid_ranges)}")
        return v
