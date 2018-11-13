import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route


if __name__ == "__main__":
    grid = Grid("wijk3")
    # for i in range(len(grid.houses)):
    #     grid.connect(i, 1)
    # #
    # grid.batteries[0].move(3, 5)
    grid.greedy()


    for i in grid.unconnected_houses:
        print(i)


    for i in grid.batteries:
        print(i.current_capacity)
    # closest_house = grid.batteries[0].find_closest_house([])
    # print(closest_house)
    # total_output = [house.max_output for house in grid.houses]
    # total_output = sum(total_output)
    # print(total_output)
    #
    # total_capacity =[battery.max_capacity for battery in grid.batteries]
    # total_capacity = sum(total_capacity)
    # print(total_capacity)
    # #
    # for house in grid.houses:
    #     print(house)
    # for battery in grid.batteries:
    #     print(battery)