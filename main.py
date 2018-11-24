import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route
from distance import distance


if __name__ == "__main__":

    i = 3
    wijk_naam = "wijk" + str(i)
    grid = Grid(wijk_naam)
    # grid.simple()
    print(grid.range_connected(grid.batteries[0]))


    # wijk_naam = "wijk3"
    # cost_bound = 43890
    # repeats = 1500
    # grid.random_hillclimber(cost_bound, repeats)

    # grid.greedy_alt()







    # grid.greedy()
    # grid.simple()
    # x = grid.calculate_total_cost() + 25000
    # grid.greedy_optimized()
    # # print(x)
    # print(grid.calculate_total_cost() + 25000)
    print(len(grid.unconnected_houses))
    # grid = Grid("wijk2")
    # print(sum(grid.shortest_paths()))
    # print(sum(grid.longest_paths()))
    #
    # grid = Grid("wijk3")
    # print(sum(grid.shortest_paths()))
    # print(sum(grid.longest_paths()))

    # print(grid.range_connected())





    # grid.find_best_option(grid.unconnected_houses, grid.batteries[0], 0, 0)

    # grid.simple()
    # grid.greedy()
    # for i in range(5):
    #     x= grid.batteries[i].calculate_routes_cost()
    #     print(x/9)
    # x = grid.calculate_total_cost()
    # print(x)
    # #
    # for i in grid.unconnected_houses:
    #     print(i)
    # sum_output = sum([i.max_output for i in grid.unconnected_houses])
    #
    # for i in grid.batteries:
    #     print(i.current_capacity)
    # print(sum_output)
    # #
    # #
    # for i in grid.batteries[0].routes:
    #     print(i.house.max_output)
    # closest_house = grid.batteries[0].find_closest_house([])
    # print(closest_house)
    # grid = Grid("wijk1")
    # grid.greedy()
    # first = grid.calculate_total_cost()
    # grid.greedy_optimized()
    # second = grid.calculate_total_cost()
    # difference = first - second
    # print(difference)
    # print(grid.unconnected_houses)
    #
    # grid.draw_grid([10, 28], [9, 3])
