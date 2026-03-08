import sys
import uvicorn
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from phase6.api_server import app

if __name__ == "__main__":
    try:
       
        print("\n" + "="*50)
        print("Starting Zomato AI Recommender (FastAPI UI)...")
        print("Visit: http://localhost:8000")
        print("="*50 + "\n")
        
        uvicorn.run("phase6.api_server:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
