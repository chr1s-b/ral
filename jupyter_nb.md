

```python
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, isnan

def perpline(line, offset):
    x = offset[0] + line[0]/2
    y = offset[1] + line[1]/2
    if (line[0] != 0) and (line[1] != 0):
        g = -1 / (line[1] / float(line[0]))
    elif line[0] == 0:
        print("[WARNING] A linear equation has determined a gradient of infinity (vertical). This may cause unexpected behaviour.")
        return np.Infinity, 0             #(determined result of following line when g=infinity) <- vertical
    else:
        return 0, y                       #(determined result of following line when g=0) <- horizontal
    c = y - (g * x)
    return g, c

def center(points):
    #unpack points
    a, b, c = points

    #find xy deltas of ab and cb
    ab = [a[0] - b[0], a[1] - b[1]]
    cb = [c[0] - b[0], c[1] - b[1]]

    #find perpendicular line from ab
    g1, c1 = perpline(ab, b)

    #find perpendicular line from cb
    g2, c2 = perpline(cb, b)

    #form and solve simultaneous equations
    #print("y = {}x + {}".format(g1, c1))
    #print("y = {}x + {}".format(g2, c2))
    A = np.array([[1,-g1],[1,-g2]])
    B = np.array([c1, c2])
    try:
        C = np.linalg.solve(A,B)
    except:
        print("[INFO] No reasonable solution, or one or more linear equations were parallel to an axis.\n       Please use a different tracing method (parabola).")
        return "N/A", "N/A"
    #return solution
    if (isnan(C[0]) or isnan(C[1])): return "N/A", "N/A"
    y, x = C[0], C[1]
    return x, y

def plot(points):
    c = center(points)
    r = sqrt((points[0][0] - c[0])**2 +
                  (points[0][1] - c[1])**2)
    plt.xlim(c[0] - r-2, c[0] + r + 2) #circle plus padding
    plt.ylim(c[1] - r-2, c[1] + r + 2) #circle plus padding
    plt.autoscale(False)
    plt.plot([x for x, y in points],
             [y for x, y in points], 'ro')

    plt.plot([c[0]], [c[1]], 'ro', color="blue")

    xs = []; ys = []
    x = -r
    while x <= r:
        y = sqrt(r ** 2 - x ** 2)
        if x == 0: print(y)
        xs.append(x+c[0]); ys.append(y+c[1]);
        x += 0.1
    plt.plot(xs, ys, color="green")
    ys = [2*c[1]-y for y in ys]
    plt.plot(xs, ys, color="green")
    plt.show()
    return

def circle(points):
    c = center(points)
    if c[0] == "N/A": return c #returns 2 x "N/A"
    r = sqrt((points[0][0] - c[0])**2 +
                  (points[0][1] - c[1])**2)
    return c, r

def quadratic(points):

        '''x0 = points[0][0]
        y0 = points[0][1]
        x1 = points[1][0]
        y1 = points[1][1]
        x2 = points[2][0]
        y2 = points[2][1]'''
        x0, y0 = points[0]
        x1, y1 = points[1]
        x2, y2 = points[2]

        x_2_coeff = (y0/((x0 - x1)*(x0 - x2)) + y1/((-x0 + x1)*(x1 - x2)) + y2/((-x0 + x2)*(-x1 + x2)))

        x_coeff   = (-x0*y1/((-x0 + x1)*(x1 - x2)) - x0*y2/((-x0 + x2)*(-x1 + x2)) - x1*y0/((x0 - x1)*(x0 - x2)) - x1*y2/((-x0$

        coeff_1   = x0*x1*y2/((-x0 + x2)*(-x1 + x2)) + x0*x2*y1/((-x0 + x1)*(x1 - x2)) + x1*x2*y0/((x0 - x1)*(x0 - x2))

        #return x_2_coeff*x**2 + x_coeff*x + coeff_1*1
        return x_2_coeff, x_coeff, coeff_1

def plot_quadratic(a,b,c):
    return

if __name__ == "__main__":
    from random import randint as rint
    for i in range(1): #how many to show (in series)
        points = ((rint(-10,10),rint(-10,10)),
                  (rint(-10,10),rint(-10,10)),
                  (rint(-10,10),rint(-10,10)))
        print("Points: "+str(points))
        c, r = circle(points)
        print("Center: "+str(c))
        print("Radius: "+str(r))
        a, b, c = quadratic(points)
        print("Quadratic: {}x^2+{}x+{}".format(a,b,c))                                                                                        
        print("\n---------------------------------\n")
        if (r != "N/A"): plot(points)

```


      File "<ipython-input-10-de6117c29da4>", line 91
        x_coeff   = (-x0*y1/((-x0 + x1)*(x1 - x2)) - x0*y2/((-x0 + x2)*(-x1 + x2)) - x1*y0/((x0 - x1)*(x0 - x2)) - x1*y2/((-x0$
                                                                                                                              ^
    SyntaxError: invalid syntax


