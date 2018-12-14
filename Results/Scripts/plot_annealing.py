import json
from tkinter.filedialog import askopenfilename
import statistics
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def normaltest(data):
    k2, p = stats.mstats.normaltest(data)
    alpha = 1e-3
    print("p = {:g}".format(p))
    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("The null hypothesis can be rejected")
    else:
        print("The null hypothesis cannot be rejected")
    return p
# set input_csv to random string name to initiate while loop
input =  "input_file"

# open input dialog untill user selects a .csv file
while not input[-5:] == '.json':

    print(input)
    # print instruction
    print("Please open a .json file")

    # input user interface
    input = askopenfilename()




with open(input) as f:
    data = json.load(f)
    f.close()

wijk = input.find('wijk')
wijk_naam = input[wijk:wijk+5]
wijk_index = int(wijk_naam[-1]) - 1
print(wijk_index)
print(wijk_naam)
greedy = [60586, 49138, 50371]
lowerbound = [53188, 45268, 42757]
greedy_hill = [56536, 45799, 44125]
greedy_double_hill = [56536, 45781, 44125]
best_first = [56986, 45835, 44107]


random = data["All random results"]
hillclimber = data["Hillclimber results"]
annealing = data["All simulated annealing results"]

random.sort()

# bins = len(random)-2
bins =  int((max(random[:-2]) * 1.05) - lowerbound[wijk_index] *0.95)

print(bins)
plot1 = plt.hist(hillclimber, bins=bins, stacked=True, label="Hillclimber")
plot2 = plt.hist(random, bins=bins, stacked=True, label="Random")
plot3 = plt.hist(annealing, bins=bins, stacked=True, label="Annealing")

# delete highest two nonsence values
# random.sort()
random.pop()
random.pop()
hillclimber.sort()
hillclimber.pop()
hillclimber.pop()
annealing.sort()
annealing.pop()
annealing.pop()


p_random = normaltest(random)
p_hillclimber = normaltest(hillclimber)
p_annealing = normaltest(annealing)

# plt.ylim(0, 800)
plt.xlim(lowerbound[wijk_index] * 0.95, max(random) * 1.05)
plt.xlabel("Costs", fontsize=18)
plt.ylabel("Iterations", fontsize=18)
plt.title(f"{wijk_naam} distribution of costs random (p={round(p_random, 3)}) hillclimber (p={round(p_hillclimber, 2)}) and simulated annealing (p={round(p_annealing, 2)}), repeats: {len(random)}\n Hillclimbers and simulated annealing performed on displayed random data", fontsize =13)

plot4 = plt.axvline(greedy[wijk_index], color="gold", label="Greedy", linewidth=1.5)
plot5 = plt.axvline(greedy_hill[wijk_index], color="red", label="Greedy/Hillclimber", linewidth=1.5)
plot6 = plt.axvline(greedy_double_hill[wijk_index], color="green", label="Greedy/Double Hillclimber", linewidth=1.5)
plot7 = plt.axvline(lowerbound[wijk_index], color="black", label="Lower bound", linewidth=1.5)
plot8 = plt.axvline(best_first[wijk_index], color="purple", label="Best first", linewidth=1.5, alpha=0.7)

plt.legend()
plt.show()
