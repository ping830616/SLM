# Author | Eduardo Ortega
import numpy as np
import matplotlib.pyplot as plt
vth=0.45
vdd = 1000
k = 2.02 / 1000


def convert_cel_kelvin(c):
    return c + 273.15
    
def return_vth_shift(c):
    kelvin = convert_cel_kelvin(c)
    vth_shift = vth - (k* (kelvin - 300 ))
    return vth_shift

def delay_comp(droop, temp):
    vth_shift = return_vth_shift(temp)
    top = 1 - (vth_shift / (vdd / 1000))
    bottom = 1 - (vth_shift / ((vdd-droop) / 1000))
    norm_val = top / bottom
    print(droop, temp)
    print(vth, vth_shift)
    print(norm_val)
    print("----------------")
    return norm_val

def main():
    droop = [10, 50, 100, 150, 200, 250]
    droop.reverse()
    temp =  [20, 40, 60,  80,  100,  120]
    z = []
    for d in droop:
        z_y = []
        for t in temp:
            path_delay = delay_comp(d, t)
            z_y.append(path_delay)
        z.append(np.array(z_y))
    z = np.array(z)
    fig, ax = plt.subplots(1,1)
    im = ax.imshow(z, cmap='jet')
    fig.colorbar(im, ax=ax, shrink=0.9)
    ax.set_xticks(np.arange(len(temp)))
    ax.set_xticklabels(temp)
    ax.set_xlabel('Temperature (C)', fontweight='bold')
    ax.set_yticks(np.arange(len(droop)))
    ax.set_yticklabels(droop)
    ax.set_ylabel('Voltage Droop (mV)', fontweight='bold')
    plt.show()

if __name__=="__main__":
    main()
