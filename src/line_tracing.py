import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from random import randint, uniform
from math import sin, acos, pi, sqrt, atan, degrees
import urllib.request

def realdata_xyz(sets):
    with urllib.request.urlopen('https://gist.githubusercontent.com/StewMH/9f75f8c2915e33b4248ed994173ebc53/raw/03a4f4221a424167beb824ad902768c900a08c50/event') as response:
        code = response.read().decode().split("\n")[1:]
    layers = {}
    for i in range(2,15):
        layers[i] = []
    for line in code:
        try:
            l = line.split(",")
            x, y, z = float(l[1]), float(l[2]), float(l[3])
            layer = int(l[5])
            point = (x, y, z)
            layers[layer].append(point)
        except:
            continue
    combos = []
    points = []
    min_layer = 2
    max_layer = 14
    for i in range(min_layer, max_layer+1):
        points += layers[i]
    for i in range(sets):
        #select three random points
        combo = [points[randint(0,len(points)-1)] for j in range(3)]
        combos.append(combo)
    return combos

def angle(point):
    if point[0] > 0: #right quadrants
        if point[1] > 0: #top right
            return degrees(atan(point[0]/point[1]))
        elif point[1] < 0: #bottom right
            return 180 + degrees(atan(point[0]/point[1]))
        return 90
    elif point[0] < 0: #left quadrants
        if point[1] > 0: #top left
            return 360 + degrees(atan(point[0]/point[1]))
        elif point[1] < 0:         #bottom left
            return 180 + degrees(atan(point[0]/point[1]))
        return 270
    if point[1] > 0: return 0
    return 180

def sector(ps):
    angles = []
    for point in ps:
        angles.append(angle(point))
    angles = sorted(angles)
    sector = angles[-1] - angles[0]
    return sector    

def minsector(points):
    s = [sector(points)] 
    #switch points locally to find minimum sector
    npoints = []
    for p in points:
        npoints.append((p[1],p[0]))
    s.append(sector(npoints))
    return sorted(s)[0]

def radius(point):
    x, y, z = point
    #3d pythagoras
    return sqrt(x**2 + y**2 + z**2)
        
def transform_data(xyz):
    rtz = []
    for trio in xyz:
        new_trio = []
        for point in trio:
            #get radius
            r = radius(point)
            #get theta
            z = point[2]
            t = acos(z/float(r))
            if point[1] < 0: t = -t
            #use z and append
            new_trio.append((r,t,z))
        rtz.append(new_trio)
    return rtz

def rtz_to_xy(rtz):
    xy = []
    for trio in rtz:
        new_trio = []
        for point in trio:
            r, t, z = point
            #basic trig
            y = r * sin(t)
            x = z
            new_trio.append((x,y))
        xy.append(new_trio)
    return xy
    
def checkroads(combos, road):
    good = []
    for combo in combos:
        if minsector(combo) < road:
            good.append(combo)
    return good

def plot(points, lines):
    for trio, line in zip(points,lines):
        color = hsv_to_rgb([uniform(0,1),1,1])
        #plot just points
        plt.plot([x for x,y in trio],
                [y for x, y in trio], 'ro', color=color, markersize=4, alpha=0.8)
        #plot lines of best fit 
        m, c = line
        x_int = -c/m
        outer = 3000; 
        if trio[0][0] < 0: 
            outer = -outer
        x = np.linspace(x_int,outer)
        y = m*x + c
        #plt.plot(x, y, color=color, alpha=0.8, linewidth=1)
    return

def linesof(xy):
    lines = []
    for trio in xy:
        mean_x = sum([x for x,y in trio])
        mean_y = sum([y for x,y in trio])

        top = sum([(x-mean_x)*(y-mean_y) for x,y in trio])
        bottom = sum([(x-mean_x)**2 for x,y in trio])
        m = top / bottom
            
        #y-intercept
        c = mean_y - m*mean_x
        lines.append((m,c))
    return lines

def side_view(xyz):
    rtz = transform_data(xyz)
    xy = rtz_to_xy(rtz)
    #xy = checkroads(xy, 5)
    #convert to a root along y=0,x=0 and return angle of line - these are best fits
    mc = linesof(xy)
    #setup plot
    plt.subplot(1,1,1)
    plt.title("Side view")
    #limit the plot
    plt.xlim(-1000, 1000)
    plt.ylim(-1000, 1000)
    plt.autoscale(False)
    plot(xy, mc)
    plt.show()

if __name__ == "__main__":
    data = realdata_xyz(100000)
    side_view(data) 
