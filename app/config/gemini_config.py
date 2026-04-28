# OLD - remove this
import google.generativeai as genai

# NEW
from google import genai
from google.genai import types
import os

def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing!")
    
    client = genai.Client(api_key=api_key)
    return client  # return client, not model

# Then use it like:
def analyze_route(origin, destination, client):
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # use this, not gemini-pro
        contents=f"Analyze supply chain risk for route: {origin} to {destination}"
    )
    return response.text