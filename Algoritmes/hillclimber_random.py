# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
from Objects.distance import distance
import random

def hillclimber_random(grid, iterations = 100000):
    """
    A version of the hillclimer that selects two houses at random.
    Requires grid as input.

    Optional parameters:

    iterations = number of iterations, (int), default: 100000

    """

    i = 0

    while i < iterations:

        found = False
        house1 = False

        while found == False:

            # get random house_ids
            r1 = random.randint(1,150)
            r2 = random.randint(1,150)

            # find house 1
            while house1 == False:
                for battery in grid.batteries:
                    for route in battery.routes:
                        if route.house.id == r1:

                            # save house 1 and battery 1
                            h1 = route
                            b1 = battery

                            # maximum avaliable output battery 1
                            max1 = h1.house.max_output + b1.current_capacity
                            house1 = True
                            break

            # find house 2
            for battery in grid.batteries:
                for route in battery.routes:
                    if route.house.id == r2:

                        # save house 1 and battery 1
                        h2 = route
                        b2 = battery

                        # maximum avaliable output battery 2
                        max2 = h2.house.max_output + b2.current_capacity

                        # check if swap is possible
                        if h1.house.max_output < max2 and h2.house.max_output < max1 and h1.house.id != h2.house.id:

                            i += 1

                            # find battery ids
                            bat1Index = None
                            bat2Index =  None
                            for idx, battery in enumerate(grid.batteries):
                                if battery.id == h1.battery_id:
                                    bat1Index = idx
                                if battery.id == h2.battery_id:
                                    bat2Index = idx

                            # calculate if the swap improves the length of the connections
                            h1len = distance(h1.house.location, grid.batteries[bat2Index].location)
                            h2len = distance(h2.house.location, grid.batteries[bat1Index].location)
                            lengte_new = h1len + h2len
                            lengte_old = h1.length + h2.length

                            # if the swap improves the length, make the swap
                            if lengte_new < lengte_old and h1.battery_id != h2.battery_id:
                                grid.swap(h1, h2)

                            # stop while loop
                            found = True
                            break

            # in case we cannot find a house to swap with house 1, we need to reset the loop
            # without this you might get stuck in the while loop
            house1 = False

    return grid
