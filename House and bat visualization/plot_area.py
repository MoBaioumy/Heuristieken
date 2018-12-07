# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 11:11:39 2018

@author: Mohamed
"""

import matplotlib.pyplot as plt
import csv
import random
import numpy as np
# import


x_huizen = []
y_huizen = []
cap = []
with open('wijk3_huizen.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            x_huizen.append(int(row[0]))
            y_huizen.append(int(row[1]))
            cap.append(float(row[2]))
            
        except:
            print("hi")
        # print(', '.join(row))

x = [38, 43, 42, 49, 3]
y = [12, 13, 3, 23, 45]

#x_huizen.sort()
#y_huizen.sort()

#plt.figure(1, figsize=(12, 10))
#plt.scatter(x, y, 300)
#plt.plot(x_huizen, y_huizen, '*r')
#
#plt.xticks(range(0, 55, 5))
#plt.yticks(range(0, 55, 5))
#plt.axis([-5, 60, -5, 60])
#plt.xlabel('X coordinates of area')
#plt.ylabel('Y coordinates of area')
#plt.title('Wijk 1')
#plt.legend(['Batteries', 'Houses'])
#plt.grid()


plt.plot(cap, 'o')
plt.xticks(range(0, 175, 25))
plt.yticks(range(0, 100, 20))
plt.title('Wijk 3')
plt.axis([-5, 160, -5, 100])

z = np.polyfit(list(range(150)), cap, 1)

p = np.poly1d(z)
#plt.plot(p)




def read_homes(file_name):
    # open up file
    return True


def read_batteries(file_name):
    # open up file
    with open(file_name, "r") as f:
        file_lines = f.readlines()
        print(file_lines)

        ###!!!! Start at 1 not 0
        for i in range(1, len(file_lines)):
            row = file_lines[i]
            row = row.rstrip()
            row = row.split()
            print(row)

            print(len(row))


            # coordinatez = row[-1]
            # print(coordinatez)

#read_batteries('wijk1_batterijen.txt')
# , delimiter=' ', quotechar='|'

def draw_route(house, bat):
    # if they share a coordinate, draw a staight line
    if (house[0] == bat[0]) or (house[1] == bat[1]):
        plt.plot([house[0], bat[0]], [house[1], bat[1]])
        
    else:
        mid_points = [ [house[0], bat[1]], [bat[0], house[1]]]
        mid_point = mid_points[random.randint(0 ,1)]
        #print(mid_point)
        # mid_point = [house[0], bat[1]]
        
        
# =============================================================================
#         Random colors and angles
# =============================================================================
        
#        colors = ['b', 'g', 'm', 'y', 'k', 'r', 'c' ]
#        color = colors[random.randint(0, len(colors) - 1)]
#        
#        plt.plot([house[0], mid_point[0]], [house[1], mid_point[1]], f'{color}')
#        plt.plot([bat[0], mid_point[0]], [bat[1], mid_point[1]], f'{color}')
        
        

# =============================================================================
#         # Every Bat has its own color
# =============================================================================
        
        colors = ['b', 'g', 'm', 'y', 'k']
        
        plt.plot([house[0], mid_point[0]], [house[1], mid_point[1]], f'{colors[i % 5]}')
        plt.plot([bat[0], mid_point[0]], [bat[1], mid_point[1]], f'{colors[i % 5]}')
        
    

#draw_route([10, 15], [15, 10])
#draw_route([40, 30], [30, 40])
#plt.plot(10, 15, '+')

#for i in range(len(x_huizen)):
#    draw_route([x_huizen[i], y_huizen[i]], [x[i % 5], y[i % 5]])


#draw_route([x_huizen[10], y_huizen[10]], [x[2 % 5], y[2 % 5]])