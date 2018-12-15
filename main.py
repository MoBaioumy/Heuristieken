# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

# Internal imports
from Objects.grid import Grid
import Algoritmes

# External imports
import csv
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy

if __name__ == "__main__":

    i = 2
    wijk_naam = "wijk" + str(i)
    grid = Grid(wijk_naam)
    for bat in grid.batteries:
        print(bat)
    grid = Algoritmes.greedy(grid)
    for bat in grid.batteries:
        print(bat)

    grid.draw_grid("")
    grid = Algoritmes.hillclimber_random(grid)
    for bat in grid.batteries:
        print(bat)
    # # grid.re_arrange_random()
    # # grid.simple()
    grid.draw_grid("")
    # gridSimple = Algoritmes.greedy(grid)
    # gridSimple = Algoritmes.hillclimber_random(grid)
    # grid.draw_grid("")



#    grid.best_battery_number()
#     all_costs = []
#
#     for i in range(300):
#         try:
#             grid.verplaat_batterij_met_k_means(5)
#         except:
#             print("Can't do K_means")
#
#         grid = greedy_lookahead(grid)
#         grid = hillclimber(grid)
#         all_costs.append(grid.calculate_total_cost())
#         all_costs.append('$')
#         for j in range(5):
#             all_costs.append(grid.batteries[j].location[0])
#             all_costs.append(grid.batteries[j].location[1])
#
#         all_costs.append('&')
#
#
#     dt = datetime.now()
#     stdt = '{:%B-%d-%Y_%H%M}'.format(dt)
#     with open(f'Results/K_means/k_means_best_{wijk_naam}_{stdt}.json', 'w') as f:
#             json.dump(all_costs, f,indent=4)
#
#
#
#
#
#
#     grid.draw_grid("")
#
# #    grid.simulated_annealing(1000)
    # # costsGreedy = []
    # costsAlt = []
    # costsHillGreedy = []
    # costsHillAlt = []
    # for i in range(150):
    #     grid = greedy(grid)
    #     costsGreedy.append(grid.calculate_total_cost())
    #     grid = hillclimber(grid)
    #     costsHillGreedy.append(grid.calculate_total_cost())
    #     grid.disconnect_all()
    #     grid = greedy_alt(grid)
    #     costsAlt.append(grid.calculate_total_cost())
    #     grid = hillclimber(grid)
    #     costsHillAlt.append(grid.calculate_total_cost())
    #     grid.disconnect_all()
    #     print(f"Next!                  {i}                          Next!")
    #
    # print(f"Greedy, Min: {min(costsGreedy)} Max: {max(costsGreedy)} Mean: {np.mean(costsGreedy)}")
    # print(f"Alt Min: {min(costsAlt)} Max: {max(costsAlt)} Mean: {np.mean(costsAlt)}")
    # print(f"Hill --> Greedy, Min: {min(costsHillGreedy)} Max: {max(costsHillGreedy)} Mean: {np.mean(costsHillGreedy)}")
    # print(f"Hill --> Alt Min: {min(costsHillAlt)} Max: {max(costsHillAlt)} Mean: {np.mean(costsHillAlt)}")

#    grid.greed()
#    grid.draw_grid("greed")
#    grid.greedy()
#    grid.draw_grid("greedy")
#    grid.hillclimber()
#    grid.draw_grid("hillclimber")
#     grid.random()
    # grid.disconnect_all()
    # grid.random()
    # grid.disconnect_all()
#    grid.random()
    # grid.draw_grid("h")
    # for battery in grid.batteries:
    #     for route in battery.routes:
    #         print(route.house.id)

    # grid.draw_grid("")
    # grid.hillclimber_double()
    # grid.draw_grid("")
#    grid.shortest_paths()
#    print(sum(grid.shortest_paths()) * 9 + 25000)
#
#
#
#    grid.verplaat_batterij_met_k_means(5)
#    print(sum(grid.shortest_paths()) * 9 + 25000)
#    grid.draw_grid("No connections")





#    grid.random_hillclimber(0, 5)
#    grid.greed()
#    grid.greedy()
#    # grid.random_hillclimber(41000, 100)
#    for house in grid.unconnected_houses:
#        print(house)
#    for battery in grid.batteries:
#        print(battery.current_capacity)
#
#    grid.hillclimber()
#    grid.hillclimber_double()
#    grid.draw_grid("")
#
#
#    grid.calculate_total_cost()




    #    all_costs = []
#    for i in range(3):
#        grid.verplaat_batterij_met_k_means(5)
#        grid.greedy()
##        if grid.calculate_total_cost() < 4500:
##            continue
#        grid.hillclimber_double()
#        all_costs.append(grid.calculate_total_cost())
#


# =============================================================================
# code for user interface
# =============================================================================

#    def sel():
#       selection = "You selected the option " + str(var.get())
#       label.config(text = selection)
#
#    root = Tk()
#    var = IntVar()
#    R1 = Radiobutton(root, text="Wijk 1", variable=var, value=1,
#                      command=sel)
#    R1.pack( anchor = W )
#
#    R2 = Radiobutton(root, text="Wijk 2", variable=var, value=2,
#                      command=sel)
#    R2.pack( anchor = W )
#
#    R3 = Radiobutton(root, text="Wijk 3", variable=var, value=3,
#                      command=sel)
#    R3.pack( anchor = W)
#
#    label = Label(root)
#    label.pack()
#
#
#    root = Tk()
#    var = IntVar()
#    R1 = Radiobutton(root, text="Greedy Algorithme", variable=var, value=1,
#                      command=sel)
#    R1.pack( anchor = W )
#
#    R2 = Radiobutton(root, text="Random", variable=var, value=2,
#                      command=sel)
#    R2.pack( anchor = W )
#
#    R3 = Radiobutton(root, text="Random Hill Climber", variable=var, value=3,
#                      command=sel)
#    R3.pack( anchor = W)
#
#    R3 = Radiobutton(root, text="Greedy Hill Climber", variable=var, value=3,
#                      command=sel)
#    R3.pack( anchor = W)
#
#    label = Label(root)
#    label.pack()
#    root.mainloop()


# =============================================================================
# code for variable k_means
# =============================================================================

    #
    # all_costs = []
    # runs = 500
    #
    # for i in range(runs):
    #     try:
    #         grid.verplaat_batterij_met_k_means(5)
    #     except:
    #         print("Can't do K_means")
    #
    #     grid = greedy_lookahead(grid)
    #     grid = hillclimber(grid)
    #     all_costs.append(grid.calculate_total_cost())
    #     all_costs.append('$')
    #     for j in range(5):
    #         all_costs.append(grid.batteries[j].location[0])
    #         all_costs.append(grid.batteries[j].location[1])
    #
    # all_costs.append('&')
    # dt = datetime.now()
    # stdt = '{:%B-%d-%Y_%H%M}'.format(dt)
    # with open(f'Results/K_means/k_means_best_{wijk_naam}_{runs}_runs_{stdt}.json', 'w') as f:
    #         json.dump(all_costs, f,indent=4)
