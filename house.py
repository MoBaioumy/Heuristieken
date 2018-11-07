class House(object):
    """
    Representation of a House in the SmartGrid assignment
    """

    def __init__(self, x_coordinate, y_coordinate, max_output):
        """
        Initialize an house, give it coordinates and a , description and room id
        """
        self.location = (int(x_coordinate), int(y_coordinate))
        self.max_output = int(max_output)
        self.closest_battery = []
        self.distance_closest_battery = []
        self.connected_battery = []
        self.distance_connected_battery = []
        self.id = id(self)

    def __str__(self):
        """
        Print name and description
        """
        return f"id: {self.id} x: {self.location[0]} y: {self.location[1]} capacity: {self.max_output}"
