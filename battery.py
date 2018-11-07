class Battery(object):
    """
    Representation of a battery in the SmartGrid assignment
    """
    # initiate id to 1
    id = 1
    def __init__(self, x_coordinate, y_coordinate, bat_type, capacity):
        """
        Initialize a battery, assign it coordinates, type, capacity and id
        """
        # location = tuple with coordinates
        self.location = (int(x_coordinate), int(y_coordinate))
        # both keep track of max cap and current capactity (when houses are connected current capacity reduces)
        self.max_capacity = capacity
        self.current_capacity = capacity
        # type and id
        self.type = bat_type
        self.id = Battery.id
        Battery.id += 1
        # list of all houses that are connected to this battery
        self.connected_houses = list()

    def __str__(self):
        """
        Print description
        """
        return f"id: {self.id} type: {self.type} x: {self.location[0]} y: {self.location[1]} capacity: {self.max_capacity}"

    def move(self, new_x, new_y):
        """
        Move battery to new x/y location
        """
        self.location = (new_x, new_y)
