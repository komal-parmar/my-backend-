from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List

# ─── Enums ────────────────────────────────────────────────────────────────────
class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ShipmentStatus(str, Enum):
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    DELAYED = "delayed"
    DELIVERED = "delivered"

# ─── Shipment ─────────────────────────────────────────────────────────────────
class ShipmentCreate(BaseModel):
    tracking_id: str = Field(..., example="SHIP-2024-001")
    origin: str = Field(..., example="Mumbai, India")
    destination: str = Field(..., example="Delhi, India")
    cargo_type: str = Field(..., example="Electronics")
    weight_kg: float
    estimated_arrival: str   # ✅ string — works with both "2025-05-12" and ISO format

class Shipment(ShipmentCreate):
    id: Optional[str] = None
    status: ShipmentStatus = ShipmentStatus.PENDING
    risk_level: RiskLevel = RiskLevel.LOW
    risk_score: float = 0.0
    created_at: Optional[str] = None   # ✅ string — Firestore returns ISO strings
    updated_at: Optional[str] = None

# ─── Risk Analysis ────────────────────────────────────────────────────────────
class RiskAnalysisRequest(BaseModel):
    shipment_id: str
    origin: str
    destination: str

class RiskAnalysisResult(BaseModel):
    shipment_id: str
    risk_score: float
    risk_level: RiskLevel
    risk_factors: List[str]
    recommendation: str
    analyzed_at: str         # ✅ string

# ─── Route Suggestion ─────────────────────────────────────────────────────────
class RouteOption(BaseModel):
    route_name: str
    estimated_time: str
    estimated_cost: str
    risk_level: RiskLevel
    via_points: List[str]
    reason: str

class RouteSuggestionResult(BaseModel):
    shipment_id: str
    current_route: str
    alternatives: List[RouteOption]

# ─── Chat ─────────────────────────────────────────────────────────────────────
class ChatMessage(BaseModel):
    message: str = Field(..., example="Why is shipment SHIP-001 delayed?")
    shipment_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    sources: List[str] = []

# ─── Alert ────────────────────────────────────────────────────────────────────
class Alert(BaseModel):
    id: Optional[str] = None
    shipment_id: str
    alert_type: str
    message: str
    severity: RiskLevel
    created_at: Optional[str] = None   # ✅ string
    is_read: bool = False