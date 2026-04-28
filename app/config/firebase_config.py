import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    if not firebase_admin._apps:

        firebase_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")

        if firebase_json:
            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
        else:
            cred = credentials.Certificate("app/config/ServiceAccountKey.json")

        firebase_admin.initialize_app(cred)

    return firestore.client()

db = init_firebase()