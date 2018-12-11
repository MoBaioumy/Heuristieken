from house import House
from battery import Battery
from route import Route
from distance import distance


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
        for b1 in grid.batteries:
            # loops through the houses in the batteries
            for h1 in b1.routes:
                # loops through the batteries
                for b2 in grid.batteries:
                    # loops through the houses in the batteries
                    for h2 in b2.routes:
                        h1cap = h1.house.max_output + b1.current_capacity
                        h2cap = h2.house.max_output + b2.current_capacity
                        # checks if a swap between two houses can be made
                        if h1.house.max_output < h2cap and h2.house.max_output < h1cap:
                                # calculate is the swap improves the length of the connections
                                h1len = distance(h1.house.location, grid.batteries[h2.battery_id - 1].location)
                                h2len = distance(h2.house.location, grid.batteries[h1.battery_id - 1].location)
                                lengte_new =  h1len + h2len
                                lengte_old = h1.length + h2.length

                                # makes the swap if the length is improved
                                if swap == False and lengte_new < lengte_old and h1.house.id != h2.house.id and :
                                    swap = grid.swap(h1, h2)
                                    break
