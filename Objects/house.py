# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

class House(object):
    """
    Representation of a House in the SmartGrid assignment
    """
    # initiate id to 1
    id = 1
    def __init__(self, x_coordinate, y_coordinate, max_output):
        """
        Initialize an house, give it coordinates, assign maximum output and id
        """
        self.location = (int(x_coordinate), int(y_coordinate))
        self.max_output = float(max_output)

        # id
        self.id = House.id
        House.id += 1

    def __str__(self):
        """
        Print name and description
        """
        return f"id: {self.id} x: {self.location[0]} y: {self.location[1]} max output: {self.max_output}"
