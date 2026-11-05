from app.services.bus_service import get_all_buses


def normalize_stop(stop):
    """
    Convert a stop name into a consistent format.

    Supports either:
    - "Mangaluru"
    - {"name": "Mangaluru"}
    """

    if isinstance(stop, dict):
        stop = stop.get("name", "")

    if not isinstance(stop, str):
        return ""

    return " ".join(stop.strip().casefold().split())


def get_stop_names(bus):
    """
    Get the ordered stop list for a bus.
    """

    stops = bus.get("stops", [])

    if not isinstance(stops, list):
        return []

    return [
        normalize_stop(stop)
        for stop in stops
        if normalize_stop(stop)
    ]


def get_stop_display_name(bus, normalized_name):
    """
    Find the original display name of a stop.
    """

    for stop in bus.get("stops", []):
        if isinstance(stop, dict):
            name = stop.get("name", "")
        else:
            name = stop

        if normalize_stop(name) == normalized_name:
            return str(name)

    return normalized_name


def get_bus_duration(bus):
    """
    Get estimated journey duration in minutes.
    """

    duration = bus.get("duration_minutes", 0)

    try:
        return max(0, int(duration))
    except (ValueError, TypeError):
        return 0


def get_bus_fare(bus):
    """
    Get the bus fare.
    """

    fare = bus.get("fare", 0)

    try:
        return max(0, float(fare))
    except (ValueError, TypeError):
        return 0.0


def create_journey(bus, source, destination):
    """
    Create journey information for one bus.
    """

    stops = get_stop_names(bus)

    if source not in stops or destination not in stops:
        return None

    source_index = stops.index(source)
    destination_index = stops.index(destination)

    # Ensure the destination comes after the source
    if destination_index <= source_index:
        return None

    journey_stops = stops[source_index:destination_index + 1]

    return {
           
        "bus_id": bus.get("id"),
        "bus_number": bus.get("busNumber", "Not available"),
        "route_name": bus.get("description", "Not available"),
        "source": get_stop_display_name(bus, source),
        "destination": get_stop_display_name(bus, destination),
        "stops": [
            get_stop_display_name(bus, stop)
            for stop in journey_stops
        ],
        "duration_minutes": None,
        "fare": None,
        "timings": [],
        "bus_type": "Not specified"
      }


def search_direct_buses(buses, source, destination):
    """
    Find direct buses between source and destination.
    """

    direct_results = []

    for bus in buses:
        journey = create_journey(
            bus,
            source,
            destination
        )

        if journey:
            direct_results.append(journey)

        direct_results.sort(
            key=lambda item: item["bus_number"]
        )

    return direct_results


def search_connecting_buses(buses, source, destination):
    """
    Find journeys requiring one bus change.
    """

    connecting_results = []

    for first_bus in buses:

        first_stops = get_stop_names(first_bus)

        if source not in first_stops:
            continue

        source_index = first_stops.index(source)

        # Check every stop after the source as a possible interchange
        for interchange in first_stops[source_index + 1:]:

            first_journey = create_journey(
                first_bus,
                source,
                interchange
            )

            if not first_journey:
                continue

            for second_bus in buses:

                # Do not use the same bus twice
                if first_bus.get("id") == second_bus.get("id"):
                    continue

                second_journey = create_journey(
                    second_bus,
                    interchange,
                    destination
                )

                if not second_journey:
                    continue

                total_duration = None                
                total_fare = None
                connecting_results.append({
                    "journey_type": "connecting",
                    "source": first_journey["source"],
                    "destination": second_journey["destination"],
                    "interchange_stop": first_journey["destination"],
                    "total_duration_minutes": total_duration,
                    "total_fare":total_fare,
                    "buses": [
                        first_journey,
                        second_journey
                    ]
                })

    # Remove duplicate connections
    unique_results = []
    seen = set()

    for journey in connecting_results:
        first_bus_id = journey["buses"][0]["bus_id"]
        second_bus_id = journey["buses"][1]["bus_id"]

        key = (
            first_bus_id,
            second_bus_id,
            normalize_stop(journey["interchange_stop"])
        )

        if key not in seen:
            seen.add(key)
            unique_results.append(journey)

        unique_results.sort(
           key=lambda item: item["interchange_stop"]
        )
    return unique_results


def search_buses(source, destination):
    """
    Main search function.

    Returns direct and connecting bus options.
    """

    if not source or not destination:
        raise ValueError(
            "Source and destination are required."
        )

    normalized_source = normalize_stop(source)
    normalized_destination = normalize_stop(destination)

    if normalized_source == normalized_destination:
        raise ValueError(
            "Source and destination cannot be the same."
        )

    buses = get_all_buses()

    direct_results = search_direct_buses(
        buses,
        normalized_source,
        normalized_destination
    )

    connecting_results = search_connecting_buses(
        buses,
        normalized_source,
        normalized_destination
    )

    return {
        "source": source.strip(),
        "destination": destination.strip(),
        "direct_buses": direct_results,
        "connecting_buses": connecting_results,
        "total_direct_options": len(direct_results),
        "total_connecting_options": len(connecting_results)
    }