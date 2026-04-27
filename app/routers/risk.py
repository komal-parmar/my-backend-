from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import os, httpx, json
from firebase_admin import firestore
from app.config.firebase_config import db
from app.config.gemini_config import get_gemini_model
from app.models.schema import RiskAnalysisRequest, RiskAnalysisResult, RiskLevel

router = APIRouter()

# ─── Helper: fetch weather data for a city ───────────────────────────────────
async def get_weather(city: str) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(url)
            if r.status_code == 200:
                data = r.json()
                return {
                    "city":        city,
                    "condition":   data["weather"][0]["description"],
                    "temperature": data["main"]["temp"],
                    "wind_speed":  data["wind"]["speed"],
                }
    except Exception:
        pass
    return {"city": city, "condition": "unknown", "temperature": 0, "wind_speed": 0}

# ─── Helper: ask Gemini to analyze risk ──────────────────────────────────────
def analyze_with_gemini(origin: str, destination: str, weather_origin: dict, weather_dest: dict) -> dict:
    prompt = f"""
You are a supply chain risk analyst. Analyze the risk for a shipment and respond ONLY with valid JSON.

Shipment details:
- Origin: {origin}
- Destination: {destination}
- Weather at origin: {weather_origin['condition']}, {weather_origin['temperature']}°C, wind {weather_origin['wind_speed']} m/s
- Weather at destination: {weather_dest['condition']}, {weather_dest['temperature']}°C, wind {weather_dest['wind_speed']} m/s

Return ONLY this JSON (no extra text):
{{
  "risk_score": <number 0.0 to 10.0>,
  "risk_level": <"low" or "medium" or "high">,
  "risk_factors": [<list of 2-4 specific risk reasons as strings>],
  "recommendation": "<one clear action to take>"
}}
"""
    model = get_gemini_model()
    response=model.generate_content(prompt)
    raw=response.txt
    # Strip markdown code fences if Gemini adds them
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

# ─── POST /api/risk/analyze ───────────────────────────────────────────────────
@router.post("/analyze", response_model=RiskAnalysisResult)
async def analyze_risk(req: RiskAnalysisRequest):
    # 1. Check shipment exists
    doc = db.collection("shipments").document(req.shipment_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Shipment not found")

    # 2. Get weather for both cities
    weather_origin = await get_weather(req.origin)
    weather_dest   = await get_weather(req.destination)

    # 3. Ask Gemini
    try:
        gemini_result = analyze_with_gemini(req.origin, req.destination, weather_origin, weather_dest)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini analysis failed: {str(e)}")

    # 4. Save risk result back to Firestore
    now = datetime.now(timezone.utc).isoformat()
    db.collection("shipments").document(req.shipment_id).update({
        "risk_score": gemini_result["risk_score"],
        "risk_level": gemini_result["risk_level"],
        "updated_at": now,
    })

    # 5. Save to risk_analyses collection for history
    db.collection("risk_analyses").add({
        "shipment_id":   req.shipment_id,
        "analyzed_at":   now,
        **gemini_result,
        "weather_data":  {"origin": weather_origin, "destination": weather_dest},
    })

    return RiskAnalysisResult(
        shipment_id=req.shipment_id,
        analyzed_at=now,
        **gemini_result,
    )

# ─── GET /api/risk/{shipment_id}/history ─────────────────────────────────────
@router.get("/{shipment_id}/history")
def get_risk_history(shipment_id: str):
    docs = (
        db.collection("risk_analyses")
        .where("shipment_id", "==", shipment_id)
        .order_by("analyzed_at", direction=firestore.Query.DESCENDING)
        .limit(10)
        .stream()
    )
    return [{"id": d.id, **d.to_dict()} for d in docs]