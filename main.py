import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route
from distance import distance

if __name__ == "__main__":

    grid = Grid("wijk1")
    grid.greedy()
    first = grid.calculate_total_cost()
    grid.greedy_optimized()
    second = grid.calculate_total_cost()
    difference = first - second
    print(difference)
    print(grid.unconnected_houses)
