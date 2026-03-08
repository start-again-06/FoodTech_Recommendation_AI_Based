import logging
import sys
from phase2.main import get_user_preferences
from phase3.recommender import RecommendationEngine

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)

def run_recommendation_flow():
    
    print("\n" + "="*50)
    print("   ZOMATO RESTAURANT RECOMMENDER - PHASE 3")
    print("="*50)
    
    
    user_input = get_user_preferences()
    if not user_input:
        print("Failed to get valid user preferences. Exiting.")
        return

    recommender = RecommendationEngine()
    print(f"\nSearching for best restaurants in {user_input.city}...")
    
    response = recommender.get_recommendations(user_input, limit=5)
    

    if response.count == 0:
        print("\n\u274c No restaurants found matching your criteria.")
        print("Try expanding your budget or changing the cuisine.")
    else:
        print(f"\n\u2705 Found {response.count} recommended restaurants for you:")
        print("-" * 60)
        for i, rec in enumerate(response.recommendations, 1):
            print(f"{i}. {rec.name} (Match Score: {rec.match_score}/10)")
            print(f"   Rating: {rec.rating} \u2b50 | Votes: {rec.votes}")
            print(f"   Cuisines: {rec.cuisines}")
            print(f"   Avg Cost for 2: \u20b9{rec.average_cost}")
            print(f"   Address: {rec.address}")
            print("-" * 60)

    print("\nThank you for using Zomato Recommender!")

if __name__ == "__main__":
    try:
        run_recommendation_flow()
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
