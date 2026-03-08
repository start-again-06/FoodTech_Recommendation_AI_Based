import logging
import sys
from phase2.main import get_user_preferences
from phase4.recommender import LLMRecommender

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)

def run_phase4_flow():
   
    print("\n" + "="*60)
    print("   ZOMATO AI RECOMMENDER - PHASE 4 (LLM POWERED)")
    print("="*60)
    
    user_input = get_user_preferences()
    if not user_input:
        print("Failed to get valid user preferences. Exiting.")
        return

    print(f"\nSearching for restaurants in {user_input.city}...")
    print("Analyzing recommendations using AI (Groq)...")
    
    try:
        recommender = LLMRecommender()
        reasoning = recommender.get_reasoned_recommendations(user_input, limit=5)
        
        print("\n" + "="*60)
        print("AI SUGGESTIONS:")
        print("="*60)
        print(reasoning)
        print("="*60)
        
    except Exception as e:
        print(f"\n\u274c Error during AI recommendation: {e}")
        print("Falling back to local results...")
        # Optional: fallback to phase3 display logic here if needed

    print("\nThank you for using Zomato AI Recommender!")

if __name__ == "__main__":
    try:
        run_phase4_flow()
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
