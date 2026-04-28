from app.config.firebase_config import init_firebase, db
from datetime import datetime, timezone

SAMPLE_SHIPMENTS = [
    {
        "tracking_id": "TRK-001",
        "origin": "Mumbai, India",
        "destination": "Dubai, UAE",
        "cargo_type": "Electronics",
        "weight_kg": 850.0,
        "carrier": "DHL Express",
        "route": "Sea → Arabian Sea → Port Rashid",
        "estimated_arrival": "2025-05-12",   # ✅ fixed name
        "status": "in_transit",
        "risk_level": "low",                 # ✅ fixed enum
        "risk_score": 0.0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    },
    {
        "tracking_id": "TRK-002",
        "origin": "Shanghai, China",
        "destination": "Hamburg, Germany",
        "cargo_type": "Automotive Parts",
        "weight_kg": 12000.0,
        "carrier": "Maersk Line",
        "route": "Sea → Suez Canal → Mediterranean",
        "estimated_arrival": "2025-05-20",
        "status": "in_transit",
        "risk_level": "low",
        "risk_score": 0.0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    },
    {
        "tracking_id": "TRK-003",
        "origin": "Los Angeles, USA",
        "destination": "Tokyo, Japan",
        "cargo_type": "Pharmaceuticals",
        "weight_kg": 200.0,
        "carrier": "FedEx International",
        "route": "Air → Pacific Route",
        "estimated_arrival": "2025-05-08",
        "status": "pending",
        "risk_level": "low",
        "risk_score": 0.0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    },
    {
        "tracking_id": "TRK-004",
        "origin": "Rotterdam, Netherlands",
        "destination": "New York, USA",
        "cargo_type": "Food & Beverages",
        "weight_kg": 5000.0,
        "carrier": "MSC Shipping",
        "route": "Sea → Atlantic Ocean",
        "estimated_arrival": "2025-05-18",
        "status": "delayed",
        "risk_level": "low",
        "risk_score": 0.0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    },
    {
        "tracking_id": "TRK-005",
        "origin": "Nairobi, Kenya",
        "destination": "London, UK",
        "cargo_type": "Agricultural Produce",
        "weight_kg": 3000.0,
        "carrier": "Kenya Airways Cargo",
        "route": "Air → Direct Flight",
        "estimated_arrival": "2025-05-07",
        "status": "in_transit",
        "risk_level": "low",
        "risk_score": 0.0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    },
]


def seed():
    print("🌱 Seeding Firestore with sample shipments...")
    init_firebase()

    collection = db.collection("shipments")

    for shipment in SAMPLE_SHIPMENTS:
        # Check if tracking_id already exists
        existing = collection.where("tracking_id", "==", shipment["tracking_id"]).limit(1).stream()

        if any(True for _ in existing):
            print(f"⚠️ {shipment['tracking_id']} already exists — skipping")
            continue

        # ✅ cleaner Firestore ID handling
        _, doc_ref = collection.add(shipment)

        print(f"✅ Created {shipment['tracking_id']} → ID: {doc_ref.id}")

    print("\n🎉 Done! Your database now has sample shipments.")


if __name__ == "__main__":
    seed()