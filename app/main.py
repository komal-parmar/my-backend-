from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import shipments, risk, chats, alerts
from app.config.firebase_config import init_firebase

 
app = FastAPI(
    title="Smart Supply Chain API",
    description="Backend for disruption detection and route optimization",
    version="1.0.0"
)
@app.on_event("startup")
def startup():
    init_firebase()


# ─── CORS (allows your React frontend to call this API) ───────────────────────
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000", "https://your-project.vercel.app" ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers (each file handles one feature) ──────────────────────────────────
app.include_router(shipments.router, prefix="/api/shipments", tags=["Shipments"])
app.include_router(risk.router,      prefix="/api/risk",      tags=["Risk Analysis"])
# app.include_router(routes.router,    prefix="/api/routes",    tags=["Route Optimization"])
app.include_router(chats.router,      prefix="/api/chat",      tags=["AI Chatbot"])
app.include_router(alerts.router,    prefix="/api/alerts",    tags=["Alerts"])

@app.get("/")
def root():
    return {"message": "Smart Supply Chain API is running ✅"}

@app.get("/health")
def health():
    return {"status": "ok"}