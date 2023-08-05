# type hinting
from typing import Any
# plotly plotting library
import plotly.graph_objs as go

###
### Class definitions
###
class DataSet:
    """
    Contains information about one DataSet.

    A DataSet represents one row of data.
    """

    # type hints
    Data: list
    Row: int


    def __init__(self, index: int, rowStr: str):
        self.Data = []
        self.Row = index
        self.ReadData(rowStr)


    def ReadData(self, rowStr: str):
        """Convert string data to numerical data.

        Args:
            rowStr (str): The row as a string, maybe from the file directly.
        """
        # split the row at any whitespace
        for data in rowStr.split():
            # append the float representation to the data
            self.Data.append(float(data))

    def filter(self, function):
        """Filters the data of this set.

        Args:
            function (function): A function which gets a list as an argument and returns a list.
        """
        self.Data = function(self.Data)

class DataPlotter:
    """
    Contains a set of DataSets and is able to plot them.

    Before plotting, apply a filter function.
    """

    DataSets: list[DataSet]
    Filter: Any
    Columns: int

    def __init__(self, path):
        """Create the DataPlotter.

        Args:
            path (str): File to be plotted.
        """
        # create datasets
        self.DataSets = []
        # create default filter
        self.Filter = lambda x: []
        # initialize default column count
        self.Columns = 0

        # open a filestream to the file
        with open(path, 'r') as dataFile:
            # read all lines from the file
            lines = dataFile.readlines()

            # enumerate all lines and count (index is stored in row)
            for row, line in enumerate(lines):
                # append a new class instance of DataSets
                self.DataSets.append(DataSet(row, line))
                
                # save maximum amount of columns
                self.Columns = max(self.Columns, len(self.DataSets[-1].Data)-1)


    def plot(self):
        """ Plot the data. """
        # get the x values of the datasets
        x = [xi.Data[0] for xi in self.DataSets]
        # extract all y values from the datasets
        y = [yi.Data[1:] for yi in self.DataSets]
        
        lines = []

        for col in range(self.Columns):
            # extract current y value from y list
            cury = [yi[col] for yi in y]

            lines.append(go.Scatter(x=x, y=cury, name=f'Column {col+1}'))
        
        fig = go.Figure(data=lines)
        fig.show()

    def filterData(self, function = None ) -> None:
        """ Filter all data and check for additional columns. """
        if function != None:
            for data in self.DataSets:
                data.filter(function)
                self.Columns = max(self.Columns, len(data.Data)-1)

        else:
            for data in self.DataSets:
                data.filter(self.Filter)
                self.Columns = max(self.Columns, len(data.Data)-1)
        


###
### Scripting area
###

if __name__ == '__main__':
    firstSet = DataSet(0, "1 2")
    print(firstSet.Row)