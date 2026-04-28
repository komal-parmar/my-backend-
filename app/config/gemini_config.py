from google import genai
import os

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing!")
    return genai.Client(api_key=api_key)

def analyze_route(origin, destination, client):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Analyze supply chain risk for route: {origin} to {destination}"
    )
    return response.text