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
import random # needed
import copy # needed
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


    def lower_bound(self):
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

        # calculate lower bound costs
        lower_bound = 0
        for battery in self.batteries:
            lower_bound += battery.cost
        lower_bound += sum(all_shortest) * 9

        return lower_bound


    def upper_bound(self):
        """
        Finds the manhattan distance for the longest path for each house
        Returns a list with all longest distances
        """
        all_longest = []
        # loop over houses for each house loop over batteries
        # find the longest distance to a battery and append to output list
        for house in self.houses:
            current_house_longest = float('-inf')
            for battery in self.batteries:
                dist = distance(house.location, battery.location)
                if dist > current_house_longest:
                    current_house_longest = dist
            all_longest.append(current_house_longest)

        # calculate lower bound costs
        upper_bound = 0
        for battery in self.batteries:
            upper_bound += battery.cost
        upper_bound += sum(all_longest) * 9

        return upper_bound


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


    def best_battery_number(self):
        """
        Loads file with best battery locations for this grid determined by k_means
        """
        self.batteries = self.load_batteries(f"Huizen_Batterijen/{self.name}_batterijen_opt_number.csv")


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

                        # Find battery ids
                        bat1Index = None
                        bat2Index =  None
                        for idx, battery in enumerate(self.batteries):
                            if battery.id == h1.battery_id:
                                bat1Index = idx
                            if battery.id == h2.battery_id:
                                bat2Index = idx

                        # if swap is possible, swap
                        if h1.house.max_output < max2 and h2.house.max_output < max1 and h1.battery_id != h2.battery_id:

                            # calculate is the swap improves the length of the connections
                            h1len = distance(h1.house.location, self.batteries[bat2Index].location)
                            h2len = distance(h2.house.location, self.batteries[bat1Index].location)
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
