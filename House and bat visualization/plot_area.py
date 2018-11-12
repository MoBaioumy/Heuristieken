# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 11:11:39 2018

@author: Mohamed
"""

import matplotlib.pyplot as plt
import csv
# import 


x_huizen = []
y_huizen = []
with open('wijk1_huizen.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try: 
            x_huizen.append(int(row[0]))
            y_huizen.append(int(row[1]))
        except:
            print("hi")
        # print(', '.join(row))

x = [38, 43, 42, 49, 3]
y = [12, 13, 3, 23, 45]

#x_huizen.sort()
#y_huizen.sort()

plt.plot(x, y, '*b')
plt.plot(x_huizen, y_huizen, '*r')

plt.xticks(range(1, 50, 5))
plt.yticks(range(1, 50, 5))
plt.axis([-5, 60, -5, 60])
plt.xlabel('X coordinates of area')
plt.ylabel('Y coordinates of area')
plt.title('Wijk 1')
plt.legend(['Batteries', 'Houses'])
plt.grid()


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

read_batteries('wijk1_batterijen.txt')
# , delimiter=' ', quotechar='|'