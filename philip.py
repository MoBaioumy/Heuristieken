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


    grid = Grid("wijk2")

    grid.repeat_simulated_annealing(20000, iterations = 10000, hill = 'True', cooling = 'exp')
