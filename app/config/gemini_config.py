import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing!")
    genai.configure(api_key=api_key)

def get_gemini_model():
    init_gemini()
    return genai.GenerativeModel("gemini-2.0-flash")  # gemini-pro is deprecated