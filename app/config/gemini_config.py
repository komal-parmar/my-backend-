import os
from google import genai
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
    print("✅ Gemini AI connected successfully")


def get_gemini_client():
    """
    Returns a ready-to-use Gemini client instance.

    Usage:
        from config.gemini_config import get_gemini_client
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Your prompt here"
        )
        print(response.text)
    """
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))