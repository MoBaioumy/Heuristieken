import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route
from distance import distance
import random
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":

    i = 1
    wijk_naam = "wijk" + str(i)
    grid = Grid(wijk_naam)
    grid.draw_grid("No connections")
    grid.k_means(5)
    grid.draw_grid("No connections")
    
    
    

    
#    grid.random_hillclimber(0, 5)
#    grid.greed()
    grid.greedy()
    for house in grid.unconnected_houses:
        print(house)
    for battery in grid.batteries:
        print(battery.current_capacity)
    grid.hillclimber()
    grid.draw_grid("")
