from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import json
import os

router = APIRouter(prefix="/api", tags=["Route Analysis"])


# ─── Request Model ────────────────────────────────────────────────────────────
class RouteRequest(BaseModel):
    origin: str
    destination: str
    waypoint: Optional[str] = None


# ─── Helper: Initialize Gemini safely ─────────────────────────────────────────
def get_model():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not set")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


# ─── Route Analysis API ───────────────────────────────────────────────────────
@router.post("/analyze-route")
async def analyze_route(req: RouteRequest):
    model = get_model()  # ✅ safe initialization

    waypoint_text = f"via {req.waypoint}" if req.waypoint else "direct"

    prompt = f"""
You are a logistics risk intelligence expert for Indian freight operations.

Analyze this route and return ONLY raw JSON — no markdown, no explanation, no code fences:

ROUTE: {req.origin} to {req.destination} ({waypoint_text})

Return this exact JSON structure:
{{
  "origin": "{req.origin}",
  "destination": "{req.destination}",
  "risk_score": <integer 0-100>,
  "risk_level": "<LOW|MED|HIGH>",
  "estimated_delay": "<e.g. 2-3 hrs or None>",
  "distance_km": <integer>,
  "transit_hours": <float>,
  "fuel_liters": <integer>,
  "disruptions": [
    {{
      "type": "<Weather|Traffic|Port|Strike|Road|Other>",
      "detail": "<specific detail for this route>"
    }}
  ],
  "recommendation": "<specific actionable recommendation>",
  "highway": "<main highway e.g. NH-48>",
  "risk_summary": "<2 sentence plain English risk summary>"
}}
"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # Remove markdown if present
        if "```" in response_text:
            parts = response_text.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                try:
                    return json.loads(part)
                except:
                    continue

        return json.loads(response_text)

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid AI response: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")