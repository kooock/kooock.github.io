from matplotlib import pyplot as mplp
import math
import random

def draw_graph(x, y,label):
    mplp.plot(x, y,label=label)



def xrange(start, final, interval):
    numbers = []
    while start < final:
