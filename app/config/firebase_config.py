import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    if not firebase_admin._apps:
        firebase_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")

        if not firebase_json:
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_JSON is not set")

        try:
            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            raise RuntimeError(f"Firebase init failed: {e}")

    return firestore.client()


# Initialize DB
db = init_firebase()