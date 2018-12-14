def simple(grid):
    """
    Simply connects houses in reverse order over the batteries
    """
    for battery in grid.batteries:
        for numb in range(150, 0, -1):
            grid.connect(numb, battery.id)

    return grid
