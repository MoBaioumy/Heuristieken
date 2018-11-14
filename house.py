from operator import add

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
        self.location = (int(x_coordinate), int(y_coordinate))
        self.max_output = float(max_output)
        self.closest_battery = []
        self.distance_closest_battery = []
        self.connected_battery = []
        self.distance_connected_battery = []
        # id
        self.id = House.id
        House.id += 1

        # Thomas: I'm not sure if this methode can and should be implemented, you can't acces
        # information from the grid e.g. self.houses since a house object does not contain grid info
        # so maybe this method should be implemented in the grid
    def closest_battery(self, id):
        """
        Load houses and batteries first to Grid file to use this method
        """
        # obtain location of the house
        x_house = self.houses[id].location[0]
        y_house = self.houses[id].location[1]

        x_dif = []
        y_dif = []

        # calculate distances per x and y
        for i in range(5):
            x_dif.append(abs(x_house - self.batteries[i].location[0]))
            y_dif.append(abs(y_house - self.batteries[i].location[1]))

        # calculate overall distance
        man_distance = list(map(add, x_dif, y_dif))
        battery_id = man_distance.index(min(man_distance))

        return battery_id

    def __str__(self):
        """
        Print name and description
        """
        return f"id: {self.id} x: {self.location[0]} y: {self.location[1]} max output: {self.max_output}"
