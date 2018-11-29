# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 16:06:15 2018

@author: moham
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
import random
import csv

x_huizen = []
y_huizen = []
with open('wijk1_huizen.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            x_huizen.append(int(row[0]))
            y_huizen.append(int(row[1]))
        except:
            hello = 4

df = pd.DataFrame({
    'x': x_huizen[0: 50],
    'y': y_huizen[0: 50]
})


np.random.seed(200)
k = 5

plt_size = 7
# centroids[i] = [x, y]
centroids = {
    i+1: [random.randint(0, 50), random.randint(0, 50)]
    for i in range(k)
}
    
fig = plt.figure(figsize=(plt_size, plt_size))
plt.scatter(df['x'], df['y'], color='k')
colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'c'}
#for i in centroids.keys():
#    plt.scatter(*centroids[i], color=colmap[i], marker = 'D', s = 200)
plt.xlim(-5, 55)
plt.ylim(-5, 55)
plt.show()

fig = plt.figure(figsize=(plt_size, plt_size))
plt.scatter(df['x'], df['y'], color='k')
colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'c'}
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i], marker = 'D', s = 200)
plt.xlim(-5, 55)
plt.ylim(-5, 55)
plt.show()

def assignment(df, centroids):
    for i in centroids.keys():
        # sqrt((x1 - x2)^2 - (y1 - y2)^2)
        df['distance_from_{}'.format(i)] = (
            np.sqrt(
                (df['x'] - centroids[i][0]) ** 2
                + (df['y'] - centroids[i][1]) ** 2
            )
        )
    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
    df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
    df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
    df['color'] = df['closest'].map(lambda x: colmap[x])
    return df

df = assignment(df, centroids)
# print(df.head())

fig = plt.figure(figsize=(plt_size, plt_size))
plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i], marker = 'D', s = 200)
plt.xlim(-5, 55)
plt.ylim(-5, 55)
plt.show()

old_centroids = copy.deepcopy(centroids)

def update(k):
    for i in centroids.keys():
        centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
        centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
    return k

centroids = update(centroids)
    
fig = plt.figure(figsize=(plt_size, plt_size))
ax = plt.axes()
plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i], marker = 'D', s = 200)
plt.xlim(-5, 55)
plt.ylim(-5, 55)
for i in old_centroids.keys():
    old_x = old_centroids[i][0]
    old_y = old_centroids[i][1]
    dx = (centroids[i][0] - old_centroids[i][0]) * 0.75
    dy = (centroids[i][1] - old_centroids[i][1]) * 0.75
    ax.arrow(old_x, old_y, dx, dy, head_width=2, head_length=3, fc=colmap[i], ec=colmap[i])
plt.show()

df = assignment(df, centroids)

# Plot results
fig = plt.figure(figsize=(plt_size, plt_size))
plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i], marker = 'D', s = 200)
plt.xlim(-5, 55)
plt.ylim(-5, 55)
plt.show()

while True:
    closest_centroids = df['closest'].copy(deep=True)
    centroids = update(centroids)
    df = assignment(df, centroids)
    if closest_centroids.equals(df['closest']):
        break

fig = plt.figure(figsize=(plt_size, plt_size))
plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.3, edgecolor='k')
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i], marker = 'D', s = 200)
plt.xlim(-5, 55)
plt.ylim(-5, 55)
plt.show()
