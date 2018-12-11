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
import time
import math


def re_arrange(self, iterations = 1):
    """
    Re-arrange for simulated_annealing
    """

    found = False
    house1 = False
    count = 0

    while found == False:

        r1 = random.randint(1,150)
        r2 = random.randint(1,150)

        while house1 == False:
            for battery in grid.batteries:
                for route in battery.routes:
                    if route.house.id == r1:
                        h1 = route
                        b1 = battery
                        max1 = h1.house.max_output + b1.current_capacity
                        house1 = True
                        break

        for battery in grid.batteries:
            for route in battery.routes:
                if route.house.id == r2:

                    h2 = route
                    b2 = battery
                    max2 = h2.house.max_output + b2.current_capacity

                    if h1.house.max_output < max2 and h2.house.max_output < max1 and h1 != h2:

                        proposed = copy.deepcopy(grid)
                        proposed.swap(h1, h2)
                        found = True
                        break

        house1 = False

    return proposed, h1, h2

def simulated_annealing(grid, N, hill = 'True', cooling = 'standard'):

    temperature = 100
    begin_temperature = 100

    for i in range(N):

        prop, h1, h2 = re_arrange(grid)
        current = grid.calculate_total_cost()
        proposed = prop.calculate_total_cost()
        probability = max(0, min(1, np.exp(-(proposed - current) / temperature)))

        if (current - proposed) > 0:
            probability = 1

        cost = grid.calculate_total_cost()

        if np.random.rand() < probability:
            grid.swap(h1, h2)

        if cooling == 'standard':
            temperature = 0.999 * temperature
        if cooling == 'linear':
            temperature = begin_temperature - i * (begin_temperature - 0) / N
        if cooling == 'exponential':
             temperature = begin_temperature * math.pow(1 / begin_temperature, i / N)

    if hill == 'True':
        grid.hillclimber()

    return grid


if __name__ == "__main__":


    grid = Grid("wijk2")

    grid.repeat_simulated_annealing(1000,1000, begin = 'random', bound = 46000)
