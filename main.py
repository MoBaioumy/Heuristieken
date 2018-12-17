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

# =============================================================================
#     The following blocks of code are for the user interface
# =============================================================================

    # event listener for button wijk 1
    def wijk_1():
        # get global value i (the value of i in the main program)
        global i
        i = 1
        # destroy root to close the GUI
        root.destroy()
        return i

    # event listener for button wijk 2
    def wijk_2():
        global i
        i = 2
        root.destroy()
        return i

    # event listener for button wijk 1
    def wijk_3():
        global i
        i = 3
        root.destroy()
        return i

    """\
    The following functions will be executed when the matching button
    is clicked in the user interface.
    Basically the grid is imported in the function as a local variable then
    the algorithme is executed, then the grid is drawn.
    """
    def greedy():
        global grid
        grid.disconnect_all()
        grid = Algoritmes.greedy(grid)
        grid.draw_grid("")

    def greedy_look_ahead():
        global grid
        grid.disconnect_all()
        grid = Algoritmes.greedy_lookahead(grid)
        grid.draw_grid("")

    def hill_climber_greedy():
        global grid
        grid = Algoritmes.hillclimber_greedy(grid)
        grid.draw_grid("")

    def k_means():
        global grid
        grid = Algoritmes.k_means(grid)
        grid.draw_grid("")

    def repeat_simulated_annealing():
        global grid
        grid = Algoritmes.repeat_simulated_annealing(grid)
        grid.draw_grid("")

    def random_connect():
        global grid
        grid = Algoritmes.random_connect(grid)
        grid.draw_grid("")


    # after the first window with wijken is closed, the one with algrithms opens
    def alg_window():
        # start thinker root
        root = Tk()

        # create a frame and add a label to ask for an option
        bottom_frame = Frame(root)
        bottom_frame.pack()

        welcome_label = Label(bottom_frame, text="Kies het algoritme")
        welcome_label.pack()

        # create all the buttons
        button_greedy_look_ahead = Button(bottom_frame, text = "Greedy Look ahead", fg="Blue",command=greedy)
        button_greedy_look_ahead.pack(side='bottom')

        button_greedy = Button(bottom_frame, text = "Greedy", fg="Blue",command=greedy_look_ahead)
        button_greedy.pack(side='bottom')

        button_hill_climber_greedy = Button(bottom_frame, text = "Hill Climber Greedy", fg="Blue",command=hill_climber_greedy)
        button_hill_climber_greedy.pack(side='bottom')

        button_k_means = Button(bottom_frame, text = "K means", fg="Blue",command=k_means)
        button_k_means.pack(side='bottom')

        button_random = Button(bottom_frame, text = "Random", fg="Blue",command=random_connect)
        button_random.pack(side='bottom')

        # close the main loop (when the window is closed)
        root.mainloop()

    # this will be executed first
    root = Tk()
    # create frame
    top_frame = Frame(root)
    top_frame.pack()

    # Label to ask for an algorithm to be selected
    welcome_label = Label(top_frame, text="Kies de wjik")
    welcome_label.pack()

    # create 3 button to ask for the wijk
    button_1 = Button(top_frame, text = "Wijk 1", fg="green", command=wijk_1)
    button_1.pack(side='left')
    button_2 = Button(top_frame, text = "Wijk 2", fg="green", command=wijk_2)
    button_2.pack(side='left')
    button_3 = Button(top_frame, text = "Wijk 3", fg="green", command=wijk_3)
    button_3.pack(side='left')
    # close main loop
    root.mainloop()

    # assign the right value and create the grid object
    wijk_naam = "wijk" + str(i)
    grid = Grid(wijk_naam)

    # start the algorithm window
    alg_window()
