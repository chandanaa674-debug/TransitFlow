
from pathlib import Path
import folium

from sample_data import STOPS


def generate_route_map(route, output_file=None):

    if not route or not route.get("segments"):
        raise ValueError("No valid route provided")

    all_stop_ids = route["stops"]

    # Check that actual coordinates are available.
    missing_coordinates = [
        STOPS[stop]["name"]
        for stop in all_stop_ids
        if STOPS[stop].get("lat") is None
        or STOPS[stop].get("lon") is None
    ]

    if missing_coordinates:
        raise ValueError(
            "Map cannot be generated yet. Coordinates are missing for: "
            + ", ".join(missing_coordinates[:10])
        )

    coordinates = [
        [STOPS[stop]["lat"], STOPS[stop]["lon"]]
        for stop in all_stop_ids
    ]

    center_lat = sum(point[0] for point in coordinates) / len(coordinates)
    center_lon = sum(point[1] for point in coordinates) / len(coordinates)

    route_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles="OpenStreetMap"
    )

    for index, stop_id in enumerate(all_stop_ids):
        stop = STOPS[stop_id]

        if index == 0:
            color = "green"
        elif index == len(all_stop_ids) - 1:
            color = "red"
        else:
            color = "blue"

        folium.Marker(
            location=[stop["lat"], stop["lon"]],
            popup=stop["name"],
            tooltip=stop["name"],
            icon=folium.Icon(color=color)
        ).add_to(route_map)

    colors = ["blue", "purple", "orange"]

    for index, segment in enumerate(route["segments"]):
        segment_coordinates = [
            [STOPS[stop]["lat"], STOPS[stop]["lon"]]
            for stop in segment["stops"]
        ]

        folium.PolyLine(
            segment_coordinates,
            color=colors[index % len(colors)],
            weight=5,
            opacity=0.8,
            tooltip=f"Bus {segment['bus_number']}"
        ).add_to(route_map)

    if output_file is None:
        output_file = (
            Path(__file__).parent
            / "generated_maps"
            / "route_map.html"
        )
    else:
        output_file = Path(output_file)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    route_map.save(str(output_file))

    return str(output_file)

