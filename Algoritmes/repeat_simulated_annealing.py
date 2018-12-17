# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid
import Algoritmes
import copy


from datetime import datetime
import json


def repeat_simulated_annealing(grid, N = 1, save = 'yes', compare = 'yes', sa_iterations = 50000, hill_iterations = 10000, hill = 'yes', begin = 'random', cooling = 'lin', Tbegin = 100, Tend = 0.01):

    """
    Repeats simulated annealing for a N number of times with different options.

    Optional parameters:

    N = number of repeats, (int), default = 1.

    save = save the file, ('yes', 'no'), default is 'yes'.

    compare = compare simulated annealing with normal hillclimber, ('yes', 'no'), default is 'yes'.

    sa_iterations = number of iterations for simulated annealing, (int), default = 50000.

    hill_iterations = number of iterations for hillclimber before simulated annealing, (int), default = 50000.

    hill = hillclimber before simulated annealing, ('yes', 'no'), default is 'yes'.

    begin = initial starting condition of grid, ('random', 'greedy'), default is 'random'.

    cooling = 'lin', 'exp', 'sig', 'geman', default 'lin'. Cooling scheme,
    user can choose between a linear cooling scheme, exponential cooling
    scheme, sigmodial cooling scheme and the Geman and Geman cooling scheme.

    Tbegin = int, default 100, begin temperature of simulated annealing

    Tend = float, default 0.01, end temperature of simulated annealing

    """

    costs = []
    costs_random = [999999]
    costs_sa = [999999]
    costs_hill = [999999]
    costs_hill2 = [999999]
    combination = {}

    # ensure that Tend is higher than 0, otherwise exponential cooling scheme does not work.
    if Tend < 0:
        Tend = 0.01

    for i in range(N):

        print('Current iteration: ', i)
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
            grid = Algoritmes.greedy_lookahead(grid)

        if hill == 'yes':

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
