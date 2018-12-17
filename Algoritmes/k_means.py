# SmartGrid December 2018
# Philip Oosterholt
# Mohamed Baioumy
# Thomas Hoedeman

from Objects.grid import Grid

import pandas as pd
import numpy as np
import random
import copy


def k_means(grid):
    """
    Input the number of clusters you want (so number of batteries).
    """

    x_houses = [house.location[0] for house in grid.houses]
    y_houses = [house.location[1] for house in grid.houses]

    k = len(grid.batteries)

    df = pd.DataFrame({'x': x_houses,'y': y_houses})

    np.random.seed(200)

    centroids = {
        i+1: [random.randint(0, 50), random.randint(0, 50)]
        for i in range(k)
    }

    def assignment(df, centroids):
        for i in centroids.keys():
            df['distance_from_{}'.format(i)] = (
                np.sqrt(
                    (df['x'] - centroids[i][0]) ** 2
                    + (df['y'] - centroids[i][1]) ** 2
                )
            )
        centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
        df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
        df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
        return df

    df = assignment(df, centroids)


    old_centroids = copy.deepcopy(centroids)

    def update(k):
        for i in centroids.keys():
            centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
            centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
        return k

    centroids = update(centroids)

    for i in old_centroids.keys():
        old_x = old_centroids[i][0]
        old_y = old_centroids[i][1]
        dx = (centroids[i][0] - old_centroids[i][0]) * 0.75
        dy = (centroids[i][1] - old_centroids[i][1]) * 0.75


    df = assignment(df, centroids)

    while True:
        closest_centroids = df['closest'].copy(deep=True)
        centroids = update(centroids)
        df = assignment(df, centroids)
        if closest_centroids.equals(df['closest']):
            break

    new_locations = []
    for i in centroids:
        loc = (int(centroids[i][0]), int(centroids[i][1]))
        new_locations.append(loc)

    for idx, battery in enumerate(grid.batteries):
        battery.move(new_locations[idx])

    return grid
