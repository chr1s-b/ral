import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, isnan
from random import uniform, randint

def gen_circle_points(radii, num_sets):
        points_list = []

        for i in range(num_sets):
            points = []
            
            for r in radii:
                a = randint(0,1)
                x = uniform(-r,r)
                y = sqrt(r**2 - x**2)
                if a == 0: y = -y
                points.append((x,y))
                
            points_list.append(points)
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
    A = np.array([[y,-g1],[y,-g2]])
    B = np.array([c1, c2])
    try:
        C = np.linalg.solve(A,B)
    except:
        print("[WARN] Lines do not converge, no real solution by this method.\n       Please use a different tracing method (parabola).")
        return "N/A", "N/A"
    #return solution
    if (isnan(C[0]) or isnan(C[1])): return "N/A", "N/A"
    y, x = C[0], C[1]
    return x, y

def plot_circle(r, cx, cy, color, lw=2):
    xs = []; ys = []
    x = -r
    while x <= r:
       y = sqrt(r ** 2 - x ** 2)
       xs.append(x+cx); ys.append(y+cy);
       x += 0.1
    plt.plot(xs, ys, color=color, linewidth=lw)
    ys = [2*cy - y for y in ys]
    plt.plot(xs, ys, color=color, linewidth=lw)

def plot_setup(radii, tolerance):
    plt.xlim(-radii[-1] -2, radii[-1] +2) #2 units padding
    plt.ylim(-radii[-1] -2, radii[-1] +2)
    plt.autoscale(False)
    
    #plot 'detector' rings
    for r in radii:
        plot_circle(r, 0, 0, "black", lw=0.8)
    
    #plot tolerance
    plot_circle(tolerance, 0, 0, "red", lw= 1)
    
    #plot origin
    plt.plot([0],[0], 'ro', color="black")
    return

def plot(points, acc, tolerance): #points and feedback accuracy for rounding output
    cen, r = circle(points)
    print("Center: ({},{})".format(round(cen[0],acc),round(cen[1],acc)))
    print("Radius: "+str(round(r,acc)))
    a, b, c = quadratic(points)
    print("Quadratic: {}x^2+{}x+{}".format(round(a,acc),round(b,acc),round(c,acc)))
    
    #plot circle and center
    if (r != "N/A"):
        if circle_near_origin(r, cen, tolerance):
            plt.plot([cen[0]], [cen[1]], 'ro', color="blue")
            plot_circle(r, cen[0], cen[1], "green")
            print("Circle plotted: TRUE")
        else:
            print("Circle plotted: FALSE")
    
    #plot the quadratic
    if quad_near_origin([a,b,c,], tolerance):
        plot_quadratic(a, b, c)
        print("Quadratic plotted: TRUE")
    else:
        print("Quadratic plotted: FALSE")
    
    #plot points
    plt.plot([x for x, y in points],
             [y for x, y in points], 'ro', color="red")
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

def quad_near_origin(coeffs, tolerance):
        t = tolerance
        x = -t
        a, b, c = coeffs[0], coeffs[1], coeffs[2]
        while x <= t:
            y = a*x**2 + b*x + c
            if sqrt(x**2+y**2) <= t: return True
            x += 0.025
        return False
    
def circle_near_origin(radius, centre, tolerance):
        a = centre[0]
        b = centre[1]

        dist = sqrt(a**2 + b**2)
        return (abs(dist - radius) <= tolerance)
        
def plot_quadratic(a,b,c):
    xs = []; ys = []
    x = -10
    while x <= 10:
        y = a * (x ** 2) + b * x + c
        xs.append(x); ys.append(y);
        x += 0.1
    plt.plot(xs, ys, color="blue")
    return

def gen_lots(radii, num_sets):
    points_r1 = []
    points_r2 = []
    points_r3 = []
    
    r1 = radii[0]
    r2 = radii[1]
    r3 = radii[2]
    
    for i in range(num_sets):
        a = randint(0,1)
        x = uniform(-r1,r1)
        y = sqrt(r1**2 - x**2)
        if a == 0: y = -y
        points_r1.append((x,y))
        
    for i in range(num_sets):
        a = randint(0,1)
        x = uniform(-r2,r2)
        y = sqrt(r2**2 - x**2)
        if a == 0: y = -y
        points_r2.append((x,y))
        
    for i in range(num_sets):
        a = randint(0,1)
        x = uniform(-r3,r3)
        y = sqrt(r3**2 - x**2)
        if a == 0: y = -y
        points_r3.append((x,y))
        
    return points_r1, points_r2, points_r3

def combinations(points_r1, points_r2, points_r3):
    combo_list = []
    
    for i in points_r1:
        for n in points_r2:
            for m in points_r3:
                point_set = [i, n, m]
                combo_list.append(point_set)
    return combo_list

def check_points(combinations, tolerance):
    good_combos_circle = []
    good_combos_quad = []
    for i in combinations:
        coeffs = quadratic(i)
        c, r = circle(i)
        quad_orig = quad_near_origin(coeffs, tolerance)
        circ_orig = circle_near_origin(r, c, tolerance)
        if quad_orig == True:
            good_combos_quad.append(i)
        if circ_orig == True:
            good_combos_circle.append(i)
    return good_combos_circle, good_combos_quad

if __name__ == "__main__":
    print("="*40)
    radii = (3, 7, 11)
    tolerance = 1
    acc = 2 #accuracy of output
    num_sets = 10
    plot_setup(radii, tolerance)
    for i in range(num_sets): #how many to show (in series)
        points = gen_circle_points(radii,1)[0]
        rounded_points = [(round(point[0], acc), round(point[1],acc)) for point in points]
        print("Points: "+str(rounded_points))
        plot(points, acc, tolerance)
        print("="*50)
    print("Tolerance: {}".format(tolerance))
    plt.show() #unindented to show all plots on one graph
