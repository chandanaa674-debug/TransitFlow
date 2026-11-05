import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv


# Find the backend directory
BACKEND_DIR = Path(__file__).resolve().parents[2]

# Load environment variables from backend/.env
load_dotenv(BACKEND_DIR / ".env")


def get_firestore_client():
    """
    Connect to Firebase Firestore.

    Returns:
        Firestore client

    Raises:
        RuntimeError if Firebase credentials are missing
        or Firebase initialization fails.
    """

    credentials_file = os.getenv(
        "FIREBASE_CREDENTIALS",
        "serviceAccountKey.json"
    )

    credentials_path = Path(credentials_file)

    # Resolve relative paths from the backend directory
    if not credentials_path.is_absolute():
        credentials_path = BACKEND_DIR / credentials_path

    if not credentials_path.exists():
        raise RuntimeError(
            f"Firebase credentials file not found: {credentials_path}. "
            "Download your Firebase service account JSON file "
            "and place it inside the backend folder."
        )

    try:
        # Initialize Firebase only once
        try:
            firebase_admin.get_app()
        except ValueError:
            certificate = credentials.Certificate(
                str(credentials_path)
            )

            firebase_admin.initialize_app(certificate)

        # Connect to Firestore
        db = firestore.client()

        return db

    except Exception as error:
        raise RuntimeError(
            f"Firebase connection failed: {error}"
        ) from error