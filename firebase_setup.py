import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials
cred = credentials.Certificate(
    r"C:\Users\anany\Downloads\serviceAccountKey.json"
)

# Connect to Firebase
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

print("Firebase connected successfully!")