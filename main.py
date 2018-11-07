import csv
from grid import Grid
from house import House
from battery import Battery
from route import Route


if __name__ == "__main__":
    grid = Grid("wijk1")
    test_route = Route(grid.houses[0], grid.batteries[0])
    print(test_route)
    test_route.plan_grid_route()
    for coords in test_route.grid_route:
        print(coords)
    print(f"cost: {test_route.cost}")
