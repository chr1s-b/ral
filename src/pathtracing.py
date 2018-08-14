import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, isnan
from random import uniform, randint

def gen_circle_points(rad_0, rad_1, rad_2, num_sets):
        points_list = []

        for i in range(num_sets):
                x0 = uniform(0, rad_0)
                y0 = sqrt(rad_0**2 - x0**2)
                x1 = uniform(0, rad_1)
                y1 = sqrt(rad_1**2 - x1**2)
                x2 = uniform(0, rad_2)
                y2 = sqrt(rad_2**2 - x2**2)

                a  = randint(0,1)
                if a == 1:
                        y0 = -y0

                b  = randint(0,1)
                if b == 1:
                        y1 = -y1

                c  = randint(0,1)
                if c==1:
                        y2 = -y2

                points = [(x0, y0), (x1, y1), (x2, y2)]
                points_list.append(points)

        return points_list

def gen_points(num_sets):

        points_list = []

        for i in range(num_sets):
                point_set = []
                for i in range(6):
                        point_set.append(uniform(-10, 10))
                points_list.append(point_set)

        return points_list
    
def perpline(line, offset):
    x = offset[0] + line[0]/2 #midpoint x
    y = offset[1] + line[1]/2 #midpoint y
    if (line[0] != 0) and (line[1] != 0):
        g = -1 / (line[1] / float(line[0]))
    elif line[0] == 0:
        return 1, 0, y            #perpendicular line is horizontal: 1y = 0x + const
    else: #line[1] == 0
        return 0, 1, x           #perpendicular line is vertical: x = const + 0y --> 0y = x - const
    c = y - (g * x)
    return 1, g, c

def center(points):
    #unpack points
    a, b, c = points

    #find xy deltas of ab and cb
    ab = [a[0] - b[0], a[1] - b[1]]
    cb = [c[0] - b[0], c[1] - b[1]]

    #find perpendicular line from ab
    y, g1, c1 = perpline(ab, b)

    #find perpendicular line from cb
    y, g2, c2 = perpline(cb, b)

    #form and solve simultaneous equations
    #print("y = {}x + {}".format(g1, c1))
    #print("y = {}x + {}".format(g2, c2))
    A = np.array([[y,-g1],[y,-g2]])      #y = 0x + c
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

def plot_circle(r, cx, cy, color):
    xs = []; ys = []
    x = -r
    while x <= r:
       y = sqrt(r ** 2 - x ** 2)
       xs.append(x+cx); ys.append(y+cy);
       x += 0.1
    plt.plot(xs, ys, color=color)
    ys = [2*cy - y for y in ys]
    plt.plot(xs, ys, color=color)

def plot(points, cen, r, a, b, c, radii):
    if (r != "N/A"):
        plt.xlim(cen[0] - r-2, cen[0] + r + 2) #circle plus padding
        plt.ylim(cen[1] - r-2, cen[1] + r + 2) #circle plus padding
        plt.autoscale(False)
        
    
    #plot points
    plt.plot([x for x, y in points],
             [y for x, y in points], 'ro', color="red")
    
    #plot circle and center
    if (r != "N/A"):
        plt.plot([cen[0]], [cen[1]], 'ro', color="blue")
        plot_circle(r, cen[0], cen[1], "green")
        
    for r in radii:
        plot_circle(r, 0, 0, "black")
        
    plot_quadratic(a, b, c)
    
    plt.show()
    return

def circle(points):
    c = center(points)
    if c[0] == "N/A": return c #returns 2 x "N/A"
    r = sqrt((points[0][0] - c[0])**2 +
                  (points[0][1] - c[1])**2)
    return c, r

def quadratic(points):
        x0, y0 = points[0]
        x1, y1 = points[1]
        x2, y2 = points[2]

        x_2_coeff = ((y1-y2)*(x0-x1)-(y0-y1)*(x1-x2))/((x1**2 - x2**2)*(x0-x1) - (x0**2-x1**2)*(x1-x2))
        x_coeff = ((y1-y2)*(x0**2-x1**2)-(y0-y1)*(x1**2-x2**2))/((x0**2-x1**2)*(x1-x2)-(x1**2-x2**2)*(x0-x1))
        coeff_1   = x0*x1*y2/((-x0 + x2)*(-x1 + x2)) + x0*x2*y1/((-x0 + x1)*(x1 - x2)) + x1*x2*y0/((x0 - x1)*(x0 - x2))
        return x_2_coeff, x_coeff, coeff_1

def plot_quadratic(a,b,c):
    xs = []; ys = []
    x = -10
    while x <= 10:
        y = a * (x ** 2) + b * x + c
        xs.append(x); ys.append(y);
        x += 0.1
    plt.plot(xs, ys, color="blue")
    return

if __name__ == "__main__":
    r_1, r_2, r_3 = 2, 7, 10
    for i in range(5): #how many to show (in series)
        points = gen_circle_points(r_1,r_2,r_3,1)[0]
        print("Points: "+str(points))
        cen, r = circle(points)
        print("Center: "+str(cen))
        print("Radius: "+str(r))
        a, b, c = quadratic(points)
        print("Quadratic: {}x^2+{}x+{}".format(a,b,c))
        plot(points, cen, r, a, b, c, (r_1, r_2, r_3))
        print("="*40)
