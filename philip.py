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

if __name__ == "__main__":


    grid = Grid("wijk3")
    grid.random()
    # grid.hillclimber()
    # grid.draw_grid("hill")
    grid.re_arrange_random(20000)
    grid.simulated_annealing(10000, hill = 'False', accept = 'std', cooling = 'sig')

    cost = grid.calculate_total_cost()
    print(cost)
    grid.re_arrange_random(100000)
    cost = grid.calculate_total_cost()
    print(cost)
    grid.hillclimber()
    # grid.draw_grid("annealing")
    cost2 = grid.calculate_total_cost()
    print(cost2)

    # grid.simulated_annealing(100000, hill = 'False', accept = 'std', cooling = 'geman')

    # grid.hillclimber()
    # grid.draw_grid("2nd")
    # cost = grid.calculate_total_cost()
    # print(cost)
    # grid.repeat_simulated_annealing(20000, iterations = 1, hill = 'True', cooling = 'exp')
