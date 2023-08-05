# argparse for parsing of incoming arguments
import argparse

# argparse to parse arguments
from .Models import DataSet
from .Models import DataPlotter


# parse input with the help of an argument parser
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
# input path to specimen folder
parser.add_argument('-file', help='Path to file')

# read arguments
args = parser.parse_args()

# get the file path from arguments
filePath = args.file

# create the dataplotter
plotter = DataPlotter(filePath)

# calculate the difference of first columns
#   start with 1, bc 0 is x value
plotter.filterData(lambda l: l+ [abs(l[2]-l[1])])

# plot the data
plotter.plot()