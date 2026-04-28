import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    # Get Firebase JSON from environment variable
    firebase_key = os.getenv("FIREBASE_KEY")

    if not firebase_key:
        raise ValueError("FIREBASE_KEY environment variable not set")

    # Convert string to JSON
    firebase_dict = json.loads(firebase_key)

    # Initialize Firebase only once
    if not firebase_admin._apps:
        cred = credentials.Certificate("app/config/ServiceAccountKey.json")
        firebase_admin.initialize_app(cred)

    return firestore.client()

# Initialize DB
db = init_firebase()