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
            # create variab
            le with all lines
            houses_reader = csv.reader(csvfile)
            # houselist
            houses = list()
            # print
            for row in houses_reader:
                if row[0].isdigit():
                    houses.append(House(row[0], row[1], row[2]))

        return houses

    def load_batteries(self, filename):
        """
        Load houses from .txt
        """
        with open(filename, "r") as csvfile:
            # create variable with all lines
            battery_reader = csv.reader(csvfile)
            # battery list
            batteries = list()
            # print
            for row in battery_reader:
                if row[0].isdigit():
                    batteries.append(Battery(row[0], row[1], "Normal", row[2], 5000))
        return batteries

    def connect(self, house_id,  battery_id):
        """
        Connect a house to a battery and change information in system accordingly
        """
        # get house
        for house in self.houses
            if house.id == house_id
                H = house
            else
                eprint("House not found")
        # get battery
        for battery in self.load_batteries:
            if battery.id == battery_id
                B_location = battery.location
            else
                eprint("Battery not found")
        # create Route

    def calculate_cost(self):
        total_cost = 0
        for battery in self.batteries:
            total_bat_cost += battery.cost
            for route in battery.routes:
                 total_route_cost += route.cost
