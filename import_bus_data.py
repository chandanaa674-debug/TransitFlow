
import csv
import firebase_admin
from firebase_admin import credentials, firestore

# Connect to Firebase
cred = credentials.Certificate(
    r"C:\Users\anany\Downloads\serviceAccountKey.json"
)

firebase_admin.initialize_app(cred)
db = firestore.client()

# Read the bus dataset
with open("bus-data.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    batch = db.batch()
    count = 0

    for row in reader:
        stops = [
            stop.strip()
            for stop in row["stops"].split(";")
            if stop.strip()
        ]

        bus_data = {
            "id": row["id"],
            "busNumber": row["busNumber"],
            "description": row["description"],
            "stops": stops,
            "verified": False
        }

        document = db.collection("routes").document(str(row["id"]))
        batch.set(document, bus_data)

        count += 1

    batch.commit()

print(f"Successfully imported {count} bus routes!")
