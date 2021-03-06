To start the user interface run the following in your terminal:

```
$ python main.py
```


The following window pops up:
![GUI grids](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/GUI_wijken.PNG)

Select the option you want.
Now the window will automatically closed and another will open prompting you for the algorithm.

![GUI Algorithms](https://github.com/ThomasHoed/Heuristieken/blob/master/Documentation/Pictures/Gui_algorithms.PNG)

Try the following:
1. Select Random, the grid will be connected and drawn. Watch the costs and lower bound
2. Select K_means, watch how the batteries get moved and the **updated lower bound**
3. Select Greedy or Greedy Look ahead, watch how the new connections look, the new cost
4. Select Hill Climber, watch how the cost improves

In the file main_repeat and main_single all the algorithms can be run separately and parameters can be adjusted. For multiple runs at once for the algorithms main_repeat is necessary. The description of the parameters is located in the scripts.
