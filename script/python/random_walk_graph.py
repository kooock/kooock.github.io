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
        i = random.randint(0,1)
        if i:
            y_point += 1
        else:
            y_point -= 1

        y.append(y_point)
    draw_graph(a, y, "random walk")



if __name__ == "__main__":
    mplp.xlabel('time')
    mplp.ylabel('point')
    mplp.title('Funcion Graph')

    xmin = 0
    xmax = 100000

    make_graph_x_y(xmin,xmax)
