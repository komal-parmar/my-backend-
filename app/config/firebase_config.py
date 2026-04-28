import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# ─── Initialize Firebase only once ───────────────────────────────────────────
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS", "./app/config/ServiceAccountKey.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# ─── Firestore client ─────────────────────────────────────────────────────────
db = firestore.client()

def init_firebase():
    pass