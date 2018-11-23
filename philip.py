from house import House
from battery import Battery
from grid import Grid
from operator import add
import numpy as np

if __name__ == "__main__":

    grid = Grid("wijk1")

    num_houses = 150
    num_batteries = 5

    # load load_batteries
    batteries = grid.batteries

    batteries = [i for i in grid.batteries]

    batteries = []
    for i in range(len(grid.batteries)):
         batteries.append(grid.batteries[i])

    # load houses
    houses = []
    for i in range(len(grid.houses)):
        houses.append(grid.houses[i])

    # calculate distance to every house per battery
    distances = []
    for i in range(num_houses):

        # obtain location of the house
        x_house = houses[i].location[0]
        y_house = houses[i].location[1]

        x_dif = []
        y_dif = []

        # calculate distances per x and y
        for i in range(num_batteries):
            x_dif.append(abs(x_house - batteries[i].location[0]))
            y_dif.append(abs(y_house - batteries[i].location[1]))

        # calculate overall distance
        man_distance = list(map(add, x_dif, y_dif))
        distances.append(man_distance)

    # set connected to false
    connections = [[], [], [], [], []]
    capacity_batteries = []
    for i in num_batteries:
        capacity_batteries.append(grid.batteries[i].capacity)
    # capacity_batteries =

    for i in range(150):

        min_house = distances.index(min(distances))
        min_bat = distances[min_house].index(min(distances[min_house]))

        distances[min_house] = [999]
        connections[min_bat].append(min_house)

    print(connections[1])


# man_distance = list(map(add, x_dif, y_dif))
# shortest = man_distance.index(min(man_distance))

    #     distances.append(distance)
    #
    # # if battery is full, select other battery
    # # find closest house
    # # update capacitiy
    # # next battery
    #
    #
    # batteries = []
    #
    # house = grid.houses[0].location
    #
    # size = len(grid.batteries)
    #
    # for i in range(size):
    #     batteries.append(grid.batteries[i].location)
    #
    # x_house = house[0]
    # y_house = house[1]
    #
    # x_battery = []
    # y_battery = []
    # #
    # for i in range(len(houses)):
    #     for i in range(size):
    #         x_battery.append(batteries[i][0])
    #         y_battery.append(batteries[i][1])
    #
    #     for i in range(size):
    #         x_dif.append(abs(x_house - x_battery[i]))
    #         y_dif.append(abs(y_house - y_battery[i]))

    #
    #
    # x_dif = []
    # y_dif = []
    #
    #
    #
    # man_distance = list(map(add, x_dif, y_dif))
    # shortest = man_distance.index(min(man_distance))
