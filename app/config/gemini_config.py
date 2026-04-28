import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def init_gemini():
    # This looks for the name inside your .env file
    api_key = os.getenv("GEMINI_API_KEY") 
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")
    
    genai.configure(api_key=api_key)

def get_gemini_model():
    init_gemini()
    # Use a modern model name here to fix the 404 error
    return genai.GenerativeModel("gemini-1.5-flash")