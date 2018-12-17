# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
import random

def random_connect(grid):
    """
    Randomly connects houses to batteries, if no solution, disconnect_all and repeat
    """
    # random.shuffle(grid.batteries)
    while grid.unconnected_houses != []:
        for battery in grid.batteries:


            min_out = min(house.max_output for house in grid.unconnected_houses)


            while battery.current_capacity > min_out:

                idx = random.randint(0, len(grid.unconnected_houses) - 1)
                house_id = grid.unconnected_houses[idx].id

                grid.connect(house_id, battery.id)

                if grid.unconnected_houses == []:
                    break
                else:
                    min_out = min(house.max_output for house in grid.unconnected_houses)
        if grid.unconnected_houses != []:
            grid.disconnect_all()

    return grid
