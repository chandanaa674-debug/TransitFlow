
import csv
import re
from pathlib import Path

CSV_FILE = Path(__file__).parent / "bus-data.csv"


def stop_key(name):
    """Convert a stop name into a consistent ID."""
    return re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")


def load_bus_data():
    buses = []
    stops_data = {}

    with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            stop_names = [
                name.strip()
                for name in row["stops"].split(";")
                if name.strip()
            ]

            stop_ids = []

            for name in stop_names:
                key = stop_key(name)
                stops_data[key] = {"name": name}
                stop_ids.append(key)

            buses.append({
                "bus_number": row["busNumber"].strip(),
                "bus_name": row["description"].strip(),
                "stops": stop_ids,

                # CSV has no travel-time information.
                "segment_minutes": [None] * max(0, len(stop_ids) - 1)
            })

    return buses, stops_data


BUSES, STOPS = load_bus_data()
