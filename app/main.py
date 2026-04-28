from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

# Import all routers — names must EXACTLY match filenames
from app.routers import alerts
from app.routers import analyze_route   # file must be analyze_route.py (lowercase)
from app.routers import risk
from app.routers import shipments
from app.routers import chats

app = FastAPI(title="SupplyLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.vercel.app",   # replace with your actual Vercel URL
        "*"                                    # remove this in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(alerts.router)
app.include_router(analyze_route.router)
app.include_router(risk.router)
app.include_router(shipments.router)
app.include_router(chats.router)


@app.get("/")
async def root():
    return {"status": "SupplyLens API running", "version": "1.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}