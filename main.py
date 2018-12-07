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
    grid.greed()
    grid.draw_grid("greed")
    grid.greedy()
    grid.draw_grid("greedy")
    grid.hillclimber()
    grid.draw_grid("hillclimber")
    # grid.random()
    # grid.disconnect_all()
    # grid.random()
    # grid.disconnect_all()
    # grid.random()
    # grid.draw_grid("h")
    # for battery in grid.batteries:
    #     for route in battery.routes:
    #         print(route.house.id)
