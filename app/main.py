from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()  
# Import routers
from app.routers import alerts
from app.routers import analyze_route
from app.routers import risk
from app.routers import shipments
from app.routers import chats

app = FastAPI(title="SupplyLens API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with prefixes
app.include_router(alerts.router, prefix="/alerts")
app.include_router(analyze_route.router, prefix="/route")
app.include_router(risk.router, prefix="/risk")
app.include_router(shipments.router, prefix="/shipments")
app.include_router(chats.router, prefix="/chat")


@app.get("/")
async def root():
    return {"status": "SupplyLens API running", "version": "1.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}