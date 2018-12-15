from Objects.grid import Grid
from Objects.distance import distance
import random

def hillclimber_random(grid, it = 10000):
    """
    Re-arrange for simulated_annealing
    """

    house1 = False
    i = 0
    swap = 0

    while i < it:

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
                            h1 = route
                            b1 = battery
                            max1 = h1.house.max_output + b1.current_capacity
                            house1 = True
                            break

            # find house 2
            for battery in grid.batteries:
                for route in battery.routes:
                    if route.house.id == r2:

                        h2 = route
                        b2 = battery
                        max2 = h2.house.max_output + b2.current_capacity

                        # if swap is possible, swap
                        if h1.house.max_output < max2 and h2.house.max_output < max1 and h1.house.id != h2.house.id:

                            i += 1

                            # calculate is the swap improves the length of the connections
                            
                            h1len = distance(h1.house.location, grid.batteries[h2.battery_id - 1].location)
                            h2len = distance(h2.house.location, grid.batteries[h1.battery_id - 1].location)
                            lengte_new = h1len + h2len
                            lengte_old = h1.length + h2.length

                            if lengte_new < lengte_old and h1.battery_id != h2.battery_id:
                                grid.swap(h1, h2)
                                swap = swap + 1

                            # stop while loop
                            found = True
                            break


            # in case we cannot find a house to swap with house 1, we need to reset the loop
            # without this you might get stuck in a loop
            house1 = False
    return grid
