import csv
from house import House
from battery import Battery
from route import Route
from distance import distance
from operator import attrgetter
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
import json
from datetime import datetime
import copy

class Grid(object):
    """
    Representation of a grid in the SmartGrid assignment
    """
    # initiate id to 1
    id = 1
    counter = 0

    def __init__(self, wijk_N):
        """
        Initialize a grid"""
        # id
        self.id = Grid.id
        Grid.id += 1
        self.name = wijk_N
        # load houses and batteries
        self.houses = self.load_houses(f"Huizen_Batterijen/{wijk_N}_huizen.csv")
        self.unconnected_houses = copy.deepcopy(self.houses)
        self.batteries = self.load_batteries(f"Huizen_Batterijen/{wijk_N}_batterijen.csv")
        # size of grid
        self.size = (50, 50)


    def __str__(self):
        """
        Print description
        """
        return f" GridID: {self.id} Grid size: {self.size}"


    def load_houses(self, filename):
        """
        Load houses from .csv
        """
        # Open file
        with open(filename, "r") as csvfile:
            # loop over rows of csv file, make house based on content and add house to house list of grid
            houses = [House(row[0], row[1], row[2]) for row in csv.reader(csvfile) if row[0].isdigit()]
        return houses


    def load_batteries(self, filename):
        """
        Load batteries from .csv
        """
        # open file
        with open(filename, "r") as csvfile:
            # loop over rows of csv file make battery based on data and add to battery list
            batteries = [Battery(row[0], row[1], "Normal", row[2], 5000) for row in csv.reader(csvfile) if row[0].isdigit()]
        return batteries


    def connect(self, house_id,  battery_id):
        """
        Connect a house to a battery and change information in system accordingly
        """
        # get house
        H = [house for house in self.unconnected_houses if house.id == house_id]
        # error check
        if not H:
            print("House not found, try disconnecting it first")
            return
        if len(H) > 1:
            print("Mutiple houses found, please reload grid")
            return
        # unlist
        H = H[0]

        # get battery
        B = [battery for battery in self.batteries if battery.id == battery_id]

        # error check
        if not B:
            print("Battery not found, please enter the id not the index number")
            return
        if len(B) > 1:
            print("Mutiple batteries found, please reload grid")
            return
        # unlist
        B = B[0]

        # if house max_output exceeds battery capacity return and print error message
        if B.current_capacity < H.max_output:
            print(f"Battery capacity ({round(B.current_capacity, 2)}) is not sufficient")
            return

        # remove house from unconnected list
        self.unconnected_houses.remove(H)

        # get battery index in battery list of grid
        B_index = self.batteries.index(B)

        # Make a route and append it to the route list in the corresponding battery
        route = Route(H, B.id, B.location)
        self.batteries[B_index].routes.append(route)

        # print connection made
        print(f"connected house {H.id} with battery {B.id}")

        # recalculate battery current capacity
        self.batteries[B_index].current_capacity -= H.max_output

        # print leftover capacity
        print(f"capcity left on battery: {round(self.batteries[B_index].current_capacity, 2)}")


    def disconnect(self, house_id):
        """
        Disconnects house based on id
        """
        # loop over routes in each battery untill we find the correct house
        for battery in self.batteries:
            for route in battery.routes:
                if route.house.id == house_id:
                    # find battery index
                    battery_idx = self.batteries.index(battery)
                    # update battery capacity
                    self.batteries[battery_idx].current_capacity += route.house.max_output
                    # place house back to unconnected_houses
                    self.unconnected_houses.append(route.house)
                    # remove route
                    self.batteries[battery_idx].routes.remove(route)
                    print(f"house {house_id} disconnected")
                    return
        # if house id not found print error message
        print("House not found, please check if house exists in grid.houses or excel file \nif it does exist please check grid.unconnected_houses \nif not present there, reload grid")
        return


    def disconnect_all(self):
        """
        Disconnects all houses from batteries
        """
        for battery in self.batteries:
            while battery.routes != []:
                self.disconnect(battery.routes[0].house.id)


    def calculate_total_cost(self):
        """
        Calculates the total cost of the current grid
        """
        total_cost_routes = sum([battery.calculate_routes_cost() for battery in self.batteries])
        total_cost_batteries = sum([battery.cost for battery in self.batteries])
        total_cost = total_cost_routes + total_cost_batteries
        return total_cost


    def shortest_paths(self):
        """
        Finds the manhattan distance for the shortest path for each house
        Returns a list with all shortest distances
        """
        all_shortest = []
        # loop over houses for each house loop over batteries
        # find the shortest distance to a battery and append to output list
        for house in self.houses:
            current_house_shortest = float('inf')
            for battery in self.batteries:
                dist = distance(house.location, battery.location)
                if dist < current_house_shortest:
                    current_house_shortest = dist
            all_shortest.append(current_house_shortest)

        return all_shortest


    def longest_paths(self):
        """
        Finds the manhattan distance for the longest path for each house
        Returns a list with all longest distances
        """
        all_longest = []
        # loop over houses for each house loop over batteries
        # find the longest distance to a battery and append to output list
        for house in self.houses:
            current_house_shortest = float('-inf')
            for battery in self.batteries:
                dist = distance(house.location, battery.location)
                if dist > current_house_shortest:
                    current_house_shortest = dist
            all_longest.append(current_house_shortest)

        return all_longest


    def draw_route(self, house, bat):
        """
        This test function draws funtion based on a non logic based
        greedy algorithm. So the batteries can go over limit
        """
        # if they share a coordinate, draw a staight line
        if (house[0] == bat[0]) or (house[1] == bat[1]):
            plt.plot([house[0], bat[0]], [house[1], bat[1]])

        else:
            mid_points = [ [house[0], bat[1]], [bat[0], house[1]]]
            mid_point = mid_points[random.randint(0 ,1)]
            #print(mid_point)
            # mid_point = [house[0], bat[1]]

            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
            color = colors[random.randint(0, len(colors) - 1)]

            plt.plot([house[0], mid_point[0]], [house[1], mid_point[1]], f'{color}')
            plt.plot([bat[0], mid_point[0]], [bat[1], mid_point[1]], f'{color}')


    def draw_grid(self):
        """
        Alternative way to draw routes using the grid_route property of the routes
        """

        # draw grid
        size = [x for x in range(51)]

        for x in range(51):
            y = [x for i in range(51)]
            plt.plot(size, y, 'k', linewidth=0.2)

        for y in range(51):
            x = [y for i in range(51)]
            plt.plot(x, size, 'k', linewidth=0.2)

        # set potential colors for batteries
        colors = ['b', 'g', 'r', 'm', 'c', 'y']

        # plot all houses and batteries, house has color of battery it is connected to
        # for each route in each battery plot the grid_routes in the same color as the battery
        for idx, battery in enumerate(self.batteries):
            color = colors[idx]
            # plot battery
            plt.plot(battery.location[0], battery.location[1], color + '8', markersize = 12)

            for route in battery.routes:
                x = [loc[0] for loc in route.grid_route]
                y = [loc[1] for loc in route.grid_route]

                # plot route
                plt.plot(x, y, color)

                # plot house
                plt.plot(route.house.location[0], route.house.location[1], color + '8', markersize = 5)

        for house in self.unconnected_houses:
            plt.plot(house.location[0], house.location[1], 'k8', markersize = 5)

        plt.show()



    def draw_all(self):
        """
        Draws all routes
        """
        for battery in self.batteries:
            plt.plot(battery.location[0], battery.location[1], 'ro', markersize=12)
            for house in self.houses:
                self.draw_route(house.location, battery.location)


    def range_connected(self, battery):
        """
        Returns absolute minimum and maximum of house that can be connected to input battery
        """
        # function that returns max output
        def max_output_func(house):
            return house.max_output
        # sort houses from smallest max output to largest
        self.unconnected_houses.sort(key=max_output_func)
        # get min amount of houses able to connect
        capacity_taken = 0
        max_connected_houses = 0
        for house in self.unconnected_houses:
            if capacity_taken + house.max_output < battery.max_capacity:
                capacity_taken += house.max_output
                max_connected_houses += 1
        # sort houses from largest to smallest max output
        self.unconnected_houses.sort(reverse=True, key=max_output_func)
        # get max amount of houses able to connect
        capacity_taken = 0
        min_connected_houses = 0
        for house in self.unconnected_houses:
            if capacity_taken + house.max_output < battery.max_capacity:
                capacity_taken += house.max_output
                min_connected_houses += 1

        range = (min_connected_houses, max_connected_houses)
        return range


    def move_batteries_random(self):
        """
        Moves all batteries to a random new location
        """
        # for each battery
        for battery in self.batteries:

            location_taken = True

            # keep generating random locations untill location is not taken by a house or battery (including current battery)
            while location_taken == True:
                location = (random.randint(0,51), random.randint(0,51))

                for house in self.houses:
                    if house.location == location:
                        location_taken = True
                        continue
                    else:
                        location_taken = False

                for bat in self.batteries:
                    if bat.location ==  location:
                        location_taken = True
                        continue
                    else:
                        location_taken = False

            # move battery
            battery.move(location)


    # From here algorithms only, above methods

    def simple(self):
        """
        Simply connects houses in reverse order over the batteries
        """
        for battery in self.batteries:
            for numb in range(150, 0, -1):
                self.connect(numb, battery.id)


    def random(self):
        """
        Randomly connects houses to batteries, solution not garanteed
        """
        # random.shuffle(self.batteries)
        for battery in self.batteries:


            min_out = min(house.max_output for house in self.unconnected_houses)


            while battery.current_capacity > min_out:

                idx = random.randint(0, len(self.unconnected_houses) - 1)
                house_id = self.unconnected_houses[idx].id

                self.connect(house_id, battery.id)

                if self.unconnected_houses == []:
                    break
                else:
                    min_out = min(house.max_output for house in self.unconnected_houses)


    def greedy_alt(self):
        """
        Alternative greedy algorithm that connect closest house then goes to next battery
        Currently not working
        """
        # writ alg that connects closest house then goes to next bat
        bat_full = 0
        while self.unconnected_houses != [] and bat_full < 5:
            for battery in self.batteries:
                closest_house = battery.find_closest_house(self.unconnected_houses)
                if closest_house != None:
                    self.connect(closest_house.id, battery.id)
                else:
                    bat_full +=1


    def greedy(self):
        """
        Connects next closest house to battery
        """
        # random.shuffle(self.batteries)

        # find min and max output value
        min_out = min(house.max_output for house in self.houses)
        max_out = max(house.max_output for house in self.houses)

        # algoritm does not work for third wijk because range of output is very low
        # the smallest house is left over when connecting via greedy,
        # therefore for this wijk we connect this house first to the first battery
        # this gives us the best option to make a good fit with this house included
        if self.name == 'wijk3':
            for house in self.houses:
                if house.max_output == min_out:
                    min_house_id = house.id
                    self.connect(min_house_id, 1)

        # for each battery loop over houses find current closest house and connect
        # when leftover capacity is under the max output a house can possibly have
        # but over 5 the algorithm tries to find a better fit
        for battery in self.batteries:
            for counter in range(len(self.unconnected_houses)):

                closest_house = battery.find_closest_house(self.unconnected_houses)

                # input check
                if closest_house == None:
                    print("No house to connect")
                    break

                house_id_connect = closest_house.id

                # leftover capcity after adding current house that will be connected
                leftover_cap = battery.current_capacity - closest_house.max_output

                if  max_out > leftover_cap > 5:
                    # find better option to connect if present
                    for house in self.unconnected_houses:
                        # difference of current loop house
                        difference_current = battery.current_capacity - house.max_output
                        # see if current house is a better fit
                        if difference_current < leftover_cap and difference_current > 0:
                            # set house_id and difference to new option
                            house_id_connect = house.id
                            leftover_cap = battery.current_capacity - house.max_output


                if leftover_cap > 5:
                    current_best = float('inf')
                    for house1 in self.unconnected_houses:
                        for house2 in self.unconnected_houses:
                            combi = house1.max_output + house2.max_output - battery.current_capacity
                            if 0 < combi < 5 and combi < current_best:
                                house_id_connect = house1.id
                                current_best = combi
                                print('x')




                # print(house_id_connect)
                self.connect(house_id_connect, battery.id)


    def find_best_option(self, houses, battery, sum_houses_capacity, sum_houses_distance):
        """

        """
        # alle combinaties/kinderen genereren voor een batterij
        #
        # als de kosten boven self.simple kosten oplossing komen dan afkappen
        # Dubbele combinaties?
        # volgorde maakt niet uit, dus het gaat om combinaties --> uitrekene min en max aantal huizen per batterij,
        # dus eerst sorteren en dan kijken hoeveel van de kleinste er in passen en hoeveel van de grootse er in passen
        # of kosten van een oplossing opslaan en zodra je er onder komt afkappen
        # als capaciteit is bereikt afpakken
        if sum_houses_capacity > battery.max_capacity:
            print("cap reached")
            return
        if sum_houses_distance > 500:
            print("longer route")
            return
        Grid.counter += 1

        new_houses = copy.deepcopy(houses)
        for house in new_houses:
            print(house)
            new_houses.remove(house)
            self.find_best_option(new_houses, battery, sum_houses_capacity, sum_houses_distance)

        # for house in houses:
        #     new_houses = copy.deepcopy(houses)
        #     print(house)
        #     for i in new_houses:
        #         print(i)
        #         if i.id == house.id:
        #             sum_houses_capacity += i.max_output
        #             dist =  distance(i.location, battery.location)
        #             sum_houses_distance += dist
        #         new_houses.remove(i)
        #     print(Grid.counter)
        #     self.find_best_option(new_houses, battery, sum_houses_capacity, sum_houses_distance)
        #     for i in new_houses:
        #         print(i)

    def hillclimber(self):
        # please comment

        counter = 1

        while counter == 1:
            counter = 0
            for batteries_one in self.batteries:
                for house_one in batteries_one.routes:
                    for batteries_two in self.batteries:
                        for house_two in batteries_two.routes:

                            total_one = house_one.house.max_output + batteries_one.current_capacity
                            total_two = house_two.house.max_output + batteries_two.current_capacity

                            if house_one.house.max_output < total_two and house_two.house.max_output < total_one:

                                    lengte_new = distance(house_one.house.location, self.batteries[house_two.battery_id - 1].location) + distance(house_two.house.location, self.batteries[house_one.battery_id - 1].location)

                                    lengte_old = house_one.length + house_two.length

                                    if counter < 1 and lengte_new < lengte_old and house_one.house.id != house_two.house.id:

                                        counter += 1
                                        # disconnect houses
                                        self.disconnect(house_one.house.id)
                                        self.disconnect(house_two.house.id)

                                        # switch connections
                                        self.connect(house_one.house.id, house_two.battery_id)
                                        self.connect(house_two.house.id, house_one.battery_id)
                                        break

    def simulated_annealing(self):
        """
        Simulated annealing
        """

    def random_hillclimber(self, cost_bound, repeats):
        """
        Random hillclimber take a certain cost bound and an amount of repeats as input
        The algorithm first finds a random solution for connecting all houses
        Then it runs a hillclimber to find the local mamximum
        It will repeat untill a solution is found under the cost bound
        Or untill amount of repeats is reached
        House combinations for best solution will be saved in .json
        Cost results for random and hillclimbers are saved aswell
        """

        # initiate
        counter = 0
        costs = [999999, 999998]
        costs_optimal = [999999, 999998]
        current_lowest_cost =  float('inf')
        combination = {}

        # loop untill repeats is reached or untill combination under lower bound is found
        while min(costs_optimal) > cost_bound and counter < repeats:

            # get random solution
            self.random()

            # if solution did not connect all houses get new solution untill all house are connected
            while self.unconnected_houses != []:
                self.disconnect_all()
                self.random()

            # costs
            cost = self.calculate_total_cost()
            costs.append(cost)

            # run hillclimber
            self.hillclimber()
            cost = self.calculate_total_cost()

            # if cost of hillclimber is best solution save data for .json export
            if cost < current_lowest_cost:
                current_lowest_cost = cost
                current_combi = {}
                for battery in self.batteries:
                    house_ids = []
                    for route in battery.routes:
                        house_id = route.house.id
                        house_ids.append(house_id)
                    current_combi[f'{battery.id}'] = house_ids
                current_combi["Costs best solution"] = cost
                combination = current_combi

            # save hillclimber cost
            costs_optimal.append(cost)

            # disconnect for new iteration
            self.disconnect_all()
            counter += 1

        # save all results in dict aswell
        combination["All random results"] = costs
        combination["All hillclimber results"] = costs_optimal

        # get current datetime in string
        dt = datetime.now()
        stdt = '{:%B-%d-%Y_%H%M}'.format(dt)

        # dump data of best found solution to .json file
        with open(f'Results/RandomHillclimber/{self.name}_Best_solution_{combination["Costs best solution"]}_{stdt}_random_optimized_with_hillclimber_{counter}_repeats_bound_{cost_bound}.json', 'w') as f:
            json.dump(combination, f,indent=4)

    def random_move_greedy_hillclimber(self, repeats):
        """
        Repeats the following:
        Randomly moves the batteries then runs a greedy algortim and hillclimber
        Saves results
        """
        # .json output dict
        info = {}
        best = float('inf')

        # for input repeats move batteries to random location run greedy and hillclimbers
        # calculate cost and save battery location and costs results to output dict
        for idx in range(repeats):
            self.move_batteries_random()
            self.greedy()
            self.hillclimber()
            cost = self.calculate_total_cost()
            if cost < best:
                best = cost
            locations = [battery.location for battery in self.batteries]
            info[idx] = {'Cost':cost, 'Location':locations}
            self.disconnect_all()

        # get current datetime in string
        dt = datetime.now()
        stdt = '{:%B-%d-%Y_%H%M}'.format(dt)

        # dump results to .json file
        with open(f'Results/RandomMove/{self.name}_Best_solution_{best}_{stdt}_random_move_greedy_optimized_with_hillclimber_{idx+1}_repeats.json', 'w') as f:
            json.dump(info, f,indent=4)
