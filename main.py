import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route


if __name__ == "__main__":
    grid = Grid("wijk1")
    for house in grid.houses:
        print(house)
