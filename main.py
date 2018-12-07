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
    grid.draw_grid("No connections")
    grid.greedy()
    grid.draw_grid("")
    grid.verplaat_batterij_met_k_means(5)
    grid.disconnect_all()
    grid.greedy()
    grid.draw_grid("")
    grid.hillclimber()
    grid.draw_grid("")
    grid.hillclimber_double()
    grid.draw_grid("")
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
    
