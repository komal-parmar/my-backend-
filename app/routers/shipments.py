from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from google.cloud import firestore  # ✅ fixed import

from app.config.firebase_config import db
from app.models.schema import Shipment, ShipmentCreate, ShipmentStatus

router = APIRouter()

COLLECTION = "shipments"

# ─── CREATE a shipment ────────────────────────────────────────────────────────
@router.post("/", response_model=Shipment, status_code=201)
def create_shipment(data: ShipmentCreate):
    now = datetime.now(timezone.utc).isoformat()

    doc_data = {
        **data.model_dump(),
        "status": ShipmentStatus.PENDING.value,
        "risk_level": "low",
        "risk_score": 0.0,
        "created_at": now,
        "updated_at": now,
    }

    # ✅ cleaner ID handling
    _, doc_ref = db.collection(COLLECTION).add(doc_data)

    return {**doc_data, "id": doc_ref.id}


# ─── GET all shipments ────────────────────────────────────────────────────────
@router.get("/")
def get_all_shipments():
    docs = (
        db.collection(COLLECTION)
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(50)
        .stream()
    )
    return [{"id": d.id, **d.to_dict()} for d in docs]


# ─── GET one shipment by ID ───────────────────────────────────────────────────
@router.get("/{shipment_id}")
def get_shipment(shipment_id: str):
    doc = db.collection(COLLECTION).document(shipment_id).get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return {"id": doc.id, **doc.to_dict()}


# ─── UPDATE shipment status ───────────────────────────────────────────────────
@router.patch("/{shipment_id}/status")
def update_status(shipment_id: str, status: ShipmentStatus):
    ref = db.collection(COLLECTION).document(shipment_id)

    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Shipment not found")

    ref.update({
        "status": status.value,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    })

    return {"message": f"Status updated to {status.value}"}


# ─── DELETE a shipment ────────────────────────────────────────────────────────
@router.delete("/{shipment_id}")
def delete_shipment(shipment_id: str):
    ref = db.collection(COLLECTION).document(shipment_id)

    if not ref.get().exists:
        raise HTTPException(status_code=404, detail="Shipment not found")

    ref.delete()

    return {"message": "Shipment deleted"}