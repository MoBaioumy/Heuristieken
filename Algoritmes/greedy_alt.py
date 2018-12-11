from house import House
from battery import Battery
from route import Route
from distance import distance
from grid import Grid
import random
from Algoritmes.greedy import greedy

def greedy_alt(grid):
    """
    Alternative greedy algorithm that connects houses in order of output (high to low)
    Currently not working
    """
    # function that returns max output
    def max_output_func(house):
        return house.max_output

    counter = 0;
    while grid.unconnected_houses != []:
        # sort houses from smallest max output to largest
        grid.unconnected_houses.sort(key=max_output_func, reverse=True)


        for house in grid.unconnected_houses:
            smallest_dist = float('inf')
            closest_battery_id = None
            for battery in grid.batteries:
                dist = distance(house.location, battery.location)
                if dist < smallest_dist and battery.current_capacity > house.max_output:
                    closest_battery_id =  battery.id
                    smallest_dist = dist
            grid.connect(house.id, closest_battery_id)
        counter += 1
        if counter > 1000:
            break
    if grid.unconnected_houses != []:
        grid = greedy(grid)

    return grid
