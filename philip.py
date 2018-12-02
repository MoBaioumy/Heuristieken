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
    house1 = False
    while found == False:

        r2 = random.randint(1,150)

        while house1 == False:
            r1 = random.randint(1,150)
            for batteries in grid.batteries:
                for house in batteries.routes:
                    if house.id == r1:
                        h1 = house
                        b1 = batteries
                        max1 = h1.house.max_output + b1.current_capacity
                        house1 = True
                        break

        for batteries in grid.batteries:
            for house in batteries.routes:
                if house.id == r2:
                    h2 = house
                    b2 = batteries
                    max2 = h2.house.max_output + b2.current_capacity
                    if h1.house.max_output < max2 and h2.house.max_output < max1:

                        proposed = copy.deepcopy(grid)
                        proposed.swap(h1, h2)
                        found = True

                        break

        r1 = random.randint(1,150)
        r2 = random.randint(1,150)



    return proposed, h1, h2

def simulated_annealing(grid, N):

    temperature = 100
    iterations = N
    best_version = copy.deepcopy(grid)
    best_possible = 35200
    best_cost = best_version.calculate_total_cost()
    fitness = []

    for i in range(N):

        proposed, h1, h2 = re_arrange(grid)
        curr = grid.calculate_total_cost() - best_possible
        prop = proposed.calculate_total_cost() - best_possible
        probability = max(0, min(1, np.exp(-(prop - curr) / temperature)))

        if (curr - prop) > 0:
            probability = 1
            print("improvement ", curr - prop)

        cost = grid.calculate_total_cost()

        if np.random.rand() < probability:
            print('switch')
            grid = proposed

        temperature = 0.95 * temperature
        print(temperature)
        cost = grid.calculate_total_cost()

        if cost < best_cost:
            best_version = copy.deepcopy(grid)
            best_cost = best_version.calculate_total_cost()

        fitness.append(best_cost)

        print(cost)

    return best_version, best_cost


if __name__ == "__main__":

    grid = Grid("wijk2")
    grid.greedy()
    grid.hillclimber()
    print(grid.calculate_total_cost())
    re_arrange(grid)
    simulated_annealing(grid, 100)
