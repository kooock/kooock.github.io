from matplotlib import pyplot as mplp
import math

def draw_graph(x, y,label):
    mplp.plot(x, y,label=label)



def xrange(start, final, interval):
    numbers = []
    while start < final:
        numbers.append(start)
        start += interval
    return numbers

def make_graph_x_y(amin,amax,n):
    a = xrange(amin, amax, 0.00001)
    y = []
    for x in a:
        y.append(math.pow(1+4*x,n/2) * math.pow(1-x,n/2))
    draw_graph(a, y, "n is {}".format(n))




if __name__ == "__main__":
    mplp.xlabel('x-coordinate')
    mplp.ylabel('y-coordinate')
    mplp.title('Funcion Graph')

    xmin = 0
    xmax = 1

    make_graph_x_y(xmin, xmax, 10)
    make_graph_x_y(xmin,xmax,20)
    make_graph_x_y(xmin, xmax, 30)
    make_graph_x_y(xmin, xmax, 40)
    make_graph_x_y(xmin,xmax,50)


    mplp.grid()
    mplp.legend()
    mplp.show()
