import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route
from distance import distance

if __name__ == "__main__":
<<<<<<< HEAD
    grid = Grid("wijk0")
    # for i in range(len(grid.houses)):
    #     grid.connect(i, 1)

    grid.find_best_option(grid.unconnected_houses[0:3], grid.batteries[0], 0, 0)

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
=======
>>>>>>> e5d45d3b0733161c61b6416ef3e2784f7269c933

    grid = Grid("wijk1")
    grid.greedy()
    first = grid.calculate_total_cost()
    grid.greedy_optimized()
    second = grid.calculate_total_cost()
    difference = first - second
    print(difference)
    print(grid.unconnected_houses)
    
    grid.draw_grid([10, 28], [9, 3])
