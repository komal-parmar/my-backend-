from fastapi import APIRouter
from app.config.firebase_config import db
from app.config.gemini_config import get_gemini_client  # ✅ updated import
from app.models.schema import ChatMessage, ChatResponse

router = APIRouter()

# ─── POST /api/chat ───────────────────────────────────────────────────────────
@router.post("/", response_model=ChatResponse)
def chat(msg: ChatMessage):
    context = ""

    if msg.shipment_id:
        doc = db.collection("shipments").document(msg.shipment_id).get()
        if doc.exists:
            s = doc.to_dict()
            context = f"""
Shipment context:
- ID: {msg.shipment_id}
- Origin: {s.get('origin')}
- Destination: {s.get('destination')}
- Status: {s.get('status')}
- Risk Level: {s.get('risk_level')}
- Risk Score: {s.get('risk_score')}
- Cargo: {s.get('cargo_type')}
- Estimated Arrival: {s.get('estimated_arrival')}
"""

    prompt = f"""
You are a helpful supply chain assistant. Answer the user's question clearly and concisely.
{context}

User question: {msg.message}

Give a helpful, direct answer in 2-4 sentences. If you don't have enough information, say so politely.
"""

    try:
        client = get_gemini_client()                         # ✅ updated to client
        response = client.models.generate_content(           # ✅ updated call
            model="gemini-2.0-flash",
            contents=prompt
        )
        reply = getattr(response, "text", None)
        if not reply:
            reply = "No response generated"
    except Exception as e:
        reply = f"Sorry, I couldn't process that right now. Error: {str(e)}"

    return ChatResponse(
        reply=reply,
        sources=["Gemini AI", "Firestore shipment data"] if msg.shipment_id else ["Gemini AI"]
    )