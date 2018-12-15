# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

# Objects
from Objects.house import House
from Objects.battery import Battery
from Objects.route import Route
from Objects.distance import distance


# Libraries
import csv
from operator import attrgetter
import matplotlib.pyplot as plt
import numpy as np
import random
import copy
import json
from datetime import datetime
import copy
import time
import pandas as pd
import math



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
        # random.shuffle(self.batteries)
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
                    return True
        # if house id not found print error message
        print("House not found, please check if house exists in grid.houses or excel file \nif it does exist please check grid.unconnected_houses \nif not present there, reload grid")
        return False


    def disconnect_all(self):
        """
        Disconnects all houses from batteries
        """
        for battery in self.batteries:
            while battery.routes != []:
                self.disconnect(battery.routes[0].house.id)


    def swap(self, h1, h2, h3 = False, h4 = False):
        swap = False
        if h3 == False:
            # disconnect houses
            self.disconnect(h1.house.id)
            self.disconnect(h2.house.id)
            print(h1)
            print(h2)
            # reconnected houses swapped
            self.connect(h1.house.id, h2.battery_id)
            self.connect(h2.house.id, h1.battery_id)
            swap = True
        else:
            # disconnect houses
            self.disconnect(h1.house.id)
            self.disconnect(h2.house.id)
            self.disconnect(h3.house.id)
            self.disconnect(h4.house.id)
            # reconnected swap
            self.connect(h1.house.id, h3.battery_id)
            self.connect(h2.house.id, h3.battery_id)
            self.connect(h3.house.id, h1.battery_id)
            self.connect(h4.house.id, h1.battery_id)
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

    def re_arrange(self):
        """
        Re-arrange for simulated_annealing
        """

        found = False
        house1 = False

        while found == False:

            # get random house_ids
            r1 = random.randint(1,150)
            r2 = random.randint(1,150)

            # find house 1
            while house1 == False:
                for battery in self.batteries:
                    for route in battery.routes:
                        if route.house.id == r1:
                            h1 = route
                            b1 = battery
                            max1 = h1.house.max_output + b1.current_capacity
                            house1 = True
                            break

            # find house 2
            for battery in self.batteries:
                for route in battery.routes:
                    if route.house.id == r2:

                        h2 = route
                        b2 = battery
                        max2 = h2.house.max_output + b2.current_capacity

                        # if swap is possible, swap
                        if h1.house.max_output < max2 and h2.house.max_output < max1 and h1 != h2:

                            # calculate is the swap improves the length of the connections
                            h1len = distance(h1.house.location, self.batteries[h2.battery_id - 1].location)
                            h2len = distance(h2.house.location, self.batteries[h1.battery_id - 1].location)
                            lengte_new = h1len + h2len
                            lengte_old = h1.length + h2.length

                            # stop while loop
                            found = True
                            break

            # in case we cannot find a house to swap with house 1, we need to reset the loop
            # without this you might get stuck in a loop
            house1 = False

        # return all the necessary information
        self.proposed = (lengte_new - lengte_old) * 9
        self.h1 = h1
        self.h2 = h2

    # From here algorithms only, above methods





    def re_arrange_random(self, it = 10000):
        """
        Re-arrange for simulated_annealing
        """

        house1 = False
        i = 0
        swap = 0

        while i < it:

            found = False
            house1 = False

            while found == False:


                # get random house_ids
                r1 = random.randint(1,150)
                r2 = random.randint(1,150)


                # find house 1
                while house1 == False:
                    for battery in self.batteries:
                        for route in battery.routes:
                            if route.house.id == r1:
                                h1 = route
                                b1 = battery
                                max1 = h1.house.max_output + b1.current_capacity
                                house1 = True
                                break

                # find house 2
                for battery in self.batteries:
                    for route in battery.routes:
                        if route.house.id == r2:

                            h2 = route
                            b2 = battery
                            max2 = h2.house.max_output + b2.current_capacity

                            # if swap is possible, swap
                            if h1.house.max_output < max2 and h2.house.max_output < max1 and h1.house.id != h2.house.id:

                                i += 1

                                # calculate is the swap improves the length of the connections
                                h1len = distance(h1.house.location, self.batteries[h2.battery_id - 1].location)
                                h2len = distance(h2.house.location, self.batteries[h1.battery_id - 1].location)
                                lengte_new = h1len + h2len
                                lengte_old = h1.length + h2.length

                                if lengte_new < lengte_old and h1.battery_id != h2.battery_id:
                                    print(h1.battery_id )
                                    print(h2.battery_id )
                                    self.swap(h1, h2)
                                    swap = swap + 1

                                # stop while loop
                                found = True
                                break

                # in case we cannot find a house to swap with house 1, we need to reset the loop
                # without this you might get stuck in a loop
                house1 = False


    def simulated_annealing(self, N, hill = 'False', accept = 'std', cooling = 'std'):

        """
        Simulated annealing
        """

        # parameters
        Tbegin = 100
        Tend = 0.01
        T = Tbegin

        for i in range(N):

            # get a proposition for a swap
            prop = self.re_arrange()

            # calculate difference of options
            current = self.calculate_total_cost()
            proposed = current + self.proposed

            # calculate probability of acceptance
            if accept == 'std':

                probability = max(0, min(1, np.exp(-(proposed - current) / T)))
                print(probability)
            # if the proposed option is better than current, accept it
            if current > proposed:
                probability = 1

            # if option is worse, generate a random number between 0 and 1, if that
            # number is lower than the probability, make the swap
            if np.random.rand() < probability:
                self.swap(self.h1, self.h2)

            # geman parameters
            d = 2

            # cooling schemes
            # standard as a test
            if cooling == 'std':
                T = 0.999 * T
            # linear
            if cooling == 'lin':
                T = Tbegin - i * (Tbegin - Tend) / N
            # exponential
            if cooling == 'exp':
                 T = Tbegin * math.pow(Tend / Tbegin, i / N)
            # sigmodial
            if cooling == 'sig':
                T = Tend + (Tbegin - Tend) / (1 + np.exp(0.3 * (i - N / 2)))
            # geman and geman
            if cooling == 'geman':
                T = Tbegin / (np.log(i + d))

        # end simulated_annealing with a hillclimber, to make sure there are no
        # more ways to improve the grid
        if hill == 'True':
            self.hillclimber()


    def repeat_simulated_annealing(self, N, iterations = 1000, hill = 'True', begin = 'random', bound = float('inf'), cooling = 'lin'):

        """
        Repeats simulated annealing for a x number of times with different options.
        """

        costs = []
        i = 0
        costs_random = [999999, 999998]
        costs_sa = [999999, 999998]
        costs_hill = [999999, 999998]
        costs_hill2 = [999999, 999998]
        combination = {}

        while i < N:

            print("Current iteration: ", i)

            if i % 100 == 0:
                print('Current best cost simulated annealing: ', min(costs_sa))
                print('Current best cost hillclimber: ', min(costs_hill))

            # let the use pick from which point to start
            if begin == 'random':

                # get random solution save time and costs
                self.random()
                cost_r = self.calculate_total_cost()
                costs_random.append(cost_r)

            if begin == 'greedy':
                self.greedy()
                self.re_arrange_random(it=10000)

            if hill == 'True':
                self.re_arrange_random(it=10000)
                cost = self.calculate_total_cost()
                costs_hill.append(cost)

            # calculate cost for bound
            cost = self.calculate_total_cost()

            # if the cost is acceptable, i.e. under the bound, run simulated_annealing
            if cost < bound:

                # run simulated annealing and save time and costs
                self.simulated_annealing(iterations, cooling=cooling)
                cost = self.calculate_total_cost()
                costs_sa.append(cost)

                i += 1

            # if cost of hillclimber is best solution save data for .json export
            if cost == min(costs_sa):
                current_combi = {}
                for battery in self.batteries:
                    house_ids = []
                    for route in battery.routes:
                        house_id = route.house.id
                        house_ids.append(house_id)
                    current_combi[f'{battery.id}'] = house_ids
                current_combi["Costs best solution"] = min(costs_sa)
                combination = current_combi

            self.hillclimber()
            cost = self.calculate_total_cost()
            costs_hill2.append(cost)

            # empty the grid
            self.disconnect_all()

        # save all results in dict aswell
        combination["Hill after SA"] = min(costs_hill2)
        combination["All random results"] = costs_random
        combination["Hillclimber results"] = costs_hill
        combination["All simulated annealing results"] = costs_sa

        # get current datetime in string
        dt = datetime.now()
        stdt = '{:%B-%d-%Y_%H%M}'.format(dt)

        # dump data of best found solution to .json file
        with open(f'Results/simulatedannealing/{self.name}_Best_solution_{combination["Costs best solution"]}_{stdt}_random_optimized_with_simulated_annealing_{i}_coolingscheme_{cooling}_steps_sa_{iterations}stepshill_{10000}.json', 'w') as f:
            json.dump(combination, f,indent=4)


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


    def best_battery_number(self):

        self.batteries = self.load_batteries(f"Huizen_Batterijen/{self.name}_batterijen_opt_number.csv")


    def verplaat_batterij_met_k_means(self, k):
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

#        fig = plt.figure(figsize=(5, 5))
#        plt.scatter(df['x'], df['y'], color='k')
        colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'c', 6: 'y'}
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
        plt.show()

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
            loc = (int(centroids[i][0]), int(centroids[i][1]))
            new_locations.append(loc)

        for i in range(len(self.batteries)):
            bat = self.batteries[i]
            bat.move(new_locations[i])


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
