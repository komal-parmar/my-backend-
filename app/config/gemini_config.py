import google.generativeai as genai
import os

def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing!")
    genai.configure(api_key=api_key)
    
    # Try each model until one works
    for model_name in ["gemini-pro", "gemini-1.5-flash", "gemini-1.5-pro"]:
        try:
            model = genai.GenerativeModel(model_name)
            model.generate_content("test")
            return model
        except:
            continue
    raise ValueError("No Gemini model available")