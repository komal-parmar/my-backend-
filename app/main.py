from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import shipments, risk, chats, alerts, analyze_route
from app.config.firebase_config import init_firebase


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_firebase()
    yield


app = FastAPI(
    title="Smart Supply Chain API",
    description="Backend for disruption detection and route optimization",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-project.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shipments.router,      prefix="/api/shipments",     tags=["Shipments"])
app.include_router(risk.router,           prefix="/api/risk",          tags=["Risk Analysis"])
app.include_router(chats.router,          prefix="/api/chat",          tags=["AI Chatbot"])
app.include_router(alerts.router,         prefix="/api/alerts",        tags=["Alerts"])
app.include_router(analyze_route.router,  prefix="/api/analyze-route", tags=["Analyze Route"])


@app.get("/")
def root():
    return {"message": "Smart Supply Chain API is running ✅"}


@app.get("/health")
def health():
    return {"status": "ok"}