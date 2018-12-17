# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
from Objects.distance import distance
import Algoritmes
import itertools
import random
import numpy as np


def greedy_lookahead(grid, N = 4, break_n = 500):
    """
    Greedy lookahead will find the house with the shortest distance to a battery
    When a batteries current capacity goes between a certain range the algortim will call the look function
    This look function will look at all possible combinations of houses to fill this battery
    Look will return the combination of houses with the shortest distance
    N =  the average amount of houses you wish to look ahead
    break_n =  is the number of iterations you want the algorithm to try finding a solution
    """
    # initiate counter that will determine when to break
    counter = 0

    # get all outputs
    all_outputs = [house.max_output for house in grid.unconnected_houses]

    # repeat till solution is found
    while grid.unconnected_houses != []:

        # best_dist is the best score on distance
        best_dist = float('inf')

        # loop over houses that are not connected
        for house in grid.unconnected_houses:

            #  finds the lowest distance to battery for each house
            # select the house with the lowest distance
            lowest_dist_house = float('inf')
            for battery in grid.batteries:
                dist = distance(house.location, battery.location)
                if dist < lowest_dist_house and battery.current_capacity > house.max_output and battery.current_capacity > np.mean(all_outputs) * N:
                    bat_id = battery.id
                    house_id = house.id
                    lowest_dist_house = dist
                elif min(all_outputs) < battery.current_capacity < np.mean(all_outputs) * N:
                    if 0 < grid.range_connected(battery)[1] < 8:
                        houses = look(grid, battery)
                        for h in houses:
                            grid.connect(h.id, battery.id)

            if lowest_dist_house < best_dist:
                connect_bat_id = bat_id
                connect_house_id = house_id
                best_dist = lowest_dist_house

        # connect house with lowest distance to closest battery
        grid.connect(connect_house_id, connect_bat_id)

        # break if stuck in infinit loop after certain n
        counter += 1
        if counter > break_n:
            break

    # fill remaining grid if needed
    if grid.unconnected_houses != []:
        grid = Algoritmes.greedy(grid)

    return grid


def look(grid, battery):
    """
    Look will find the best combination of houses to fill the current capacity of input battery,
    with the shortest total distance
    """
    # get min and max of houses able to connect to battery
    range_con = grid.range_connected(battery)

    # initiate
    lowest_combination =  [0, 0]
    all_outputs = [house.max_output for house in grid.unconnected_houses]
    best_dist = float('inf')
    out_houses = []

    # in range of able to connect houses generate all possible combinations of house outputs
    for i in range(range_con[1]):

        # generate combination
         combinations = itertools.combinations(all_outputs, i)

         # find lowest combination
         for combi in combinations:
             if 0 < battery.current_capacity - sum(combi)  < battery.current_capacity - sum(lowest_combination) and battery.current_capacity - sum(combi) < 5:

                 # find houses
                 houses = []
                 for output in combi:
                     for house in grid.unconnected_houses:
                         if house.max_output == output:
                             houses.append(house)

                 # calculate total distance
                 total_dist = 0
                 for h in houses:
                     total_dist += distance(h.location, battery.location)

                 # if current combination has better distance save combination
                 if total_dist < best_dist:
                     best_dist = total_dist
                     lowest_combination = combi
                     out_houses = houses

    return out_houses
