import csv
from house import House
from battery import Battery
from route import Route

class Grid(object):
    """
    Representation of a grid in the SmartGrid assignment
    """
    # initiate id to 1
    id = 1
    def __init__(self, wijk_N):
        """
        Initialize a grid"""
        # id
        self.id = Grid.id
        Grid.id += 1
        # load houses and batteries
        self.houses = self.load_houses(f"Huizen_Batterijen/{wijk_N}_huizen.csv")
        self.unconnected_houses = self.houses
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

    # def disconnect(self, house_id)
    #     for battery in self.batteries:
    #         for route in battery.routes
    #             if route.house.id == house_id:
    #                 self.unconnected_houses.append(route.house)



    def greedy(self):
        # find min and max
        min = 1000000
        max = 0
        for house in self.houses:
            if house.max_output > max:
                max = house.max_output
            if house.max_output < min:
                min = house.max_output
        # loop over batteries
        for battery in self.batteries:
            # repeat for amount of unconnected_houses
            for counter in range(len(self.unconnected_houses)):
                # find closest house
                house_id = battery.find_closest_house(self.unconnected_houses)

                # check if closest house is found
                if not house_id == None:
                    # find current house object
                    for house in self.unconnected_houses:
                        if house_id == house.id:
                            H = house
                    # get difference between current cap and house max_output
                    difference_best = battery.current_capacity - H.max_output
                    # find better option if difference is in range 5 to max_max_ouput
                    if difference_best > 5 and difference_best < max:
                        # loop over unconnected_houses
                        for house in self.unconnected_houses:
                            # difference of current loop house
                            difference_current = battery.current_capacity - house.max_output
                            # see if current house is a better fit
                            if difference_current < difference_best and difference_current > 0:
                                # set H object house_id and difference to new option
                                H = house
                                house_id = house.id
                                difference_best = battery.current_capacity - H.max_output

                    # find difference is still over 15 find if a combination of 2 house is better
                    if difference_best > 5:
                        for house1 in self.unconnected_houses:
                            for house2 in self.unconnected_houses:
                                if  house1.max_output + house2.max_output - battery.current_capacity < 5:

                                    house_id = house1.id


                    self.connect(house_id, battery.id)


        # for counter in range(len(self.unconnected_houses)):
        #     for battery in self.batteries:
        #         house_id = battery.find_closest_house(self.unconnected_houses)
        #         if not house_id == None:
        #             for house in self.unconnected_houses:
        #                 if house_id == house.id:
        #                     H = house
        #
        #             print(battery.current_capacity - H.max_output)
        #             if battery.current_capacity - H.max_output > 5 and battery.current_capacity - H.max_output < 76.16:
        #
        #                 for house in self.unconnected_houses:
        #                     if battery.current_capacity - house.max_output < battery.current_capacity - H.max_output:
        #                         house_id = H.id
        #
        #
        #             self.connect(house_id, battery.id)



    # def calculate_cost(self):
    #     total_cost = 0
    #     for battery in self.batteries:
    #         total_bat_cost += battery.cost
    #         for route in battery.routes:
    #              total_route_cost += route.cost
