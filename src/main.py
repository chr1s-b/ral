from pathtracing import *
from line_tracing import *
import matplotlib.pyplot as plt

def main():
    print("Starting")
    # config variables
    config = {"radii": (100, 500, 1000),
              "tolerance": 1000,
              "road": 70,
              "acc": 2,
              "point sets": 1000000,
              "min radius": 1000,
              "sideroad": 1}
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
    plt.show()
    return

if __name__ == "__main__":
    main()
