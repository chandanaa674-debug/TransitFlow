def calculate_duration(segment_minutes, start_index, end_index):
    if start_index < 0 or end_index > len(segment_minutes):
        raise ValueError("Invalid stop index")

    if start_index >= end_index:
        raise ValueError("Destination must come after source")

    selected_segments = segment_minutes[start_index:end_index]

    if any(minutes is None for minutes in selected_segments):
        return None

    return sum(selected_segments)