from fastapi import APIRouter
from app.config.firebase_config import db
from app.config.gemini_config import init_gemini, get_gemini_model
from app.models.schema import ChatMessage, ChatResponse

router = APIRouter()

# ─── POST /api/chat ───────────────────────────────────────────────────────────
@router.post("/", response_model=ChatResponse)
def chat(msg: ChatMessage):
    context = ""

    # ─── Get shipment context ────────────────────────────────────────────────
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
        # ✅ correct usage
        init_gemini()
        model = get_gemini_model()

        response = model.generate_content(prompt)
        reply = response.text if response.text else "No response generated"

    except Exception as e:
        reply = f"Sorry, I couldn't process that right now. Error: {str(e)}"

    return ChatResponse(
        reply=reply,
        sources=["Gemini AI", "Firestore shipment data"] if msg.shipment_id else ["Gemini AI"]
    )