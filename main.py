import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route


if __name__ == "__main__":
    grid = Grid("wijk3")
    # for i in range(len(grid.houses)):
    #     grid.connect(i, 1)

    grid.find_best_option(grid.unconnected_houses, grid.batteries[0], 0, 0)

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

    # total_output = [house.max_output for house in grid.houses]
    # total_output = sum(total_output)
    # print(total_output)
    #
    # total_capacity =[battery.max_capacity for battery in grid.batteries]
    # total_capacity = sum(total_capacity)
    # print(total_capacity)
