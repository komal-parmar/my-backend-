from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from google import genai
import json
import os

router = APIRouter(tags=["Route Analyze"])

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class RouteRequest(BaseModel):
    origin: str
    destination: str
    waypoint: Optional[str] = None


@router.post("/analyze-route")
async def analyze_route(req: RouteRequest):
    waypoint_text = f"via {req.waypoint}" if req.waypoint else "direct"

    prompt = f"""
You are a logistics risk intelligence expert for Indian freight and supply chain operations.

Analyze this specific route and provide a real-time risk assessment:
ROUTE: {req.origin} → {req.destination} ({waypoint_text})

Return ONLY a valid JSON object with this exact structure, no markdown, no explanation, just raw JSON:

{{
  "origin": "{req.origin}",
  "destination": "{req.destination}",
  "risk_score": <integer 0-100>,
  "risk_level": "<LOW|MED|HIGH>",
  "estimated_delay": "<e.g. 2-3 hrs or None>",
  "distance_km": <estimated integer km>,
  "transit_hours": <estimated float hours>,
  "fuel_liters": <estimated integer liters for a heavy truck>,
  "disruptions": [
    {{
      "type": "<Weather|Traffic|Port|Strike|Road|Other>",
      "detail": "<specific detail about this disruption on this exact route>"
    }}
  ],
  "recommendation": "<specific actionable rerouting recommendation>",
  "highway": "<main highway e.g. NH-48>",
  "risk_summary": "<2 sentence plain English summary of the overall risk>"
}}

Be specific to the actual {req.origin} to {req.destination} route in India.
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        response_text = response.text.strip()

        # Clean markdown fences if Gemini adds them
        FENCE = "```"
        if FENCE in response_text:
            parts = response_text.split(FENCE)
            inner = parts[1].strip()
            if inner.startswith("json"):
                inner = inner[4:].strip()
            return json.loads(inner)

        return json.loads(response_text)

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"AI returned invalid format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")