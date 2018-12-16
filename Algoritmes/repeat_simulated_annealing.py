# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
import Algoritmes


from datetime import datetime
import json


def repeat_simulated_annealing(grid, N, iterations = 100000, hill = 'True', begin = 'random', bound = float('inf'), cooling = 'lin'):

    """
    Repeats simulated annealing for a x number of times with different options.
    """

    costs = []
    i = 0
    costs_random = [999999, 999998]
    costs_sa = [999999, 999998]
    costs_hill = [999999, 999998]
    costs_hill2 = [999999, 999998]
    combination = {}

    while i < N:

        print("Current iteration: ", i)

        if i % 100 == 0:
            print('Current best cost simulated annealing: ', min(costs_sa))
            print('Current best cost hillclimber: ', min(costs_hill))

        # let the use pick from which point to start
        if begin == 'random':

            # get random solution save time and costs
            grid = Algoritmes.random_connect(grid)
            cost_r = grid.calculate_total_cost()
            costs_random.append(cost_r)

        if begin == 'greedy':
            grid = Algoritmes.greedy(grid)
            grid = Algoritmes.hillclimber_random(grid, it=100000)

        if hill == 'True':
            grid = Algoritmes.hillclimber_random(grid, it=100000)
            cost = grid.calculate_total_cost()
            costs_hill.append(cost)

        # calculate cost for bound
        cost = grid.calculate_total_cost()

        # if the cost is acceptable, i.e. under the bound, run simulated_annealing
        if cost < bound:

            # run simulated annealing and save time and costs
            grid = Algoritmes.simulated_annealing(grid, iterations, cooling=cooling)
            cost = grid.calculate_total_cost()
            costs_sa.append(cost)

            i += 1

        # if cost of hillclimber is best solution save data for .json export
        if cost == min(costs_sa):
            current_combi = {}
            for battery in grid.batteries:
                house_ids = []
                for route in battery.routes:
                    house_id = route.house.id
                    house_ids.append(house_id)
                current_combi[f'{battery.id}'] = house_ids
            current_combi["Costs best solution"] = min(costs_sa)
            combination = current_combi

        grid = Algoritmes.hillclimber_greedy(grid)
        cost = grid.calculate_total_cost()
        costs_hill2.append(cost)

        # empty the grid
        grid.disconnect_all()

    # save all results in dict aswell
    combination["Hill after SA"] = min(costs_hill2)
    combination["All random results"] = costs_random
    combination["Hillclimber results"] = costs_hill
    combination["All simulated annealing results"] = costs_sa

    # get current datetime in string
    dt = datetime.now()
    stdt = '{:%B-%d-%Y_%H%M}'.format(dt)

    # dump data of best found solution to .json file
    with open(f'Results/simulatedannealing/{grid.name}_Best_solution_{combination["Costs best solution"]}_{stdt}_random_optimized_with_simulated_annealing_{i}_coolingscheme_{cooling}_steps_sa_{iterations}stepshill_{10000}.json', 'w') as f:
        json.dump(combination, f,indent=4)
