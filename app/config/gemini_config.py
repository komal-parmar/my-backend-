"""
config/gemini_config.py
───────────────────────
Initializes the Gemini AI client.
Import `get_gemini_model()` wherever you need AI features.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def init_gemini():
    """Call once at app startup (in main.py)."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY is missing!\n"
            "→ Get it free from: https://aistudio.google.com/app/apikey\n"
            "→ Paste it in your .env file"
        )

    genai.configure(api_key=api_key)
    print("✅ Gemini AI connected successfully")


def get_gemini_model():
    """
    Returns a ready-to-use Gemini model instance.

    Usage:
        from config.gemini_config import get_gemini_model
        model = get_gemini_model()
        response = model.generate_content("Your prompt here")
        print(response.text)
    """
    return genai.GenerativeModel("gemini-2.0-flash")   # Fast + free tier
