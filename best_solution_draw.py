import json
from tkinter.filedialog import askopenfilename
from grid import Grid
from house import House
from battery import Battery
from route import Route
from distance import distance

input =  'filename'

while not input[-5:] == '.json':

    print(input)
    # print instruction
    print("Please open a .json file")

    # input user interface
    input = askopenfilename()


with open(input) as f:
    data = json.load(f)
    f.close()

wijk_index = input.find('wijk')
wijk_naam = input[wijk_index:wijk_index+5]

grid = Grid(wijk_naam)

for i in range(1, 6):
    current = data[str(i)]
    for house_id in current:
        grid.connect(house_id, i)
grid.draw_grid("Best solution")
