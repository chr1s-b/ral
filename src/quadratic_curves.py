from random import uniform
from random import randint
from math import sqrt

def quadratic(points_list):

        x0 = float(points_list[0])
        y0 = float(points_list[1])
        x1 = float(points_list[2])
        y1 = float(points_list[3])
        x2 = float(points_list[4])
        y2 = float(points_list[5])

        x_2_coeff = ((y1-y2)*(x0-x1)-(y0-y1)*(x1-x2))/((x1**2 - x2**2)*(x0-x1) - (x0**2-x1**2)*(x1-x2))
        x_coeff = ((y1-y2)*(x0**2-x1**2)-(y0-y1)*(x1**2-x2**2))/((x0**2-x1**2)*(x1-x2)-(x1**2-x2**2)*(x0-x1))
        coeff_1   = x0*x1*y2/((-x0 + x2)*(-x1 + x2)) + x0*x2*y1/((-x0 + x1)*(x1 - x2)) + x1*x2*y0/((x0 - x1)*(x0 - x2))

        return x_2_coeff, x_coeff, coeff_1

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

                points = [x0, y0, x1, y1, x2, y2]
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

def main():
        num_sets = 1
        rad_0 = 2
        rad_1 = 5
        rad_2 = 9
        points = gen_circle_points(rad_0, rad_1, rad_2, num_sets)

        for i in range(num_sets):
                print(points[i], quadratic(points[i]))

if __name__ == "__main__":
        main()
