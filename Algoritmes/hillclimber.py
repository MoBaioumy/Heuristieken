from Objects.house import House
from Objects.battery import Battery
from Objects.route import Route
from Objects.grid import Grid
from Objects.distance import distance


def hillclimber(grid):
    """
    This hillclimber algoritm checks if a swap between two houses can be made,
    and if so, if the swap would shorten the length of the path, if this is
    the case, the swap is made.
    """

    # set swap to true to start the loop
    swap = True

    # loops until no swaps can be made
    while swap == True:
        # sets swap to false
        swap = False
        # loops through the batteries
        for battery1 in grid.batteries:
            # loops through the houses in the batteries
            for route1 in battery1.routes:
                # loops through the batteries
                for battery2 in grid.batteries:
                    # loops through the houses in the batteries
                    for route2 in battery2.routes:
                        battery1cap = route1.house.max_output + battery1.current_capacity
                        battery2cap = route2.house.max_output + battery2.current_capacity
                        # checks if a swap between two houses can be made
                        if route1.house.max_output < battery2cap and route2.house.max_output < battery1cap:
                                # calculate is the swap improves the length of the connections
                                lengte_new =  distance(route1.house.location, battery2.location) + distance(route2.house.location, battery1.location)
                                lengte_old = route1.length + route2.length

                                # makes the swap if the length is improved
                                if swap == False and lengte_new < lengte_old and route1.house.id != route2.house.id:
                                    swap = grid.swap(route1, route2)
                                    break
    return grid
