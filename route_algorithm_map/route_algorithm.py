from sample_data import BUSES, STOPS
from distance_calculator import calculate_duration


def find_direct_routes(source, destination):
    routes = []

    if source not in STOPS or destination not in STOPS:
        raise ValueError("Invalid source or destination stop")

    if source == destination:
        return routes

    for bus in BUSES:
        stops = bus["stops"]

        if source in stops and destination in stops:
            start_index = stops.index(source)
            end_index = stops.index(destination)

            # Bus must reach the destination after the source.
            if start_index < end_index:
                duration = calculate_duration(
                    bus["segment_minutes"],
                    start_index,
                    end_index
                )

                route_stops = stops[start_index:end_index + 1]

                routes.append({
                    "type": "Direct",
                    "bus_numbers": [bus["bus_number"]],
                    "bus_names": [bus["bus_name"]],
                    "stops": route_stops,
                    "stop_names": [
                        STOPS[stop]["name"] for stop in route_stops
                    ],
                    "transfer_stops": [],
                    "transfers": 0,
                    "total_minutes": duration,
                    "segments": [{
                        "bus_number": bus["bus_number"],
                        "bus_name": bus["bus_name"],
                        "stops": route_stops,
                        "duration_minutes": duration
                    }]
                })

    return routes