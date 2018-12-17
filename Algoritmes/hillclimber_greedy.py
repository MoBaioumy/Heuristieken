# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
from Objects.distance import distance


def hillclimber_greedy(grid):
    """
    This hillclimber algoritm checks if a swap between two houses can be made,
    and if so, if the swap would shorten the length of the path, if this is
    the case, the swap is made.

    Requires the grid as input.
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
                        b1cap = h1.house.max_output + b1.current_capacity
                        b2cap = h2.house.max_output + b2.current_capacity
                        # checks if a swap between two houses can be made
                        if h1.house.max_output < b2cap and h2.house.max_output < b1cap:
                                # calculate is the swap improves the length of the connections
                                len_new =  distance(h1.house.location, b2.location) + distance(h2.house.location, b1.location)
                                len_old = h1.length + h2.length

                                # makes the swap if the length is improved
                                if swap == False and len_new < len_old and h1.house.id != h2.house.id:
                                    swap = grid.swap(h1, h2)
                                    break
    return grid
