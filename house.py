class House(object):
    """
    Representation of a House in the SmartGrid assignment
    """
    # initiate id to 1
    id = 1
    def __init__(self, x_coordinate, y_coordinate, max_output):
        """
        Initialize an house, give it coordinates and a , description and room id
        """
        # tuple with x/y location
        self.location = (int(x_coordinate), int(y_coordinate))
        # output
        self.max_output = max_output
        # potential information in regard to batteries
        self.closest_battery = []
        self.distance_closest_battery = []
        self.connected_battery = []
        self.distance_connected_battery = []
        # id
        self.id = House.id
        House.id += 1

    def __str__(self):
        """
        Print name and description
        """
        return f"id: {self.id} x: {self.location[0]} y: {self.location[1]} capacity: {self.max_output}"
