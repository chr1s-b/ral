from pathtracing import *
from line_tracing import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main():
    print("Starting")
    # config variables
    config = {"radii": (100, 500, 1000),
              "tolerance": 100,
              "road": 70,
              "acc": 2,
              "point sets": 100000,
              "min radius": 1000,
              "sideroad": 1,
              "3D": False}
    print("Generating data")
    data = realdata_xyz(config["point sets"])
    print("Generated {} sets of points".format(len(data)))
    print("Calculating side projection")
    xyz, sidexy, sidemc = sidecheck(data,
                                    config["sideroad"])
    print("Points left:",len(xyz))
    print("Generating a reference")
    linedata = {}
    for i, trio in enumerate(xyz):
        linedata[str(trio)] = [sidexy[i], sidemc[i]]
    print("Calculating front projection")
    xyz = front_check(xyz, config)
    print("Rechecking references")
    sidexy=[]
    sidemc=[]
    for trio in xyz:
        sidexy.append(linedata[str(trio)][0])
        sidemc.append(linedata[str(trio)][1])
    print("Points left:",len(xyz))
    plt.figure(1)
    print("Rendering front view")
    #plt.subplot(201)
    front_view(xyz, config)
    print("Rendering side view")
    #plt.subplot(200)
    plt.figure(2)
    side_view(sidexy, sidemc)
    
    #3D
    if config["3D"]:
        print("Rendering 3D point scatter")
        fig = plt.figure(3)
        ax = fig.add_subplot(111,projection='3d')
        for trio in data:
            for point in trio:
                x, y, z = point
                r = sqrt(x**2 + y**2 + z**2)
                c = hsv_to_rgb((r/5200., 1, 1))
                ax.plot([x], [z], [y], 'r+', color=c, alpha=0.7)
        #ax.set_axis_off()      
    
    plt.show()
    return

if __name__ == "__main__":
    main()
