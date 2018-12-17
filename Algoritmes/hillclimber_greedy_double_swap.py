# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
from Objects.distance import distance
import Algoritmes


def hillclimber_greedy_double_swap(grid):
    """
    This hillclimber algoritm checks if a swap between pairs of two houses can be made,
    and if so, if the swap would shorten the length of the path, if this is
    the case, the swap is made.
    """
    swap = True
    # loops until no swaps can be made
    while swap == True:
        # sets swap to false
        swap = False
        grid  = Algoritmes.hillclimber_greedy(grid)
        # loops through the batteries
        for b1 in grid.batteries:
            for h1 in b1.routes:
                for h2 in b1.routes:
                    for b2 in grid.batteries:
                        for h3 in b2.routes:
                            for h4 in b2.routes:

                                h1h2 = h1.house.max_output + h2.house.max_output
                                h3h4 = h3.house.max_output + h4.house.max_output
                                cap1 = h1h2 + b1.current_capacity
                                cap2 = h3h4 + b2.current_capacity

                                if h1 != h2 and h3 != h4 and h1h2 < cap2 and h3h4 < cap1:

                                    len_old = h1.length + h2.length + h3.length + h4.length

                                    # Find battery ids
                                    bat1Index = None
                                    bat3Index =  None
                                    for idx, battery in enumerate(grid.batteries):
                                        if battery.id == h1.battery_id:
                                            bat1Index = idx
                                        if battery.id == h3.battery_id:
                                            bat3Index = idx

                                    # get all distances
                                    d1 = distance(h1.house.location, grid.batteries[bat3Index].location)
                                    d2 = distance(h2.house.location, grid.batteries[bat3Index].location)
                                    d3 = distance(h3.house.location, grid.batteries[bat1Index].location)
                                    d4 = distance(h4.house.location, grid.batteries[bat1Index].location)

                                    len_new = d1 + d2 + d3 + d4

                                    # makes the swap if the length is improved
                                    if swap == False and len_new < len_old:

                                        swap = grid.swap(h1, h2, h3, h4)
                                        break
    return grid
