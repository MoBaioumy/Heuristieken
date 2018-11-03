import csv
from house import House
from battery import Battery

class Grid(object):
    """
    Representation of a grid in the SmartGrid assignment
    """

    def __init__(self, wijk_N):
        """
        Initialize a grid"""
        # self.size = (length, width)
        self.id = wijk_N
        self.houses = self.load_houses(f"Huizen&Batterijen/{wijk_N}_huizen.csv")
        self.batteries = self.load_batteries(f"Huizen&Batterijen/{wijk_N}_batterijen.csv")

    def __str__(self):
        """
        Print description
        """
        return f" ID: {self.id} size: {self.size}"

    def load_houses(self, filename):
        """
        Load houses from .csv
        """
        # Open file
        with open(filename, "r") as csvfile:
            # create variable with all lines
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
            # houselist
            batteries = list()
            # print
            for row in battery_reader:
                if row[0].isdigit():
                    batteries.append(Battery(row[0], row[1], "Normal", row[2]))
        return batteries

if __name__ == "__main__":
    grid = Grid("wijk1")
