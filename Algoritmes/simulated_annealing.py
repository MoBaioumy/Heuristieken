# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
from Objects.distance import distance
import Algoritmes

import numpy as np
import math
import random



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
        prop, h1, h2 = re_arrange(grid)

        # calculate difference of options
        current = grid.calculate_total_cost()
        proposed = current + prop

        # calculate probability of acceptance
        probability = max(0, min(1, np.exp(-(proposed - current) / T)))

        # if the proposed option is better than current, accept it
        if current > proposed:
            probability = 1

        # if option is worse, generate a random number between 0 and 1, if that
        # number is lower than the probability, make the swap
        if np.random.rand() < probability:
            grid.swap(h1, h2)

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

def re_arrange(grid):
    """
    Re-arrange for simulated_annealing
    """

    found = False
    house1 = False

    while found == False:

        # get random house_ids
        r1 = random.randint(1,150)
        r2 = random.randint(1,150)

        # find house 1
        while house1 == False:
            for battery in grid.batteries:
                for route in battery.routes:
                    if route.house.id == r1:

                        # save house 1 and battery 1
                        h1 = route
                        b1 = battery
                        max1 = h1.house.max_output + b1.current_capacity
                        house1 = True
                        break

        # find house 2
        for battery in grid.batteries:
            for route in battery.routes:
                if route.house.id == r2:

                    # save house 1 and battery 1
                    h2 = route
                    b2 = battery
                    max2 = h2.house.max_output + b2.current_capacity

                    # Find battery ids
                    bat1Index = None
                    bat2Index =  None
                    for idx, battery in enumerate(grid.batteries):
                        if battery.id == h1.battery_id:
                            bat1Index = idx
                        if battery.id == h2.battery_id:
                            bat2Index = idx

                    # if swap is possible, swap
                    if h1.house.max_output < max2 and h2.house.max_output < max1 and h1.battery_id != h2.battery_id:

                        # calculate is the swap improves the length of the connections
                        h1len = distance(h1.house.location, grid.batteries[bat2Index].location)
                        h2len = distance(h2.house.location, grid.batteries[bat1Index].location)
                        lengte_new = h1len + h2len
                        lengte_old = h1.length + h2.length

                        # stop while loop
                        found = True
                        break

        # in case we cannot find a house to swap with house 1, we need to reset the loop
        # without this you might get stuck in a loop
        house1 = False

    # return all the necessary information
    proposed = (lengte_new - lengte_old) * 9
    h1 = h1
    h2 = h2

    return proposed, h1, h2
