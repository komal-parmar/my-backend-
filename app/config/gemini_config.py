import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing!")
    print("✅ Gemini AI connected successfully")

def get_gemini_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
