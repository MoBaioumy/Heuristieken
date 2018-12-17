# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
import Algoritmes


# External imports
import csv
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy

from tkinter import Tk, Label, Frame, Button

if __name__ == "__main__":
    i = 3
    wijk = "wijk" + str(i)
    grid = Grid(wijk)
    # grid = Algoritmes.greedy_alt(grid)
    # print(grid.calculate_total_cost())
    for i in range(10):
        grid.disconnect_all()
        grid = Algoritmes.greedy_alt(grid)
        print(grid.calculate_total_cost())
