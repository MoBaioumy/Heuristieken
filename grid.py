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
            print("House not found")
            return 1
        if len(H) > 1:
            print("Mutiple houses found, please reload grid")
            return 2
        # unlist
        H = H[0]

        # get battery
        B = [battery for battery in self.batteries if battery.id == battery_id]
        # error check
        if not B:
            print("Battery not found")
            return 1
        if len(B) > 1:
            print("Mutiple batteries found, please reload grid")
            return 2
        # unlist
        B = B[0]

        if B.current_capacity < H.max_output:
            print(f"Battery capacity ({round(B.current_capacity, 2)}) is not sufficient")
            return 3

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



    # def calculate_cost(self):
    #     total_cost = 0
    #     for battery in self.batteries:
    #         total_bat_cost += battery.cost
    #         for route in battery.routes:
    #              total_route_cost += route.cost
