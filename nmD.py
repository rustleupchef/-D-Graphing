import sys
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

class StaticAxis:
    def __init__(self, name: int, range: tuple, ticks: int, isInput: bool, startingValue=None, label = None) -> None:
        self.name = name
        self.range = range
        self.ticks = ticks
        self.isInput = isInput
        self.startingValue = startingValue
        if startingValue is not None:
            if not (range[0] <= startingValue <= range[1]):
                raise ValueError("Starting value must be within the specified range.")
        else:
            self.startingValue = abs(range[1] - range[0])//2
        self.label = label

class DynamicAxis:
    def __init__(self, name: int, isInput: bool, startingValue=None, label = None) -> None:
        self.name = name
        self.isInput = isInput
        self.startingValue = startingValue
        self.label = label


class Grid:
    def __init__ (self, name: str, outputAxes: list[DynamicAxis, StaticAxis] = [], inputAxes: list[DynamicAxis, StaticAxis] = [], table: list[list[float]] = []):
        self.name = name
        self.outputAxes = outputAxes
        self.inputAxes = inputAxes
        self.table = table
    
    def countOf(self, isDynamic: bool, isInput: bool) -> int:
        count = 0
        for axis in self.inputAxes.values() if isInput else self.outputAxes.values():
            if (isDynamic and isinstance(axis, DynamicAxis)) or (not isDynamic and isinstance(axis, StaticAxis)):
                count += 1
        return count

    def addStaticAxis(self, axis: StaticAxis) -> None:
        if axis.isInput:
            self.inputAxes.append(axis)
        else:
            self.outputAxes.append(axis)
    
    def addDynamicAxis(self, axis: DynamicAxis) -> None:
        if axis.name in self.inputAxes or axis.name in self.outputAxes:
            raise ValueError(f"An axis with the name {axis.name} already exists.")
        if axis.isInput:
            if self.countOf(isDynamic=True, isInput=True) >= 2:
                raise ValueError("Only one dynamic input axis is allowed.")
            self.inputAxes.append(axis)
        else:
            if self.countOf(isDynamic=True, isInput=False) >= 2:
                raise ValueError("Only one dynamic output axis is allowed.")
            self.outputAxes.append(axis)
    
    def setTable(self, table) -> None:
        if type(table) is str:
            if os.path.exists(table) and os.path.isfile(table):
                with open(table, 'r') as f:
                    text = f.read().split("\n")
                    self.table = [[float(x) for x in line.split(",")] for line in text]
            else:
                raise FileNotFoundError(f"File {table} does not exist.")
        elif type(table) is list:
            self.table = table
        else:
            raise TypeError("Table must be a filename or a list of lists.")
    
    def graphTable(self) -> None:
        img = None
        for i in range(max(len(self.inputAxes), len(self.outputAxes))):
            plt.clf()
            x , y = [], []
            for row in self.table:
                x.append(0.5)
                y.append(0.5)
                if i < len(self.inputAxes):
                    x[-1] = row[self.inputAxes[i].name]
                if i < len(self.outputAxes):
                    y[-1] = row[self.outputAxes[i].name]

            print(f"{x=}, {y=}")

            if i < len(self.inputAxes):
                plt.xlabel(self.inputAxes[i].label)
            if i < len(self.outputAxes):
                plt.ylabel(self.outputAxes[i].label)

            if min(y) != max(y):
                plt.ylim(min(y), max(y))
            else:
                plt.ylim(0, max(x))
                y = [max(x)/2 for d in y]
                plt.yticks([])

            if min(x) != max(x):
                plt.xlim(min(x), max(x))
            else:
                plt.xlim(0, max(y))
                x = [max(y)/2 for d in x]
                plt.xticks([])

            if img is None:
                plt.plot(x, y, linewidth=5)
                plt.savefig("input/output.png", dpi=300)
                img = mpimg.imread("input/output.png")
            else:
                plt.plot(x, y)
                for index, value in enumerate(x):
                    width = (max(x) - min(x))/len(x)
                    height = (max(y) - min(y))/len(y)

                    print(f"{width=} {height=}")

                    width = max(y) if width == 0 else width
                    height = max(x) if height == 0 else height

                    print(f"{width=} {height=}")

                    plt.imshow(img, extent=[value-width/2, value+width/2, y[index]-height/2, y[index]+height/2])
                plt.savefig("input/output.png", dpi=300)
                img = mpimg.imread("input/output.png")

        plt.title(f"Grid: {self.name}")
        plt.show()

def main(args=None):
    if len(args) != 2:
        raise ValueError("Two arguments required: table filename and grid name.")
    grid = Grid(name=args[1])
    grid.setTable(args[0])
    table = grid.table

    if len(table) == 0 or len(table[0]) == 0:
        raise ValueError("Table cannot be empty.")
    
    threshold = len(table[0]) // 2
    for i in range(len(table[0])):
        axis = StaticAxis(name=i, range=(0, 3), ticks=5, isInput=(i < threshold), label= f"x{i}" if i < threshold else f"y{i - threshold}")
        grid.addStaticAxis(axis)
    
    print([axis.name for axis in grid.inputAxes])
    print([axis.name for axis in grid.outputAxes])

    grid.graphTable()

if __name__ == "__main__":
    main(args=sys.argv[1:])