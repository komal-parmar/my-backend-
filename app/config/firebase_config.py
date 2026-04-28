import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    firebase_key = os.getenv("FIREBASE_KEY")

    # 🔹 CASE 1: Running on Render (production)
    if firebase_key:
        firebase_dict = json.loads(firebase_key)
        cred = credentials.Certificate(firebase_dict)

    # 🔹 CASE 2: Running locally
    else:
        cred = credentials.Certificate("app/config/ServiceAccountKey.json")

    # Initialize only once
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    return firestore.client()

db = init_firebase()