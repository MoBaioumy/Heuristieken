from Objects.grid import Grid
import random
import Algoritmes

def greedy_alt(grid):
    """
    Alternative greedy algorithm that connects houses in order of output (high to low)
    """
    # function that returns max output
    def max_output_func(house):
        return house.max_output

    counter = 0;
    while grid.unconnected_houses != []:
        # sort houses from largest to smallest
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

    # fill last part greedy if needed
    if grid.unconnected_houses != []:
        grid = greedy(grid)

    return grid
