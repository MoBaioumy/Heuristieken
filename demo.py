import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route
from distance import distance
import random
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    i = 1
    wijk_naam = "wijk" + str(i)
    grid = Grid(wijk_naam)


    start = time.time()
    grid.greedy()
    stop = time.time()
    diff = stop - start
    grid.draw_grid( "Greedy, Time: " + str(round(diff, 2)) )


    start = time.time()
    grid.hillclimber()
    stop = time.time()
    diff = stop - start
    grid.draw_grid( "Hillclimber, Time: " + str(round(diff, 2)) )


    grid.disconnect_all()


    start = time.time()
    grid.random()
    stop = time.time()
    diff = stop - start
    grid.draw_grid( "Random Time: " + str(round(diff, 2)))


    start = time.time()
    grid.hillclimber()
    stop = time.time()
    diff = stop - start
    grid.draw_grid( "Hillclimber Time: " + str(round(diff, 2)) )
