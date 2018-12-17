# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
import Algoritmes


# External imports
import csv
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy

if __name__ == "__main__":
    """
    This script runs the algoritms seperately without a gui interface
    """

    wijk = 2
    wijk_naam = "wijk" + str(wijk)
    grid = Grid(wijk_naam)

    # 1 = random
    # 2 = greedy
    # 3 = hillclimer
    # 4 = hillclimber_random
    # 5 = k_means
    # 6 = simulated annealing
    algoritme = 6

    # random
    if algoritme == 1:

        grid = Algoritmes.random_connect(grid)
        cost = grid.calculate_total_cost()
        print("Cost of solution:", cost)

    # greedy
    if algoritme == 2:

        grid = Algoritmes.greedy_lookahead(grid)
        cost = grid.calculate_total_cost()
        print("Cost of solution:", cost)

    # hillclimber
    if algoritme == 3:

        grid = Algoritmes.greedy_lookahead(grid)
        grid = Algoritmes.hillclimber_greedy(grid)
        cost = grid.calculate_total_cost()
        print("Cost of solution:", cost)

    # hillclimber_random
    if algoritme == 4:

        grid = Algoritmes.greedy_lookahead(grid)
        grid = Algoritmes.hillclimber_random(grid)
        cost = grid.calculate_total_cost()
        print("Cost of solution:", cost)

    # k_means
    if algoritme == 5:

        grid = Algoritmes.k_means(grid)
        grid = Algoritmes.greedy_lookahead(grid)
        grid = Algoritmes.hillclimber_greedy(grid)
        cost = grid.calculate_total_cost()
        print("Cost of solution:", cost)

    # simulated annealing
    if algoritme == 6:

        grid = Algoritmes.greedy_lookahead(grid)
        grid = Algoritmes.hillclimber_random(grid)
        grid = Algoritmes.simulated_annealing(grid, N = 100000, Tbegin = 50, Tend = 0.01, cooling = 'sig')
        cost = grid.calculate_total_cost()
        print("Cost of solution:", cost)
