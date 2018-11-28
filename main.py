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
<<<<<<< HEAD
    grid.greedy()
    grid.hillclimber()
    print(grid.unconnected_houses)
=======

    grid.random_hillclimber(0, 100)
>>>>>>> bd3b3bb215fdef41de9e87c1c39c4633bce13a59
