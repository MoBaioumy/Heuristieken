import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route


if __name__ == "__main__":
    grid = Grid("wijk1")
    # grid.connect(1, 1)
    test = Battery.closest_house(grid, 1)
    print(test)
