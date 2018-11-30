from house import House
from battery import Battery
from grid import Grid
from operator import add
import numpy as np

if __name__ == "__main__":

    grid = Grid("wijk1")

    num_houses = 150
    num_batteries = 5

    for i in range(1,50):

        r1 = random.randint(1,150)

        for b in grid.batteries:
            for h in b.routes:
                if h.id == r1:
                    h1 = h
                    b1 = b
                    max1 = h1.house.max_output + b1.current_capacity
                    r2 = random.randint(1,150)
                    break


        for b in grid.batteries:
            for h in b.routes:
                if h.id == r2:
                    h2 = h
                    b2 = b
                    max2 = h2.house.max_output + b.current_capacity
                    if h1.house.max_output < max2 and h2.house.max_output < max1:
                        len_old = h1.length + h2.length
                        # calculate is the swap improves the length of the connections
                        h1len = distance(h1.house.location, grid.batteries[h2.battery_id - 1].location)
                        h2len = distance(h2.house.location, grid.batteries[h1.battery_id - 1].location)
                        len_new =  h1len + h2len
                        if len_old > len_new:
                            print('better')
                        else:
                            print('worse')
                        grid.swap(h1, h2)
