from .sample_data import STOPS
from .route_recommendation import search_routes
from .map_generator import generate_route_map


def main():

    # Example journey
    source = "state_bank"
    destination = "thokkottu"

    print("\n========== TRANSITFLOW ROUTE SEARCH ==========")

    print(f"From: {STOPS[source]['name']}")
    print(f"To:   {STOPS[destination]['name']}")

    routes = search_routes(source, destination)

    if not routes:
        print("\nNo routes found.")
        return

    for index, route in enumerate(routes, start=1):

        print(f"\nRoute {index}")
        print("----------------------------------")
        print("Journey type:", route["type"])
        print("Buses:", " -> ".join(route["bus_numbers"]))
        print("Stops:", " -> ".join(route["stop_names"]))
        print("Transfers:", route["transfers"])
        print("Estimated time:", route["total_minutes"], "minutes")

        if route["transfer_stops"]:
            print("Change bus at:", ", ".join(route["transfer_stops"]))

    best_route = routes[0]

    print("\n========== BEST ROUTE ==========")
    print("Buses:", " -> ".join(best_route["bus_numbers"]))
    print("Estimated time:", best_route["total_minutes"], "minutes")
    print("Change bus at:", ", ".join(best_route["transfer_stops"]))

    map_path = generate_route_map(best_route)

    print("\nMap generated successfully!")
    print("Map location:", map_path)
    print("\nOpen the HTML file in your browser to view the map.")


if __name__ == "__main__":
    main()