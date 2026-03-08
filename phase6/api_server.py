import logging
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from typing import List, Optional
from pydantic import BaseModel
from phase2.models import UserInput
from phase4.recommender import LLMRecommender
from phase5.feedback_collector import FeedbackCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zomato AI Recommendation API",
    description="API for restaurant recommendations in Bangalore with AI reasoning.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_path = os.path.join(BASE_DIR, "frontend")
if not os.path.exists(frontend_path):
    os.makedirs(frontend_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

class RecommendationRequest(BaseModel):
    city: str
    price_range: str
    cuisine: Optional[List[str]] = None
    min_rating: float = 0.0

class RestaurantResponse(BaseModel):
    name: str
    rating: float
    votes: int
    cuisines: str
    average_cost: float
    reasoning: str

class FeedbackRequest(BaseModel):
    restaurant_name: str
    rating: int
    comment: Optional[str] = ""

@app.get("/")
async def root():
    
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to Zomato AI Recommender API", "status": "active", "api_docs": "/docs"}

@app.post("/api/recommend", response_model=dict)
async def get_recommendations(request: RecommendationRequest):
    
    try:
        # Map API request to internal UserInput model
        user_input = UserInput(
            city=request.city,
            price_range=request.price_range,
            cuisine=request.cuisine,
            min_rating=request.min_rating
        )
        
        recommender = LLMRecommender()
        
        
        engine_response = recommender.engine.get_recommendations(user_input, limit=6)
        
        if engine_response.count == 0:
            return {
                "status": "success",
                "count": 0,
                "recommendations": [],
                "message": f"No restaurants found in {request.city} matching your criteria."
            }
            
        
        ai_reasoning = recommender.get_reasoned_recommendations(user_input, limit=6)
        
      
        results = []
        for rec in engine_response.recommendations:
            
            reasoning = recommender.get_individual_reasoning(user_input, rec)
            results.append({
                "name": rec.name,
                "rating": rec.rating,
                "votes": rec.votes,
                "cuisines": rec.cuisines,
                "average_cost": rec.average_cost,
                "address": rec.address,
                "reasoning": reasoning
            })
            
        return {
            "status": "success",
            "count": len(results),
            "recommendations": results,
            "ai_reasoning_summary": ai_reasoning # Keep summary as well
        }
        
    except Exception as e:
        logger.error(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest):
 
    try:
        collector = FeedbackCollector()
        collector.collect_feedback(
            restaurant_name=feedback.restaurant_name,
            rating=feedback.rating,
            comment=feedback.comment
        )
        return {"status": "success", "message": "Feedback submitted successfully"}
    except Exception as e:
        logger.error(f"Feedback API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
