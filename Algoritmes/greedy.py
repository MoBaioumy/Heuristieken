# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
import random


def greedy(grid):
    """
    Loops over batteries and connects closest house to battery
    """
    # repeat untill all houses are connected meaning a solution is found
    while grid.unconnected_houses != []:
        # disconnect 3 random houses if solution is not found, prevents that no solution will be found, makes outcome worse
        if len(grid.unconnected_houses) < 3:
            for i in range(3):
                grid.disconnect(random.randint(0, 150))

        # shuffle battery order otherwise you always get the same solution with this algoritm, we want to explore all possible solutions
        random.shuffle(grid.batteries)

        # find min and max output value of all houses
        all_outputs = [house.max_output for house in grid.houses]
        min_out = min(all_outputs)
        max_out = max(all_outputs)

        # calculate factor, this represent the average amount allowed leftover capacity
        leftover_when_all_connected = sum(battery.max_capacity for battery in grid.batteries) - sum(all_outputs)
        factor = leftover_when_all_connected / len(grid.batteries)


        # for each battery loop over houses find current closest house and connect
        # when leftover capacity is under the max output a house can possibly have
        # but over 5 the algorithm tries to find a better fit
        for battery in grid.batteries:
            for counter in range(len(grid.unconnected_houses)):

                closest_house = battery.find_closest_house(grid.unconnected_houses)

                # input check
                if closest_house == None:
                    print("No house to connect")
                    break

                house_id_connect = closest_house.id

                # leftover capcity after adding current house that will be connected
                leftover_cap = battery.current_capacity - closest_house.max_output

                if  max_out > leftover_cap > factor:
                    # find better option to connect if present
                    for house in grid.unconnected_houses:
                        # difference of current loop house
                        difference_current = battery.current_capacity - house.max_output
                        # see if current house is a better fit
                        if difference_current < leftover_cap and difference_current > 0:
                            # set house_id and difference to new option
                            house_id_connect = house.id
                            leftover_cap = battery.current_capacity - house.max_output

                # check if a combination of two houses can fit the leftover capacity better
                if leftover_cap > factor * 2:
                    current_best = float('inf')
                    for house1 in grid.unconnected_houses:
                        for house2 in grid.unconnected_houses:
                            combi = house1.max_output + house2.max_output - battery.current_capacity
                            if 0 < combi < factor and combi < current_best:
                                house_id_connect = house1.id
                                current_best = combi

                # connect house that is best option according to heursitics
                grid.connect(house_id_connect, battery.id)

    return grid
