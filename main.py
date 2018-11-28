import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route
from distance import distance
import random
import matplotlib.pyplot as plt

if __name__ == "__main__":

    i = 2
    wijk_naam = "wijk" + str(i)
    grid = Grid(wijk_naam)
    grid.greedy()
    grid.hillclimber()
    print(grid.unconnected_houses)
