# Author | Eduardo Ortega
import parse_log_for_training as f
import glob, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
dft_rowhammer = (f.dft, f.dft_rh)
dft_droop = (f.dft, f.dft_droop)

volt_key = "CPU Voltage"

def comp_good_vs_bad(data):
    safe, attack = data[0], data[1]
    good = glob.glob(f"TELEMETRY_DATA/{safe}.csv")[0]
    bad = glob.glob(f"TELEMETRY_DATA/{attack}.csv")[0]
    df_good = pd.read_csv(good)
    df_bad = pd.read_csv(bad)
    keys = list(df_good.keys())
    for k in keys:
        f_good, f_bad = df_good[k], df_bad[k]
        print(f"=======\n{k}")
        print("GOOD\tBAD")
        ave_g, ave_b = np.average(f_good), np.average(f_bad)
        cv_g, cv_b = np.std(f_good)/ave_g, np.std(f_bad)/ave_b
        print(f"AVE: {ave_g}\t{ave_b}")
        print(f"CV: {cv_g}\t{cv_b}")
        time.sleep(2)


def comp_voltage_droop(data):
    safe, droop = data[0], data[1]
    df_good = pd.read_csv(f"TELEMETRY_DATA/{safe}.csv")
    df_droop = pd.read_csv(f"TELEMETRY_DATA/{droop}.csv")
    print(len(list(df_good.keys())))
    quit()
    good_v = df_good[volt_key]
    droop_v = df_droop[volt_key]
    t = [(1/1000)*x for x in range(0, len(good_v))]
    plt.plot(t, good_v, label="Good Voltage")
    plt.plot(t, droop_v, label="Forced Droops")
    plt.xlabel('Time (s)', fontweight='bold')
    plt.ylabel('Voltage (V)', fontweight='bold')
    plt.legend(loc='upper center', 
            bbox_to_anchor=(0.5, 1.15), 
            shadow=True, 
            fancybox=True, 
            ncol=2)
    plt.show()

def main():
    #comp_good_vs_bad(pampar_dft_droop)
    comp_voltage_droop(pampar_dft_droop)

if __name__=="__main__":
    main()
