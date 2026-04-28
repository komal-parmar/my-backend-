import os
import google.generativeai as genai

def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing!")

    genai.configure(api_key=api_key)
    print("✅ Gemini AI connected successfully")


def get_gemini_model():
    return genai.GenerativeModel("gemini-pro")