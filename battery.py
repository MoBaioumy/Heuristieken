from house import House
from distance import distance

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
        self.max_capacity = float(capacity)
        # keeps track of amount of capacity leftover
        self.current_capacity = float(capacity)
        self.type = bat_type
        self.cost = cost
        # id
        self.id = Battery.id
        Battery.id += 1
        # list of all routes from this battery
        self.routes = list()
        # route cost
        self.cost_routes = 0

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
        for route in self.routes:
            route.battery_location = self.location
            route.length = abs(route.house.location[0] - route.battery_location[0]) + abs(route.house.location[1] - route.battery_location[1])
            route.cost = route.length * route.cost_gridline
            route.grid_route = route.plan_grid_route()
            print(route.id)

    def find_closest_house(self, houses):
        smallest_distance = 100000000000000000000000000000000000
        smallest_distance_id = None
        for house in houses:
            dist = distance(house.location, self.location)
            if self.current_capacity > house.max_output:
                if dist < smallest_distance:
                    smallest_distance = dist
                    smallest_distance_id = house.id
        if smallest_distance_id == None:
            # print(f"No shortest distance found, probably because battery capacity is full. current capcity: {self.current_capacity}")
            return
        return smallest_distance_id

    def calculate_routes_cost(self):
        total_route_cost = sum([route.cost for route in self.routes])
        self.cost_routes =  total_route_cost
        return total_route_cost
