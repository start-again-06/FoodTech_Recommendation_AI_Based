import os
import logging
from typing import List, Dict, Any, Optional
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)

class GroqClient:
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            try:
                import streamlit as st
                if hasattr(st, "secrets"):
                    self.api_key = st.secrets.get("GROQ_API_KEY")
            except Exception:
                pass

        if not self.api_key:
            raise ValueError("Groq API key not found. Please set GROQ_API_KEY in .env file or Streamlit secrets.")
        
        self.client = Groq(api_key=self.api_key)
        self.model = model

    def get_completion(self, messages: List[Dict[str, str]], temperature: float = 0.5, max_tokens: int = 1000) -> str:
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"Groq API Error: {e}")
            raise
