import sys
import logging
from typing import Dict, Any, Optional

from phase2.models import UserInput
from phase2.input_validator import InputValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommandLineInterface:
    
    
    def __init__(self, validator: Optional[InputValidator] = None):
       
        self.validator = validator or InputValidator()
        
    def print_welcome(self):
       
        print("\n" + "="*50)
        print("   WELCOME TO ZOMATO RESTAURANT RECOMMENDER")
        print("="*50)
        print("Helping you find the best places to eat!\n")
        
    def prompt_user(self) -> UserInput:
        
        while True:
            print("-" * 30)
            print("Please enter your preferences:")
            
           
            localities = self.validator.available_cities
            print(f"\nAvailable Bangalore Localities ({len(localities)} total):")
            
            for i in range(0, len(localities), 3):
                row = ""
                for j in range(i, min(i + 3, len(localities))):
                    row += f"{j+1:2}. {localities[j]:22}"
                print(row)
            
            selection = input("\nSelect Locality by name or number: ").strip()
            
           
            selected_city = selection
            if selection.isdigit():
                index = int(selection) - 1
                if 0 <= index < len(localities):
                    selected_city = localities[index]
                    print(f"Selected: {selected_city}")
                else:
                    print(f"\n\u274c Error: Invalid number '{selection}'. Please choose between 1 and {len(localities)}.")
                    continue
            
           
            from phase2.config import PRICE_CATEGORIES
            print("\nPrice Categories:")
            categories = list(PRICE_CATEGORIES.keys())
            for idx, cat in enumerate(categories, 1):
                min_p, max_p = PRICE_CATEGORIES[cat]
                desc = f"₹{min_p} to ₹{max_p}" if max_p != float('inf') else f"starting from ₹{min_p}"
                print(f"{idx}. {cat.capitalize()}: {desc}")
            
            price_input = input("\nEnter Option (1-3), Category Name, or Budget Amount: ").strip().lower()
            
            
            price_range = price_input
            
           
            if price_input in ['1', '2', '3']:
                price_range = categories[int(price_input) - 1]
                print(f"Selected: {price_range}")
            
            # Case 2: Numeric Budget Amount (e.g., 559)
            elif price_input.replace('.', '', 1).isdigit():
                budget_amount = float(price_input)
                for cat, (min_p, max_p) in PRICE_CATEGORIES.items():
                    if min_p <= budget_amount < max_p:
                        price_range = cat
                        print(f"Mapped budget ₹{budget_amount} to category: {price_range}")
                        break
                else:
                    price_range = "premium"
                    print(f"Mapped budget ₹{budget_amount} to category: {price_range}")
            
            
            print("\nAvailable Cuisines (Sample):")
            sample_cuisines = self.validator.available_cuisines[:20] 
            for i in range(0, len(sample_cuisines), 5):
                print(", ".join(sample_cuisines[i:i+5]))
            print("... and 80+ more")
            
            cuisine = input("\nPreferred Cuisine (Optional, press Enter to skip): ").strip() or None
            
            rating_input = input("Minimum Rating (0-5, default 0): ").strip()
            min_rating = float(rating_input) if rating_input else 0.0
            
           
            raw_data = {
                "city": selected_city,
                "price_range": price_range,
                "cuisine": cuisine,
                "min_rating": min_rating
            }
            
            
            user_input, error = self.validator.validate_user_input(raw_data)
            
            if user_input:
                print("\n\u2713 Input validated successfully!")
                return user_input
            else:
                print(f"\n\u274c Error: {error}")
                print("Please try again.\n")

    def run(self):
        
        try:
            self.print_welcome()
            user_input = self.prompt_user()
            
            print("\nSummary of your request:")
            print(f"- Bangalore Locality: {user_input.city}")
            print(f"- Price: {user_input.price_range}")
            if user_input.cuisine:
                print(f"- Cuisine: {user_input.cuisine}")
            print(f"- Min Rating: {user_input.min_rating}")
            
            print("\nProceeding to Phase 3 (Integration)...")
            return user_input
            
        except KeyboardInterrupt:
            print("\n\nExiting... Goodbye!")
            sys.exit(0)

def main():
    cli = CommandLineInterface()
    cli.run()

if __name__ == "__main__":
    main()
