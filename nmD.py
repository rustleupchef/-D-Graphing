import sys

class StaticAxis:
    def __init__(self, name: str, range: tuple, isInput: bool, startingValue=None):
        self.name = name
        self.range = range
        self.isInput = isInput
        self.startingValue = startingValue
        if startingValue is not None:
            if not (range[0] <= startingValue <= range[1]):
                raise ValueError("Starting value must be within the specified range.")
        else:
            self.startingValue = abs(range[1] - range[0])//2

class DynamicAxis:
    def __init__(self, name: str, axis: int, isInput: bool, startingValue=None):
        self.name = name
        self.axis = axis
        self.isInput = isInput
        self.startingValue = startingValue
        
class Grid:
    def __init__ (self, name: str, outputAxes = [], inputAxes = []):
        self.name = name
        self.outputAxes = outputAxes
        self.inputAxes = inputAxes
    

def main(args=None):
    pass

if __name__ == "__main__":
    main(args=sys.argv[1:])