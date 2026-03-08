from pydantic import BaseModel, Field
from typing import List, Optional

class RestaurantRecommendation(BaseModel):
    
    name: str = Field(..., description="Restaurant name")
    city: str = Field(..., description="Locality/City")
    address: str = Field(..., description="Full address")
    cuisines: str = Field(..., description="Cuisine types")
    average_cost: int = Field(..., description="Average cost for two")
    price_category: str = Field(..., description="Economy category (budget, mid-range, premium)")
    rating: float = Field(..., description="Aggregate rating")
    votes: int = Field(..., description="Number of votes")
    match_score: float = Field(default=0.0, description="Calculated recommendation score")

class RecommendationResponse(BaseModel):
    
    user_city: str
    count: int
    recommendations: List[RestaurantRecommendation]
