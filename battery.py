from operator import add

class Battery(object):
    """
    Representation of a battery in the SmartGrid assignment
    """
    # initiate id to 1
    id = 1
    def __init__(self, x_coordinate, y_coordinate, bat_type, capacity, cost):
        """
        Initialize a battery, assign it coordinates, type, capacity and id
        """
        self.location = (int(x_coordinate), int(y_coordinate))
        # max capacity
        self.capacity = float(capacity)
        # keeps track of amount of capacity leftover
        self.current_capacity = float(capacity)
        self.type = bat_type
        self.cost = cost
        # id
        self.id = Battery.id
        Battery.id += 1
        # list of all houses that are connected to this battery
        self.connected_houses = list()

    def closest_house(self, id):
        """
        Load houses and batteries first to Grid file to use this method
        """
        # obtain location of the battery
        x_battery = self.batteries[id].location[0]
        y_battery = self.batteries[id].location[1]

        x_dif = []
        y_dif = []

        # calculate distances per x and y
        for i in range(150):
            x_dif.append(abs(x_battery - self.houses[i].location[0]))
            y_dif.append(abs(y_battery - self.houses[i].location[1]))

        # calculate overall distance
        man_distance = list(map(add, x_dif, y_dif))
        house_id = man_distance.index(min(man_distance))

        return house_id

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
