# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
import Algoritmes

import numpy as np
import math


def simulated_annealing(grid, N, hill = 'False', accept = 'std', cooling = 'std'):

    """
    Simulated annealing
    """
    # parameters
    Tbegin = 100
    Tend = 0.01
    T = Tbegin

    for i in range(N):

        # get a proposition for a swap
        prop = grid.re_arrange()

        # calculate difference of options
        current = grid.calculate_total_cost()
        proposed = current + grid.proposed

        # calculate probability of acceptance
        if accept == 'std':
            probability = max(0, min(1, np.exp(-(proposed - current) / T)))
        # if the proposed option is better than current, accept it
        if current > proposed:
            probability = 1

        # if option is worse, generate a random number between 0 and 1, if that
        # number is lower than the probability, make the swap
        if np.random.rand() < probability:
            grid.swap(grid.h1, grid.h2)

        # geman parameters
        d = 2

        # cooling schemes
        # standard as a test
        if cooling == 'std':
            T = 0.999 * T
        # linear
        if cooling == 'lin':
            T = Tbegin - i * (Tbegin - Tend) / N
        # exponential
        if cooling == 'exp':
             T = Tbegin * math.pow(Tend / Tbegin, i / N)
        # sigmodial
        if cooling == 'sig':
            T = Tend + (Tbegin - Tend) / (1 + np.exp(0.3 * (i - N / 2)))
        # geman and geman
        if cooling == 'geman':
            T = Tbegin / (np.log(i + d))

    # end simulated_annealing with a hillclimber, to make sure there are no
    # more ways to improve the grid
    if hill == 'True':
        grid  = Algoritmes.hillclimber_greedy(grid)
    return grid
