from house import House
from battery import Battery
from route import Route
from distance import distance
from grid import Grid
import itertools
import random
from Algoritmes import greedy

def look(grid, battery):
    r = grid.range_connected(battery)
#    print(r)
    lowest_combination =  [0, 0]
    all_outputs = [house.max_output for house in grid.unconnected_houses]
    best_dist = float('inf')
    out_houses = []
    for i in range(r[1]):
         combinations = itertools.combinations(all_outputs, i)
#         print("progress!")
         for combi in combinations:
             # print(sum(j) - battery.current_capacity)
             if 0 < battery.current_capacity - sum(combi)  < battery.current_capacity - sum(lowest_combination) and battery.current_capacity - sum(combi) < 7 :
                 houses = []
                 for output in combi:
                     for house in grid.unconnected_houses:
                         if house.max_output == output:
                             houses.append(house)
                 total_dist = 0
                 for h in houses:
                     total_dist += distance(h.location, battery.location)
                 if total_dist < best_dist:
                     best_dist = total_dist
                     lowest_combination= combi
                     out_houses = houses
    houses = []
    if sum(lowest_combination) < battery.current_capacity and sum(lowest_combination) - battery.current_capacity < 7:
        for output in lowest_combination:
            for house in grid.unconnected_houses:
                if house.max_output == output:
                    houses.append(house)

    return houses


def greedy_lookahead(grid):
    # initiate counter that will determine when to break
    counter = 0
    # repeat till solution is found
    while grid.unconnected_houses != []:
        # best_dist is the best score on distance
        best_dist = float('inf')
        # loop over houses that are not connected
        for house in grid.unconnected_houses:
            #  finds the lowest distance to battery for each house
            lowest_dist_house = float('inf')
            for battery in grid.batteries:
                dist = distance(house.location, battery.location)
                if dist < lowest_dist_house and battery.current_capacity > house.max_output:
                    # and battery.current_capacity > 280
                    bat_id = battery.id
                    house_id = house.id
                    lowest_dist_house = dist
                # elif 30 < battery.current_capacity < 280:
                #     if 0 < grid.range_connected(battery)[1] < 9:
                #         houses = look(grid, battery)
                #         for h in houses:
                #             grid.connect(h.id, battery.id)

            if lowest_dist_house < best_dist:
                connect_bat_id = bat_id
                connect_house_id = house_id
                best_dist = lowest_dist_house
        # print(best_dist)
        grid.connect(connect_house_id, connect_bat_id)
        counter += 1
#        print(counter)
        if counter > 101:
            break
    grid = greedy(grid)

    return grid
