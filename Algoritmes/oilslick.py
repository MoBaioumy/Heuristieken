# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid

import copy

def oilslick(grid, N):
    """
    Oilslick calculates for each grid point how much output can reach that point in N amount of turns
    Each turn the output of a house will spread one segment in each direction

    This algorithm was written to determine the optimal position for batteries
    However it is not finished

    N = amount of turns
    """
    # generate tuple's of all coordinates
    coordinates = list()
    for x in range (0, 51):
        for y in range (0, 51):
            coordinates.append((x, y))

    # create representation of grid in dict
    grid_locations = {}
    for loc in coordinates:
        grid_locations[loc] = set([0])

    # place house max output values on location
    for house in grid.unconnected_houses:
        grid_locations[house.location] = set([house.max_output])

    counter = 0

    max = grid.batteries[0].max_capacity

    finished_locations = list()


    for i in range(N):
        # make structure to hold new values
        new_grid_locations = {}
        for location in coordinates:
            new_grid_locations[location] = set([0])

        # loop over grid locations
        for loc in grid_locations:

            # initiate
            up, down, left, right = None, None, None, None

            # up
            # if up exists
            if loc[1] < 50:
                # make up location
                up = (loc[0], loc[1] + 1)
                # if it is smaller than max cap battery
                temp = grid_locations[loc]|grid_locations[up]

            # down
            if loc[1] > 0:
                down = (loc[0], loc[1] - 1)
                temp = temp|grid_locations[down]

            # left
            if loc[0] > 0:
                left = (loc[0] - 1, loc[1])
                temp = temp|grid_locations[left]

            # right
            if loc[0] < 50:
                right = (loc[0] + 1, loc[1])
                temp = temp|grid_locations[right]

            new_grid_locations[loc] = temp
        del grid_locations
        grid_locations = copy.deepcopy(new_grid_locations)

    output_locations= []
    for i in grid_locations:
        if sum(grid_locations[i]) > max:
            output_locations.append(i)

    return output_locations
