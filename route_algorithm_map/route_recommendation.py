from sample_data import STOPS
from route_algorithm import find_direct_routes
from connection_algorithm import find_connecting_routes


def search_routes(source, destination):

    if source not in STOPS or destination not in STOPS:
        raise ValueError("Invalid source or destination stop")

    if source == destination:
        raise ValueError("Source and destination cannot be the same")

    direct_routes = find_direct_routes(source, destination)
    connecting_routes = find_connecting_routes(source, destination)

    all_routes = direct_routes + connecting_routes

    # Fastest route first; fewer transfers wins a tie.
    all_routes.sort(
        key=lambda route: (
            route["total_minutes"],
            route["transfers"]
        )
    )

    return all_routes