class Route(object):
    """
    Representation of a route object in the SmartGrid assignment
    """
    # initiate id to 1
    id = 1
    def __init__(self, house, battery_id, battery_location):
        # route id
        self.id = Route.id
        Route.id += 1
        # def house and battery connected by route
        self.house = house
        self.battery_id = battery_id
        self.battery_location - battery_location
        # calculate manhattan distance
        self.length = abs(self.house.location[0] - self.battery.location[0]) + abs(self.house.location[1] - self.battery.location[1])
        # calculate cost
        cost_gridline = 9
        self.cost = self.length * cost_gridline
        # set route
        self.grid_route = list()
        self.grid_route = self.plan_grid_route()


    def __str__(self):
        """
        Print description
        """
        return f"this route connects house: {self.house.id} and battery: {self.battery.id}"

    def plan_grid_route(self):
        """
        Plan a grid route by first moving all spaces on x axis then on y axis
        """
        # initiate empty list to append to and return at end
        grid_route = list()
        # calculate the distance between x locations
        distance_x = self.house.location[0] - self.battery.location[0]
        # calculate the distance between y locations
        distance_y = self.house.location[1] - self.battery.location[1]
        # initiate current location that will be updated to house location
        current_location = self.house.location

        for i in range(0, distance_x):
            print(i)
        # loop over x axis update location in steps of 1
        for i in range(abs(distance_x)):
            # if difference is positive  increment with - 1
            if distance_x > 0:
                current_location = (current_location[0] - 1, current_location[1])
                grid_route.append(current_location)
            # else increment with + 1
            elif distance_x < 0:
                current_location = (current_location[0] + 1, current_location[1])
                grid_route.append(current_location)
        # loop over y axis update location in steps of 1 same method
        for i in range(abs(distance_y)):
            if distance_y > 0:
                current_location = (current_location[0], current_location[1] - 1)
                grid_route.append(current_location)
            elif distance_y < 0:
                current_location = (current_location[0], current_location[1] + 1)
                grid_route.append(current_location)
        # return list of coordinates of grid_route
        return grid_route
