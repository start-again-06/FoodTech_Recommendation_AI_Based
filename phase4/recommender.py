import logging
from typing import Optional, Any, List
from phase2.models import UserInput
from phase3.recommender import RecommendationEngine
from phase4.groq_client import GroqClient
from phase4.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, format_restaurant_context

logger = logging.getLogger(__name__)

class LLMRecommender:
   
    def __init__(self, groq_client: Optional[GroqClient] = None, engine: Optional[RecommendationEngine] = None):
        
        self.groq_client = groq_client or GroqClient()
        self.engine = engine or RecommendationEngine()

    def get_reasoned_recommendations(self, user_input: UserInput, limit: int = 5) -> str:
        
        
        response = self.engine.get_recommendations(user_input, limit=limit)
        
        if response.count == 0:
            return f"I'm sorry, but I couldn't find any restaurants in {user_input.city} matching your criteria."

        
        restaurant_list = format_restaurant_context(response.recommendations)
        
    
        user_message = USER_PROMPT_TEMPLATE.format(
            city=user_input.city,
            price_range=user_input.price_range,
            cuisine=user_input.cuisine or "any",
            min_rating=user_input.min_rating,
            restaurant_list=restaurant_list
        )
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
        
       
        logger.info("Requesting reasoned recommendations from Groq...")
        reasoning = self.groq_client.get_completion(messages)
        
        return reasoning

    def get_individual_reasoning(self, user_input: UserInput, restaurant: Any) -> str:
        
        prompt = (
            f"Why is the restaurant '{restaurant.name}' in {user_input.city} a good match for someone looking for "
            f"{user_input.cuisine or 'any'} cuisine in the {user_input.price_range} price range with at least "
            f"{user_input.min_rating} rating? The restaurant has a rating of {restaurant.rating}, "
            f"serves {restaurant.cuisines}, and costs ₹{restaurant.average_cost} for two. "
            "Provide a short, 1-2 sentence justification starting with 'Why you'll like it:'."
        )
        
        messages = [
            {"role": "system", "content": "You are a helpful Zomato restaurant expert."},
            {"role": "user", "content": prompt}
        ]
        
        return self.groq_client.get_completion(messages)

    def generate_ai_summary(self, user_input: UserInput, recommendations: List[Any]) -> str:
        
        if not recommendations:
            return f"I couldn't find any restaurants in {user_input.city} matching your criteria."
            
        restaurant_names = ", ".join([r.name for r in recommendations])
        prompt = (
            f"I found {len(recommendations)} great spots in {user_input.city} for you: {restaurant_names}. "
            f"They match your preference for {user_input.price_range} pricing and {user_input.cuisine or 'various'} cuisines. "
            "Provide a single, welcoming sentence summarizing why these are good choices. "
            "Be energetic and helpful."
        )
        
        messages = [
            {"role": "system", "content": "You are a helpful Zomato restaurant expert."},
            {"role": "user", "content": prompt}
        ]
        
        return self.groq_client.get_completion(messages)
