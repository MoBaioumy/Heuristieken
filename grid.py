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
import itertools
import time
import pandas as pd



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
            # print(f"Battery capacity ({round(B.current_capacity, 2)}) is not sufficient")
            return

        # remove house from unconnected list
        self.unconnected_houses.remove(H)

        # get battery index in battery list of grid
        B_index = self.batteries.index(B)

        # Make a route and append it to the route list in the corresponding battery
        route = Route(H, B.id, B.location)
        self.batteries[B_index].routes.append(route)

        # print connection made
        # print(f"connected house {H.id} with battery {B.id}")

        # recalculate battery current capacity
        self.batteries[B_index].current_capacity -= H.max_output

        # print leftover capacity
        # print(f"capcity left on battery: {round(self.batteries[B_index].current_capacity, 2)}")


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
                    # print(f"house {house_id} disconnected")
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


    def swap(self, h1, h2):

        # disconnect houses
        self.disconnect(h1.house.id)
        self.disconnect(h2.house.id,)
        # swap connections
        self.connect(h1.house.id, h2.battery_id)
        self.connect(h2.house.id, h1.battery_id)
        swap = True

        return swap


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


    def draw_grid(self, info):
        """
        Draw routes using the grid_route property of the routes
        """
        plt.figure()

        # draw grid
        size = [x for x in range(51)]
        for x in range(51):
            current = [x for i in range(51)]
            plt.plot(size, current, 'k', linewidth=0.2)
            plt.plot(current, size, 'k', linewidth=0.2)

        # set potential colors for batteries
        colors = ['b', 'g', 'r', 'm', 'c', 'y']

        # plot all houses and batteries, house has color of battery it is connected to
        # for each route in each battery plot the grid_routes in the same color as the battery
        for idx, battery in enumerate(self.batteries):
            color = colors[idx]
            # plot battery
            plt.plot(battery.location[0], battery.location[1], color + '8', markersize = 12)

            for route in battery.routes:

                # get x and y
                x = [loc[0] for loc in route.grid_route]
                y = [loc[1] for loc in route.grid_route]

                # plot route
                plt.plot(x, y, color)

                # plot house
                plt.plot(route.house.location[0], route.house.location[1], color + '8', markersize = 5)

        # plot all unconnected houses in black
        for house in self.unconnected_houses:
            plt.plot(house.location[0], house.location[1], 'k8', markersize = 5)

        # costs and wijk name in title
        cost = self.calculate_total_cost()
        plt.title(f"{self.name} costs: {cost} {info}")

        plt.show()


    def k_means2(self, x_houses, y_houses, k):
        """
        As input (3 inputs) you need an array with the x coordiantes of all the houses
        and another with y coordinates and the third input the number of
        clusters you want (so number of batteries).
        """
        df = pd.DataFrame({'x': x_houses,'y': x_houses})


        np.random.seed(200)
        k = k
        # centroids[i] = [x, y]
        centroids = {
            i+1: [random.randint(0, 50), random.randint(0, 50)]
            for i in range(k)
        }

#        fig = plt.figure(figsize=(5, 5))
#        plt.scatter(df['x'], df['y'], color='k')
#        colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'c'}
#        for i in centroids.keys():
#            plt.scatter(*centroids[i], color=colmap[i])
#        plt.xlim(-5, 55)
#        plt.ylim(-5, 55)
#        plt.show()

        def assignment(df, centroids):
            for i in centroids.keys():
                # sqrt((x1 - x2)^2 - (y1 - y2)^2)
                df['distance_from_{}'.format(i)] = (
                    np.sqrt(
                        (df['x'] - centroids[i][0]) ** 2
                        + (df['y'] - centroids[i][1]) ** 2
                    )
                )
            centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
            df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
            df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
            df['color'] = df['closest'].map(lambda x: colmap[x])
            return df

        df = assignment(df, centroids)
        # print(df.head())

#        fig = plt.figure(figsize=(5, 5))
#        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
#        for i in centroids.keys():
#            plt.scatter(*centroids[i], color=colmap[i])
#        plt.xlim(-5, 55)
#        plt.ylim(-5, 55)
#        plt.show()

        old_centroids = copy.deepcopy(centroids)

        def update(k):
            for i in centroids.keys():
                centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
                centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
            return k

        centroids = update(centroids)

#        fig = plt.figure(figsize=(5, 5))
#        ax = plt.axes()
#        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
#        for i in centroids.keys():
#            plt.scatter(*centroids[i], color=colmap[i])
#        plt.xlim(-5, 55)
#        plt.ylim(-5, 55)
        for i in old_centroids.keys():
            old_x = old_centroids[i][0]
            old_y = old_centroids[i][1]
            dx = (centroids[i][0] - old_centroids[i][0]) * 0.75
            dy = (centroids[i][1] - old_centroids[i][1]) * 0.75
#            ax.arrow(old_x, old_y, dx, dy, head_width=2, head_length=3, fc=colmap[i], ec=colmap[i])
#        plt.show()

        df = assignment(df, centroids)

        # Plot results
#        fig = plt.figure(figsize=(5, 5))
#        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
#        for i in centroids.keys():
#            plt.scatter(*centroids[i], color=colmap[i])
#        plt.xlim(-5, 55)
#        plt.ylim(-5, 55)
#        plt.show()

        while True:
            closest_centroids = df['closest'].copy(deep=True)
            centroids = update(centroids)
            df = assignment(df, centroids)
            if closest_centroids.equals(df['closest']):
                break

#        fig = plt.figure(figsize=(5, 5))
#        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
#        for i in centroids.keys():
#            plt.scatter(*centroids[i], color=colmap[i])
#        plt.xlim(-5, 55)
#        plt.ylim(-5, 55)
#        plt.show()

        new_locations = []
        for i in centroids:
            loc = (centroids[i][0], centroids[i][1])
            new_locations.append(loc)

        for i in range(len(self.batteries)):
            bat = self.batteries[i]
            bat.move(new_locations[i])
            print()


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
            if capacity_taken + house.max_output < battery.current_capacity:
                capacity_taken += house.max_output
                max_connected_houses += 1
        # sort houses from largest to smallest max output
        self.unconnected_houses.sort(reverse=True, key=max_output_func)
        # get max amount of houses able to connect
        capacity_taken = 0
        min_connected_houses = 0
        for house in self.unconnected_houses:
            if capacity_taken + house.max_output < battery.current_capacity:
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
        while self.unconnected_houses != []:
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
            if self.unconnected_houses != []:
                self.disconnect_all()


    def greedy_alt(self):
        """
        Alternative greedy algorithm that connects houses in order of output (high to low)
        Currently not working
        """
        # function that returns max output
        def max_output_func(house):
            return house.max_output
        # sort houses from smallest max output to largest
        self.unconnected_houses.sort(key=max_output_func, reverse=True)

        counter = 0
        while self.unconnected_houses != []:
            for house in self.unconnected_houses:
                smallest_dist = float('inf')
                closest_battery_id = None
                for battery in self.batteries:
                    dist = distance(house.location, battery.location)
                    if dist < smallest_dist and battery.current_capacity > house.max_output:
                        closest_battery_id =  battery.id
                        smallest_dist = dist
                self.connect(house.id, closest_battery_id)

                # exit after many repeats
                counter += 1
                if counter > 1000:
                    return


    def look(self, battery):
        r = self.range_connected(battery)
        print(r)
        lowest =  [0, 0]
        outputs = [house.max_output for house in self.unconnected_houses]
        best_dist = float('inf')
        out_houses = []
        for i in range(r[1]):
             x = itertools.combinations(outputs, i)
             print("progress!")
             for j in x:
                 # print(sum(j) - battery.current_capacity)
                 if 0 < battery.current_capacity - sum(j)  < battery.current_capacity - sum(lowest) and battery.current_capacity - sum(j) < 7 :
                     houses = []
                     for i in j:
                         for house in self.unconnected_houses:
                             if house.max_output == i:
                                 houses.append(house)
                     total_dist = 0
                     for h in houses:
                         total_dist += distance(h.location, battery.location)
                     if total_dist < best_dist:
                         best_dist = total_dist
                         lowest = j
                         out_houses = houses
                     # print(sum(j) - battery.current_capacity)
        houses = []
        if sum(lowest) < battery.current_capacity and sum(j) - battery.current_capacity < 7:
            for i in lowest:
                for house in self.unconnected_houses:
                    if house.max_output == i:
                        houses.append(house)

        return houses


    def greed(self):
        counter = 0
        while self.unconnected_houses != []:
            best_dist = float('inf')
            for house in self.unconnected_houses:
                lowest_dist_house = float('inf')
                for battery in self.batteries:
                    dist = distance(house.location, battery.location)
                    if dist < lowest_dist_house and battery.current_capacity > house.max_output and battery.current_capacity > 280:
                        bat_id = battery.id
                        house_id = house.id
                        lowest_dist_house = dist
                    elif 50 < battery.current_capacity < 280:
                        if self.range_connected(battery)[1] < 9:
                            houses = self.look(battery)
                            for h in houses:
                                self.connect(h.id, battery.id)

                if lowest_dist_house < best_dist:
                    connect_bat_id = bat_id
                    connect_house_id = house_id
                    best_dist =  lowest_dist_house
            self.connect(connect_house_id, connect_bat_id)
            counter += 1
            print(counter)
            if counter > 200:
                return
        if self.unconnected_houses != []:
            for house in self.unconnected_houses:
                print(house.max_output)
            for battery in self.batteries:
                print(battery.current_capacity)


    def greedy(self):
        """
        Connects next closest house to battery
        """
        # random.shuffle(self.batteries)

        # find min and max output value
        all_outputs = [house.max_output for house in self.houses]
        min_out = min(all_outputs)
        max_out = max(all_outputs)

        # calculate factor, this represent the average amount allowed leftover capacity
        leftover_when_all_connected = sum(battery.max_capacity for battery in self.batteries) - sum(all_outputs)
        factor = leftover_when_all_connected / len(self.batteries)

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
                    # print("No house to connect")
                    break

                house_id_connect = closest_house.id

                # leftover capcity after adding current house that will be connected
                leftover_cap = battery.current_capacity - closest_house.max_output

                if  max_out > leftover_cap > factor:
                    # find better option to connect if present
                    for house in self.unconnected_houses:
                        # difference of current loop house
                        difference_current = battery.current_capacity - house.max_output
                        # see if current house is a better fit
                        if difference_current < leftover_cap and difference_current > 0:
                            # set house_id and difference to new option
                            house_id_connect = house.id
                            leftover_cap = battery.current_capacity - house.max_output


                if leftover_cap > factor * 2:
                    current_best = float('inf')
                    for house1 in self.unconnected_houses:
                        for house2 in self.unconnected_houses:
                            combi = house1.max_output + house2.max_output - battery.current_capacity
                            if 0 < combi < factor and combi < current_best:
                                house_id_connect = house1.id
                                current_best = combi





                # print(house_id_connect)
                self.connect(house_id_connect, battery.id)


    def find_best_option(self, houses, battery, sum_houses_capacity, sum_houses_distance):
        """
        Werk niet

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
        """
        This hillclimber algoritm checks if a swap between two houses can be made,
        and if so, if the swap would shorten the length of the path, if this is
        the case, the swap is made.
        """

        # set swap to true to start the loop
        swap = True

        # loops until no swaps can be made
        while swap == True:
            # sets swap to false
            swap = False
            # loops through the batteries
            for b1 in self.batteries:
                # loops through the houses in the batteries
                for h1 in b1.routes:
                    # loops through the batteries
                    for b2 in self.batteries:
                        # loops through the houses in the batteries
                        for h2 in b2.routes:
                            h1cap = h1.house.max_output + b1.current_capacity
                            h2cap = h2.house.max_output + b2.current_capacity
                            # checks if a swap between two houses can be made
                            if h1.house.max_output < h2cap and h2.house.max_output < h1cap:
                                    # calculate is the swap improves the length of the connections
                                    h1len = distance(h1.house.location, self.batteries[h2.battery_id - 1].location)
                                    h2len = distance(h2.house.location, self.batteries[h1.battery_id - 1].location)
                                    lengte_new =  h1len + h2len
                                    lengte_old = h1.length + h2.length

                                    # makes the swap if the length is improved
                                    if swap == False and lengte_new < lengte_old and h1.house.id != h2.house.id:
                                        swap = self.swap(h1.house.id, h2.house.id, h1.battery_id, h2.battery_id)
                                        break


    def hillclimber_double(self):
        """
        This hillclimber algoritm checks if a swap between pairs of two houses can be made,
        and if so, if the swap would shorten the length of the path, if this is
        the case, the swap is made.
        """
        swap = True
        # loops until no swaps can be made
        while swap == True:
            # sets swap to false
            swap = False
            self.hillclimber()
            print(self.calculate_total_cost())
            # loops through the batteries
            for b1 in self.batteries:
                for h1 in b1.routes:
                    for h2 in b1.routes:
                        for b2 in self.batteries:
                            for h3 in b2.routes:
                                for h4 in b2.routes:

                                    # MAKE FUNCTION OF THIS
                                    h1h2 = h1.house.max_output + h2.house.max_output
                                    h3h4 = h3.house.max_output + h4.house.max_output

                                    cap1 = h1h2 + b1.current_capacity
                                    cap2 = h3h4 + b2.current_capacity

                                    if h1 != h2 and h3 != h4 and h1h2 < cap2 and h3h4 < cap1:

                                        len_old = h1.length + h2.length + h3.length + h4.length

                                        d1 = distance(h1.house.location, self.batteries[h3.battery_id - 1].location)
                                        d2 = distance(h2.house.location, self.batteries[h3.battery_id - 1].location)
                                        d3 = distance(h3.house.location, self.batteries[h1.battery_id - 1].location)
                                        d4 = distance(h4.house.location, self.batteries[h1.battery_id - 1].location)

                                        len_new = d1 + d2 + d3 + d4

                                        # makes the swap if the length is improved
                                        if swap == False and len_new < len_old:

                                            # disconnect houses
                                            self.disconnect(h1.house.id)
                                            self.disconnect(h2.house.id)
                                            self.disconnect(h3.house.id)
                                            self.disconnect(h4.house.id)

                                            # swap connections
                                            self.connect(h1.house.id, h3.battery_id)
                                            self.connect(h2.house.id, h3.battery_id)
                                            self.connect(h3.house.id, h1.battery_id)
                                            self.connect(h4.house.id, h1.battery_id)
                                            swap = True

                                            break


    def re_arrange(self):
        """
        Re-arrange for simulated_annealing
        """




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
        costs_random = [999999, 999998]
        times_random =  []
        costs_hillclimber = [999999, 999998]
        times_hillclimber = []
        current_lowest_cost =  float('inf')
        combination = {}

        # loop untill repeats is reached or untill combination under lower bound is found
        while min(costs_hillclimber) > cost_bound and counter < repeats:


            # get random solution save time and costs
            random_start = time.time()
            self.random()
            random_stop = time.time()

            times_random.append(random_stop - random_start)

            cost_r = self.calculate_total_cost()
            costs_random.append(cost_r)


            # run hillclimber save time and costs
            hill_start = time.time()
            self.hillclimber()
            hill_stop = time.time()

            times_hillclimber.append(hill_stop - hill_start)

            cost_h = self.calculate_total_cost()
            costs_hillclimber.append(cost_h)



            # if cost of hillclimber is best solution save data for .json export
            if cost_h < current_lowest_cost:
                current_lowest_cost = cost_h
                current_combi = {}
                for battery in self.batteries:
                    house_ids = []
                    for route in battery.routes:
                        house_id = route.house.id
                        house_ids.append(house_id)
                    current_combi[f'{battery.id}'] = house_ids
                current_combi["Costs best solution"] = cost_h
                combination = current_combi

            # disconnect for new iteration
            self.disconnect_all()
            counter += 1
            print(counter)

        # save all results in dict aswell
        combination["All random results"] = costs_random
        combination["All hillclimber results"] = costs_hillclimber
        combination["Random times"] = times_random
        combination["Hillclimber times "] = times_hillclimber

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


    def k_means(self, k):
        """
        Input the number of clusters you want (so number of batteries).
        """

        x_houses = [house.location[0] for house in self.houses]
        y_houses = [house.location[1] for house in self.houses]
        df = pd.DataFrame({'x': x_houses,'y': y_houses})

        ## Please comment
        np.random.seed(200)
        # centroids[i] = [x, y]
        centroids = {
            i+1: [random.randint(0, 50), random.randint(0, 50)]
            for i in range(k)
        }

        fig = plt.figure(figsize=(5, 5))
        plt.scatter(df['x'], df['y'], color='k')
        colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'c'}
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])
        plt.xlim(-5, 55)
        plt.ylim(-5, 55)
        plt.show()

        def assignment(df, centroids):
            for i in centroids.keys():
                # sqrt((x1 - x2)^2 - (y1 - y2)^2)
                df['distance_from_{}'.format(i)] = (
                    np.sqrt(
                        (df['x'] - centroids[i][0]) ** 2
                        + (df['y'] - centroids[i][1]) ** 2
                    )
                )
            centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
            df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
            df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
            df['color'] = df['closest'].map(lambda x: colmap[x])
            return df

        df = assignment(df, centroids)
        # print(df.head())

        fig = plt.figure(figsize=(5, 5))
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])
        plt.xlim(-5, 55)
        plt.ylim(-5, 55)
        plt.show()

        old_centroids = copy.deepcopy(centroids)

        def update(k):
            for i in centroids.keys():
                centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
                centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
            return k

        centroids = update(centroids)

        fig = plt.figure(figsize=(5, 5))
        ax = plt.axes()
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])
        plt.xlim(-5, 55)
        plt.ylim(-5, 55)
        for i in old_centroids.keys():
            old_x = old_centroids[i][0]
            old_y = old_centroids[i][1]
            dx = (centroids[i][0] - old_centroids[i][0]) * 0.75
            dy = (centroids[i][1] - old_centroids[i][1]) * 0.75
            ax.arrow(old_x, old_y, dx, dy, head_width=2, head_length=3, fc=colmap[i], ec=colmap[i])
        plt.show()

        df = assignment(df, centroids)

        # Plot results
        fig = plt.figure(figsize=(5, 5))
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])
        plt.xlim(-5, 55)
        plt.ylim(-5, 55)
        plt.show()

        while True:
            closest_centroids = df['closest'].copy(deep=True)
            centroids = update(centroids)
            df = assignment(df, centroids)
            if closest_centroids.equals(df['closest']):
                break

        fig = plt.figure(figsize=(5, 5))
        plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
        for i in centroids.keys():
            plt.scatter(*centroids[i], color=colmap[i])
        plt.xlim(-5, 55)
        plt.ylim(-5, 55)
        plt.show()

        new_locations = []
        for i in centroids:
            loc = (int(centroids[i][0]), int(centroids[i][1]))
            new_locations.append(loc)

        for i in range(len(self.batteries)):
            bat = self.batteries[i]
            bat.move(new_locations[i])
            print()


    def move_calc(self):
        # generate tuple's of all coordinates
        coordinates = list()
        for x in range (0, 51):
            for y in range (0, 51):
                coordinates.append((x, y))

        # create representation of grid in dict
        grid_locations = {}
        for loc in coordinates:
            grid_locations[loc] = set([0])

        # place house max output values on location
        for house in self.unconnected_houses:
            grid_locations[house.location] = set([house.max_output])

        counter = 0

        max = self.batteries[0].max_capacity

        finished_locations = list()

        for i in range(15):
            # make structure to hold new values
            new_grid_locations = {}
            for location in coordinates:
                new_grid_locations[location] = set([0])

            # loop over grid locations
            for loc in grid_locations:

                # initiate
                up, down, left, right = None, None, None, None

                # up
                # if up exists
                if loc[1] < 50:
                    # make up location
                    up = (loc[0], loc[1] + 1)
                    # if it is smaller than max cap battery
                    temp = grid_locations[loc]|grid_locations[up]

                # down
                if loc[1] > 0:
                    down = (loc[0], loc[1] - 1)
                    temp = temp|grid_locations[down]

                # left
                if loc[0] > 0:
                    left = (loc[0] - 1, loc[1])
                    temp = temp|grid_locations[left]

                # right
                if loc[0] < 50:
                    right = (loc[0] + 1, loc[1])
                    temp = temp|grid_locations[right]

                new_grid_locations[loc] = temp
            del grid_locations
            grid_locations = copy.deepcopy(new_grid_locations)

        for i in grid_locations:
            if  sum(grid_locations[i]) > max:
                print(i)
