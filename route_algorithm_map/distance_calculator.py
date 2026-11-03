def calculate_duration(segment_minutes, start_index, end_index):
    """
    Calculate travel time between two positions
    in a bus's stop sequence.
    """
    if start_index < 0 or end_index >= len(segment_minutes) + 1:
        raise ValueError("Invalid stop index")

    if start_index >= end_index:
        raise ValueError("Destination must come after source")

    return sum(segment_minutes[start_index:end_index])