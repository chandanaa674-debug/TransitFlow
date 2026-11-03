# Demonstration data for Mangaluru bus routes.
# Stops, coordinates and timings are illustrative.

STOPS = {
    "state_bank": {
        "name": "State Bank",
        "lat": 12.8650,
        "lon": 74.8420
    },
    "hampankatta": {
        "name": "Hampankatta",
        "lat": 12.8690,
        "lon": 74.8430
    },
    "kankanady": {
        "name": "Kankanady",
        "lat": 12.8780,
        "lon": 74.8520
    },
    "pumpwell": {
        "name": "Pumpwell",
        "lat": 12.8895,
        "lon": 74.8580
    },
    "thokkottu": {
        "name": "Thokkottu",
        "lat": 12.8350,
        "lon": 74.8580
    },
    "lalbagh": {
        "name": "Lalbagh",
        "lat": 12.8790,
        "lon": 74.8450
    },
    "bejai": {
        "name": "Bejai",
        "lat": 12.8870,
        "lon": 74.8400
    }
}

BUSES = [
    {
        "bus_number": "101",
        "bus_name": "Demo Bus 101",
        "stops": [
            "state_bank",
            "hampankatta",
            "kankanady",
            "pumpwell"
        ],
        "segment_minutes": [5, 8, 7]
    },
    {
        "bus_number": "102",
        "bus_name": "Demo Bus 102",
        "stops": [
            "pumpwell",
            "kankanady",
            "thokkottu"
        ],
        "segment_minutes": [7, 12]
    },
    {
        "bus_number": "103",
        "bus_name": "Demo Bus 103",
        "stops": [
            "state_bank",
            "lalbagh",
            "bejai"
        ],
        "segment_minutes": [8, 6]
    }
]

# Assumed waiting time when changing buses.
TRANSFER_WAIT_MINUTES = 5