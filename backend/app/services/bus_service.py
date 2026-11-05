from app.config.firebase import get_firestore_client


def get_all_buses():
    """
    Retrieve all buses from Firestore.
    """

    db = get_firestore_client()

    buses_collection = db.collection("buses")

    documents = buses_collection.stream()

    buses = []

    for document in documents:
        bus_data = document.to_dict() or {}

        bus_data["id"] = document.id

        # Skip buses explicitly marked inactive
        if bus_data.get("active") is False:
            continue

        buses.append(bus_data)

    return buses


def get_bus_by_id(bus_id):
    """
    Retrieve one bus using its Firestore document ID.
    """

    db = get_firestore_client()

    document = (
        db.collection("buses")
        .document(bus_id)
        .get()
    )

    if not document.exists:
        return None

    bus_data = document.to_dict() or {}

    bus_data["id"] = document.id

    if bus_data.get("active") is False:
        return None

    return bus_data