import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route
from distance import distance
import random
import numpy as np
import copy
import matplotlib.pyplot as plt

def re_arrange(grid):
    """
    Re-arrange for simulated_annealing
    """

    found = False

    while found == False:

        r1 = random.randint(1,150)

        for batteries in grid.batteries:
            for house in batteries.routes:
                print(house.id)
                if house.id == r1:

                    print('Found')
                    found = True
                    break

                    # h1 = h
                    # b1 = b
                    # max1 = h1.house.max_output + b1.current_capacity
                    # break

        # for b in grid.batteries:
        #     for h in b.routes:
        #         if h.id == r2:
        #             h2 = h
        #             b2 = b
        #             max2 = h2.house.max_output + b.current_capacity
        #             if h1.house.max_output < max2 and h2.house.max_output < max1:
        #                 hit = True
        #                 len_old = h1.length + h2.length
        #                 # calculate is the swap improves the length of the connections
        #                 h1len = distance(h1.house.location, grid.batteries[h2.battery_id - 1].location)
        #                 h2len = distance(h2.house.location, grid.batteries[h1.battery_id - 1].location)
        #                 len_new =  h1len + h2len
        #                 proposed = [h1, h2]
        #                 proposed_change = len_old - len_new
        #                 print(proposed)
        #                 print(proposed_change)
        #                 return proposed_change, h1, h2

#
# def re_arrange(grid):
#
#     hit = False
#     r1 = random.randint(1,150)
#     r2 = random.randint(1,150)
#
#     while hit == False:
#
#         for b in grid.batteries:
#             for h in b.routes:
#                 if h.id == r1:
#
#                     h1 = h
#                     b1 = b
#                     max1 = h1.house.max_output + b1.current_capacity
#                     print(h1)
#
#                     for b2 in grid.batteries:
#                         for h2 in b2.routes:
#                             if h2.id == r2:
#
#
#                                 h2 = h2
#                                 b2 = b2
#
#                                 max2 = h2.house.max_output + b2.current_capacity
#
#                                 if h1.house.max_output < max2 and h2.house.max_output < max1:
#
#                                     hit = True
#                                     len_old = h1.length + h2.length
#                                     # calculate is the swap improves the length of the connections
#                                     h1len = distance(h1.house.location, grid.batteries[h2.battery_id - 1].location)
#                                     h2len = distance(h2.house.location, grid.batteries[h1.battery_id - 1].location)
#                                     len_new =  h1len + h2len
#                                     current = grid.calculate_total_cost()
#                                     proposed_change = len_old - len_new
#                                     proposed = current + proposed_change
#                                     break
#
#
#             r1 = random.randint(1,150)
#             r2 = random.randint(1,150)

def simulated_annealing(grid, N):

    temperature = 100
    iterations = N
    best_version = copy.deepcopy(grid)
    best_possible = 35200
    best_cost = best_version.calculate_total_cost()
    fitness = []
    print('test')

    for i in range(N):

        proposed, current, h1, h2 = re_arrange(grid)
        proposed -= best_possible
        current -= best_possible

        probability = max(0, min(1, np.exp(-(proposed - current) / temperature)))

        if (current - proposed) > 0:
            probability = 1

        if np.random.rand() < probability:
            grid.swap(h1, h2)

        temperature = 0.99 * temperature
        cost = grid.calculate_total_cost()

        if cost < best_cost:
            best_version = copy.deepcopy(grid)
            best_cost = best_version.calculate_total_cost()

        fitness.append(best_cost)
        print(grid.unconnected_houses)

    return best_version, best_cost


if __name__ == "__main__":

    grid = Grid("wijk2")
    grid.random()
    print(grid.unconnected_houses)

    re_arrange(grid)
