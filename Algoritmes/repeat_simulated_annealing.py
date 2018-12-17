# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
import Algoritmes
import copy


from datetime import datetime
import json


def repeat_simulated_annealing(grid, N = 1, save = 'no', compare = 'yes', sa_iterations = 50000, hill_iterations = 10000, hill = 'True', begin = 'random', cooling = 'lin', Tbegin = 100, Tend = 0.01):

    """
    Repeats simulated annealing for a x number of times with different options.
    """

    costs = []
    costs_random = [999999]
    costs_sa = [999999]
    costs_hill = [999999]
    costs_hill2 = [999999]
    combination = {}

    for i in range(N):

        # let the use pick from which point to start
        if begin == 'random':

            # get random solution save time and costs
            grid = Algoritmes.random_connect(grid)

            # save results
            if compare == 'yes':
                cost = grid.calculate_total_cost()
                costs_random.append(cost)

        # greedy begin
        if begin == 'greedy':
            grid = Algoritmes.greedy(grid)

        if hill == 'True':

            grid = Algoritmes.hillclimber_random(grid, iterations = hill_iterations)

            # continue with hillclimbing for the normal hillclimber in order
            # to be able to compare the two algorithms
            if compare == 'yes':

                # deepcopy grid to make an actual copy not a pointer
                grid2 = copy.deepcopy(grid)
                # run the hillclimber with the same amount of iterations as sa
                grid2 = Algoritmes.hillclimber_random(grid2, sa_iterations)
                # save costs
                cost = grid2.calculate_total_cost()
                costs_hill.append(cost)

        # run simulated annealing and save time and costs
        grid = Algoritmes.simulated_annealing(grid, sa_iterations, Tbegin = Tbegin, Tend = Tend, cooling = cooling)
        cost = grid.calculate_total_cost()
        costs_sa.append(cost)

        if save == 'yes':

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

            # run hillclimber once more to check if the result was optimal
            # these results are saved but not counted as the best sa score
            grid = Algoritmes.hillclimber_greedy(grid)
            cost = grid.calculate_total_cost()
            costs_hill2.append(cost)

        # empty the grid
        grid.disconnect_all()

    # print results
    print('Best solution simulated annealing: ', min(costs_sa))
    print('Best solution hillclimber: ', min(costs_hill))

    if save == 'yes':

        # save all results in dict aswell
        combination["All simulated annealing results"] = costs_sa
        if compare == 'yes':
            combination["Hillclimber results"] = costs_hill
            combination["All random results"] = costs_random

        # get current datetime in string
        dt = datetime.now()
        stdt = '{:%B-%d-%Y_%H%M}'.format(dt)

        # dump data of best found solution to .json file
        with open(f'Results/simulatedannealing/{grid.name}_Best_solution_{combination["Costs best solution"]}_{stdt}_random_optimized_with_simulated_annealing_{i}_coolingscheme_{cooling}_steps_sa_{sa_iterations}stepshill_{hill_iterations}.json', 'w') as f:
            json.dump(combination, f,indent=4)
