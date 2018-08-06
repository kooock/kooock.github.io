from matplotlib import pyplot as mplp
import math
import random

def draw_graph(x, y,label):
    mplp.plot(x, y,label=label)



def xrange(start, final, interval):
    numbers = []
    while start < final:
        numbers.append(start)
        start += interval
    return numbers

def make_graph_x_y(xmin,xmax):
    a = xrange(xmin, xmax, 1)
    y_point = 0
    y = []
    for x in a:
