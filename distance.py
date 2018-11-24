def distance(location_1, location_2):
    """
    Made for the SmartGrid assignment for Programmeertheorie
    Take two location tuples as input
    Returns the manhattan distance between these locations
    """
    distance = abs(location_1[0] - location_2[0]) + abs(location_1[1] - location_2[1])
    return distance
