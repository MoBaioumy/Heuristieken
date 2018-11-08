import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route


if __name__ == "__main__":
    grid = Grid("wijk1")
    # grid.connect(1, 1)
    test = []
    for i in range(150):
        test.append(House.closest_battery(grid, i))

    print(test)
