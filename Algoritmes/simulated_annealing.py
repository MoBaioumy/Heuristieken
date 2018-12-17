# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
import Algoritmes

import numpy as np
import math


def simulated_annealing(grid, N, Tbegin = 100, Tend = 0.01, cooling = 'lin'):
    """
    Simulated annealing algoritm. Description:

    Requires grid as input.
    Requires iterations N as input (int).

    Optional input:
    
    Tbegin = int, default 100, begin temperature of simulated annealing
    Tend = float, default 0.01, end temperature of simulated annealing
    cooling = 'lin', 'exp', 'sig', 'geman', default 'lin'. Cooling scheme,
    user can choose between a linear cooling scheme, exponential cooling
    scheme, sigmodial cooling scheme and the Geman and Geman cooling scheme.
    """

    T = Tbegin

    for i in range(N):

        # get a proposition for a swap
        prop = grid.re_arrange()

        # calculate difference of options
        current = grid.calculate_total_cost()
        proposed = current + grid.proposed

        # calculate probability of acceptance
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

    return grid
