import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route
from distance import distance
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == "__main__":

    grid = Grid("wijk2")

    grid.repeat_simulated_annealing(1000,1000)
