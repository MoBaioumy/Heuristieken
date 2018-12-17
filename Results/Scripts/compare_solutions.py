import json
from tkinter.filedialog import askopenfilename
import os
import numpy as np

inputfolder = "Heuristieken/Results/RandomHillclimber/"

wijk1 = []
wijk2 = []
wijk3 = []
for filename in os.listdir(inputfolder):
    with open(inputfolder + filename) as f:
        data = json.load(f)
        f.close()
        wijk_index = filename.find('wijk')
        wijk_naam = filename[wijk_index:wijk_index+5]
        wijk_nummer = int(wijk_naam[-1])


        results = list()
        for i in range(1, 6):
            current = data[str(i)]
            current.sort()
            results.append(set(current))
        if wijk_nummer == 1:
            wijk1.append({data["Costs best solution"] : results})
        elif wijk_nummer == 2:
            wijk2.append({data["Costs best solution"] : results})
        elif wijk_nummer == 3:
            wijk3.append({data["Costs best solution"] : results})

all = [wijk1, wijk2, wijk3]


diffs = {"Wijk1" : [],
         "Wijk2" : [],
         "Wijk3" : []}
for idx, wijk in enumerate(all):
    wijk_naam = "Wijk" + str(idx+1)
    print("")
    print(wijk_naam)
    print("")
    for i in range(len(wijk) - 1):
        x = wijk[i]
        y = wijk[i+1]
        total_diff = 0
        for key_x in x:
            for key_y in y:
                for i in range(len(x[key_x])):
                    diff = list(x[key_x][i] - y[key_y][i]) + list(y[key_y][i] - x[key_x][i])
                    diff.sort()
                    print(diff)
                    total_diff += len(diff)

        diffs[wijk_naam].append(total_diff)


for key in diffs:
    print(key, end=' ')
    print(np.mean(diffs[key]))
