# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

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


    def move(self, location):
        """
        Move battery to new x/y location
        """
        # new location
        self.location = location

        # update routes
        for route in self.routes:
            route.battery_location = self.location
            route.length = abs(route.house.location[0] - route.battery_location[0]) + abs(route.house.location[1] - route.battery_location[1])
            route.cost = route.length * route.cost_gridline
            route.grid_route = route.plan_manhattan_grid_route()
            print(route.id)

        # update cost of routes
        self.cost_routes = self.calculate_routes_cost()

        print(f"Moved battery {self.id} to {self.location}")


    def find_closest_house(self, houses):
        """
        Finds the closest house to this battery in input list
        """
        # initiate
        smallest_distance = float('inf')
        smallest_distance_house = None

        # loop over houses to find closest house
        # checks if this house can fit current capcity of the battery
        for house in houses:
            dist = distance(house.location, self.location)
            if self.current_capacity > house.max_output:
                if dist < smallest_distance:
                    smallest_distance = dist
                    smallest_distance_house = house

        if smallest_distance_house == None:
            # print(f"No shortest distance found, probably because battery capacity is full. current capcity: {self.current_capacity}")
            return
        return smallest_distance_house


    def calculate_routes_cost(self):
        """
        Sums the cost of all connected routes
        """
        total_route_cost = sum([route.cost for route in self.routes])
        self.cost_routes =  total_route_cost
        return total_route_cost
