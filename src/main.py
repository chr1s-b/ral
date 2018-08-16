from pathtracing import *
from line_tracing import *
import matplotlib.pyplot as plt

def main():
    print("Starting")
    print("Generating data")
    data = realdata_xyz(100000)
    plt.figure(1)
    print("Rendering front view")
    #plt.subplot(201)
    front_view(data)
    print("Rendering side view")
    #plt.subplot(200)
    plt.figure(2)
    side_view(data)
    plt.show()
    return

if __name__ == "__main__":
    main()
