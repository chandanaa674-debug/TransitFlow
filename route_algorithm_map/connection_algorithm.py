
from sample_data import BUSES, STOPS, TRANSFER_WAIT_MINUTES
from distance_calculator import calculate_duration


def find_connecting_routes(source, destination):
    routes = []

    if source not in STOPS or destination not in STOPS:
        raise ValueError("Invalid source or destination stop")

    if source == destination:
        return routes

    for first_bus in BUSES:
        first_stops = first_bus["stops"]

        if source not in first_stops:
            continue

        source_index = first_stops.index(source)

        # Check possible interchange stops after the source.
        for interchange_index in range(
            source_index + 1, len(first_stops)
        ):
            interchange = first_stops[interchange_index]

            first_duration = calculate_duration(
                first_bus["segment_minutes"],
                source_index,
                interchange_index
            )

            first_route_stops = first_stops[
                source_index:interchange_index + 1
            ]

            for second_bus in BUSES:
                if first_bus["bus_number"] == second_bus["bus_number"]:
                    continue

                second_stops = second_bus["stops"]

                if interchange not in second_stops:
                    continue

                if destination not in second_stops:
                    continue

                interchange_second_index = second_stops.index(interchange)
                destination_index = second_stops.index(destination)

                # Destination must come after interchange.
                if interchange_second_index >= destination_index:
                    continue

                second_duration = calculate_duration(
                    second_bus["segment_minutes"],
                    interchange_second_index,
                    destination_index
                )

                second_route_stops = second_stops[
                    interchange_second_index:destination_index + 1
                ]

                # Do not invent journey durations when timing data is missing.
                if first_duration is None or second_duration is None:
                    total_duration = None
                else:
                    total_duration = (
                        first_duration
                        + TRANSFER_WAIT_MINUTES
                        + second_duration
                    )

                combined_stops = (
                    first_route_stops + second_route_stops[1:]
                )

                routes.append({
                    "type": "Connecting",
                    "bus_numbers": [
                        first_bus["bus_number"],
                        second_bus["bus_number"]
                    ],
                    "bus_names": [
                        first_bus["bus_name"],
                        second_bus["bus_name"]
                    ],
                    "stops": combined_stops,
                    "stop_names": [
                        STOPS[stop]["name"] for stop in combined_stops
                    ],
                    "transfer_stops": [STOPS[interchange]["name"]],
                    "transfers": 1,
                    "total_minutes": total_duration,
                    "segments": [
                        {
                            "bus_number": first_bus["bus_number"],
                            "bus_name": first_bus["bus_name"],
                            "stops": first_route_stops,
                            "duration_minutes": first_duration
                        },
                        {
                            "bus_number": second_bus["bus_number"],
                            "bus_name": second_bus["bus_name"],
                            "stops": second_route_stops,
                            "duration_minutes": second_duration
                        }
                    ]
                })

    return routes
