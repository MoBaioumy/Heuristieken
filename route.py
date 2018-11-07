class Route(object):
    """
    Representation of a route object in the SmartGrid assignment
    """
    def __init__(self, battery, house):
        self.house = house
        self.battery = battery
        self.length = abs(self.house.location[0] - self.battery.location[0]) + abs(self.house.location[1] - self.battery.location[1])
        cost_gridline = 9
        self.cost = self.length * cost_gridline

    def __str__(self):
        """
        Print description
        """
        return f"this route connects: {self.house.id} and {self.battery.id}"
