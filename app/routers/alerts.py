from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from firebase_admin import firestore


from app.config.firebase_config import db
from app.models.schema import Alert, RiskLevel

router = APIRouter()

COLLECTION = "alerts"

# ─── GET all alerts (newest first) ───────────────────────────────────────────
@router.get("/")
def get_alerts(limit: int = 20):
    docs = (
        db.collection(COLLECTION)
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    return [{"id": d.id, **d.to_dict()} for d in docs]

# ─── GET alerts for one shipment ──────────────────────────────────────────────
@router.get("/{shipment_id}")
def get_alerts_for_shipment(shipment_id: str):
    docs = (
        db.collection(COLLECTION)
        .where("shipment_id", "==", shipment_id)
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .stream()
    )
    return [{"id": d.id, **d.to_dict()} for d in docs]

# ─── CREATE an alert (called automatically by risk analysis) ──────────────────
@router.post("/", status_code=201)
def create_alert(alert: Alert):
    now = datetime.now(timezone.utc).isoformat()
    data = {
        **alert.model_dump(exclude={"id"}),
        "created_at": now,
        "is_read": False,
    }
    doc_ref = db.collection(COLLECTION).add(data)
    doc_id=doc_ref[1].id
    return {"id": doc_id, **data}

# ─── MARK alert as read ───────────────────────────────────────────────────────
@router.patch("/{alert_id}/read")
def mark_as_read(alert_id: str):
    ref = db.collection(COLLECTION).document(alert_id)
    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Alert not found")
    ref.update({"is_read": True})
    return {"message": "Alert marked as read"}