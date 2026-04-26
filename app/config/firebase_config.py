import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# ─── Build the Firebase credential from your .env variables ──────────────────
# (This avoids storing the serviceAccountKey.json file in your repo)_cred_dict = {
#     "type": "service_account",
#     "project_id":                os.getenv("FIREBASE_PROJECT_ID"),
#     "private_key_id":            os.getenv("FIREBASE_PRIVATE_KEY_ID"),
#     "private_key":               os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
#     "client_email":              os.getenv("FIREBASE_CLIENT_EMAIL"),
#     "client_id":                 os.getenv("FIREBASE_CLIENT_ID"),
#     "auth_uri":                  "https://accounts.google.com/o/oauth2/auth",
#     "token_uri":                 "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url":      f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}",
# }

# ─── Initialize Firebase only once ───────────────────────────────────────────
if not firebase_admin._apps:
    cred = credentials.Certificate("ServiceAccountKey.json")
    firebase_admin.initialize_app(cred)

# ─── Firestore client — import this anywhere you need the database ────────────
db = firestore.client()

def init_firebase():
    pass