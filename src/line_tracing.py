"""
Created on Thu Aug 16 11:52:33 2018
Author: olliebreach

Description: 
"""

import numpy as np
import matplotlib.pyplot as plt
from random import randint
from math import degrees, radians, atan
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
    print(len(points))
    for i in range(sets):
        #select three random points
        combo = [points[randint(0,len(points)-1)] for j in range(3)]
        combos.append(combo)
    return combos

def transform_data(data):
    new_data = []
    for i in data:
        points = []
        for point in i:
            r = np.sqrt(point[0]**2 + point[1]**2)
            theta = degrees(np.arctan2(point[1], point[0]))
            z = point[2]
            new_point = (r, theta, z)
            points.append(new_point)
        new_data.append(points)
    
    return new_data

def road_angle(points):
    
    sorted_points = sorted(points, key=lambda tup: abs(tup[0]*np.sin(tup[1])))
    r1, theta1, z1 = sorted_points[0]
    r2, theta2, z2 = sorted_points[1]
    r3, theta3, z3 = sorted_points[2]
    
    a = r3*np.sin(theta3) - r1*np.sin(theta1)
    b = (z3 + r3*np.cos(theta3)) - (z1 + r1*np.cos(theta1))
    c = r2*np.sin(theta2) - r1*np.sin(theta1)
    d = (z2 + r2*np.cos(theta3)) - (z1 + r1*np.cos(theta1))
    
    road = degrees(np.arctan2(a, b) - np.arctan2(c, d))
    return road
    
def is_line_rtz(points):
    road = road_angle(points)
    
    if road <= 0.5:
        return True
    else:
        return False
    
def line_angle(points):
    sorted_points = sorted(points, key=lambda tup: abs(tup[0]*np.sin(tup[1])))
    r1, theta1, z1 = sorted_points[0]
    r2, theta2, z2 = sorted_points[1]
    r3, theta3, z3 = sorted_points[2]
    
    a = r3*np.sin(theta3) - r1*np.sin(theta1)
    b = (z3 + r3*np.cos(theta3)) - (z1 + r1*np.cos(theta1))
    c = r2*np.sin(theta2) - r1*np.sin(theta1)
    d = (z2 + r2*np.cos(theta3)) - (z1 + r1*np.cos(theta1))
    
    y = atan(a/b)
    x = atan(c/d)
    angle = (x + y)/2
    return angle

def plot_line_rtz(points):
    angle = line_angle(points)
    sorted_points = sorted(points, key=lambda tup: abs(tup[0]*np.sin(tup[1])))
    grad = np.tan(radians(angle))
    cpoint1 = (sorted_points[0][2] + sorted_points[0][0]*np.cos(sorted_points[0][1]), sorted_points[0][0]*np.sin(sorted_points[0][1]) )
    cpoint2 = (sorted_points[1][2] + sorted_points[1][0]*np.cos(sorted_points[1][1]), sorted_points[1][0]*np.sin(sorted_points[1][1]) )
    cpoint3 =(sorted_points[2][2] + sorted_points[2][0]*np.cos(sorted_points[2][1]), sorted_points[2][0]*np.sin(sorted_points[2][1]) )
    converted_points = [cpoint1, cpoint2, cpoint3]
    yend = sorted_points[2][1]
    
    y = np.linspace(0, yend, 100)
    z = ((y - sorted_points[0][1] + grad*sorted_points[0][0])/grad)
    plt.plot(z, y)

def lines(data):
    lines = []
    
    for i in data:
        if is_line_rtz(i):
            print(str(i)+" is a line with angle "+str(line_angle(i)))
            lines.append(i)
            plot_line_rtz(i)
            
    if len(lines) != 0:
        sorted_lines = sorted(lines, key = lambda tup: tup[0])
        minz = sorted_lines[0][0]
        maxz = sorted_lines [len(sorted_lines)-1][0]
        plt.plot([minz, maxz], [0,0])

def main():
    xyz = realdata_xyz(100)
    data = transform_data(xyz)
    lines(data)

if __name__ == "__main__":
    main()    
    
