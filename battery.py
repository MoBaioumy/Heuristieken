class Battery(object):
    """
    Representation of a battery in the SmartGrid assignment
    """

    def __init__(self, x_coordinate, y_coordinate, bat_type, capacity):
        """
        Initialize a battery, assign it coordinates, type, capacity and id
        """
        self.location = (x_coordinate, y_coordinate)
        self.capacity = capacity
        self.type = bat_type
        self.id = id(self)
        self.connected_houses = list()

    def __str__(self):
        """
        Print description
        """
        return f"id: {self.id} type: {self.type} x: {self.location[0]} y: {self.location[1]} capacity: {self.capacity}"
