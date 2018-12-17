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

    while grid.unconnected_houses != []:
        for battery in grid.batteries:

            # find min output of unconnected houses
            if len(grid.unconnected_houses) == 1:
                min_out = grid.unconnected_houses[0].max_output
            elif len(grid.unconnected_houses) > 1:
                min_out = min(house.max_output for house in grid.unconnected_houses)
            else:
                break

            # only try to find a house if current_capacity is smaller than minimum output
            while battery.current_capacity > min_out:

                # find random house
                idx = random.randint(0, len(grid.unconnected_houses) - 1)
                house_id = grid.unconnected_houses[idx].id

                grid.connect(house_id, battery.id)

                if grid.unconnected_houses == []:
                    break
                else:
                    min_out = min(house.max_output for house in grid.unconnected_houses)

        # if no solution disconnect all houses and repeat
        if grid.unconnected_houses != []:
            grid.disconnect_all()

    return grid
