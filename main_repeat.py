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
    This script runs the repeat algoritms. These algoritmes are used to find
    the best score. See for the parameters for the possible variations.
    """
    wijk = 2
    algoritme = 1 # 1 = repeat_simulated_annealing, 2 = repeat_hillclimber_greedy

    wijk_naam = "wijk" + str(wijk)
    grid = Grid(wijk_naam)

   if algoritme = 1:
        # # parameters
        N = 1 # number of iterations
        save = 'yes' # yes/no, save file to results
        compare = 'yes' # yes/no, compare simulated annealing with hillcimber
        sa_iterations = 100000 # number of simulated annealing repeats
        hill_iterations = 10000 # number of hillclimber iterations before simulated annealing
        hill = 'yes' # yes/no, hillclimber before simulated annealing
        begin = 'greedy' # random/greedy, start grid
        cooling = 'lin' # lin, sig, exp, geman, cooling scheme
        Tbegin = 50 # begin temperature
        Tend = 0.01 # end temperature

        grid = Algoritmes.repeat_simulated_annealing(grid, N = N, save = save, compare = compare,
        sa_iterations = sa_iterations, hill_iterations = hill_iterations, hill = hill,
        begin = begin, cooling = cooling, Tbegin = Tbegin, Tend = Tend)

    if algoritme = 2:

        # parameters
        repeats = 1
        save = 'yes' # yes/no, save file to results
        bound = 1 # bound stops at bad random results
        begin = 'greedy' # random/greedy, start grid
        grid = Algoritmes.repeat_hillclimber_greedy(grid, repeats = repeats,
        bound = bound, save = save, begin = begin)
