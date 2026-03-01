import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

try:
    from phase6.api_server import app
except ImportError as e:
    # Fallback to a minimal app if imports fail, to help debug on Vercel
    from fastapi import FastAPI
    app = FastAPI()
    @app.get("/api/health")
    def health():
        return {"status": "error", "message": f"Import failed: {str(e)}", "path": sys.path}

