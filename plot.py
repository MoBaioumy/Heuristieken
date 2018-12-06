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

# greedy = input("Greedy: ")
# greedy_hill = input("Greedy hill: ")
# greedy_double_hill = input("Greedy double hill: ")
# lowerbound = input("Lower bound: ")
random = data["All random results"]
hillclimber = data["All hillclimber results"]
random_times= data["Random times"]
hillclimber_times = data["Hillclimber times "]


bins = len(random)-2
plot1 = plt.hist(hillclimber, bins=bins, stacked=True, label="Hillclimber")
plot2 = plt.hist(random, bins=bins, stacked=True, label="Random")

# delete highest two nonsence values
random.sort()
random.pop()
random.pop()
hillclimber.sort()
hillclimber.pop()
hillclimber.pop()



p_random = normaltest(random)
p_hillclimber = normaltest(hillclimber)

plt.ylim(0, 650)
plt.xlim(min(hillclimber) * 0.95, max(random) * 1.05)
plt.xlabel("Costs", fontsize=18)
plt.ylabel("Iterations", fontsize=18)
plt.title(f"Distribution of costs random (p={round(p_random, 3)}) and hillclimber (p={round(p_hillclimber)}), repeats: {len(random)}\n Hillclimbers performed on displayed random data", fontsize =13)

plot3 = plt.axvline(x=60586, color="gold", label="Greedy", linewidth=2)
plot4 = plt.axvline(x=56536, color="red", label="Greedy/Hillclimber", linewidth=2)
plot5 = plt.axvline(x=0, color="green", label="Greedy/Double Hillclimber", linewidth=2)
plot6 = plt.axvline(x=53188, color="black", label="Lower bound", linewidth=2)
plt.legend()
plt.show()
