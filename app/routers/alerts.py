from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from google.cloud import firestore  # ✅ fixed import

from app.config.firebase_config import db
from app.models.schema import Alert

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
        .stream()
    )

    alerts = [{"id": d.id, **d.to_dict()} for d in docs]

    # ✅ manual sorting (avoids Firestore index error)
    alerts.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return alerts


# ─── CREATE an alert ──────────────────────────────────────────────────────────
@router.post("/", status_code=201)
def create_alert(alert: Alert):
    now = datetime.now(timezone.utc).isoformat()

    data = {
        **alert.model_dump(exclude={"id"}),
        "created_at": now,
        "is_read": False,
    }

    # ✅ cleaner way to get document id
    _, doc_ref = db.collection(COLLECTION).add(data)

    return {"id": doc_ref.id, **data}


# ─── MARK alert as read ───────────────────────────────────────────────────────
@router.patch("/{alert_id}/read")
def mark_as_read(alert_id: str):
    ref = db.collection(COLLECTION).document(alert_id)
    doc = ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Alert not found")

    ref.update({"is_read": True})

    return {"message": "Alert marked as read"}