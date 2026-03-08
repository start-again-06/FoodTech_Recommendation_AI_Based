from typing import List, Dict, Any

SYSTEM_PROMPT = """
You are a helpful Zomato Restaurant Recommendation Assistant. 
Your goal is to provide a very brief, enthusiastic 2-3 sentence summary of the best matches found. 
Do NOT provide a numbered list in the summary, as the UI will show the details in cards. 
Just summarize why the selection is great for the user's specific craving.
"""

USER_PROMPT_TEMPLATE = """
I'm looking for restaurants in **{city}** with a **{price_range}** budget.
I prefer **{cuisine}** cuisine (if specified).
Minimum rating: **{min_rating}**.

Here are the top matches found in our database:
{restaurant_list}

Please provide a personalized recommendation list with a brief "Why you'll like it" for each.
"""

def format_restaurant_context(recommendations: List[Any]) -> str:
    """
    Format restaurant objects for the LLM context.
    """
    if not recommendations:
        return "No restaurants found."
    
    context = ""
    for i, rec in enumerate(recommendations, 1):
        context += f"\n{i}. {rec.name}\n"
        context += f"   - Rating: {rec.rating} ({rec.votes} votes)\n"
        context += f"   - Cuisines: {rec.cuisines}\n"
        context += f"   - Average Cost for Two: ₹{rec.average_cost}\n"
        context += f"   - Price Category: {rec.price_category}\n"
        context += f"   - Address: {rec.address}\n"
    return context
