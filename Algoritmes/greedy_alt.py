# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
from Objects.distance import distance
import random
import Algoritmes

MAX_ITERATIONS = 1000

def greedy_alt(grid):
    """
    Alternative greedy algorithm that connects houses in order of
    output (high to low)
    """

    def max_output_func(house):
        """
        returns max output of a specified house.
        """
        return house.max_output

    counter = 0;
    while grid.unconnected_houses != []:
        # sort houses from largest to smallest
        grid.unconnected_houses.sort(key=max_output_func, reverse=True)

        for house in grid.unconnected_houses:
            # for the unconnected_houses, intialize the distance to infinity
            # and make sure it doen't have a closet battery
            smallest_dist = float('inf')
            closest_battery_id = None

            # if there is capacity left, connect the house to closet battery
            for battery in grid.batteries:
                dist = distance(house.location, battery.location)
                if dist < smallest_dist and battery.current_capacity > house.max_output:
                    closest_battery_id =  battery.id
                    smallest_dist = dist
            grid.connect(house.id, closest_battery_id)
        counter += 1
        if counter > MAX_ITERATIONS:
            break

    # fill last part with the other greedy if needed
    if grid.unconnected_houses != []:
        grid = Algoritmes.greedy(grid)

    return grid
