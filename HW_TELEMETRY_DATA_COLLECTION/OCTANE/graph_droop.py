# Author | Eduardo Ortega
import glob, os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def main():
    fig, ax = plt.subplots(1, 2)
    list_of_data = glob.glob('../TELEMETRY_DATA/*.csv')
    workload = [d.split("_")[-1].split('.')[0].strip() for d in list_of_data]
    benign = [d for d in list_of_data if 'benign' in d]
    droop = [d for d in list_of_data if 'DROOP' in d]
    for idx, sys in enumerate(['DDR4', 'DDR5']):
        title = 'SETUP A' if sys == 'DDR4' else 'SETUP B'
        for volt_list in [benign, droop]:
            volt_sys = [d for d in volt_list if sys in d]
            volt_dist = []
            for d in volt_sys:
                df = pd.read_csv(d)
                voltage = np.array(df['CPU Voltage'].tolist())
                volt_dist.append(voltage)
            volt_dist = np.array(volt_dist)
            num_data = volt_dist.shape[1]
            min_volt, max_volt, q1_volt, q3_volt, med_volt = [], [], [], [], []
            for d in range(num_data):
                values = volt_dist[:,d].flatten()
                min_volt.append(min(values))
                max_volt.append(max(values))
                q1_volt.append(np.percentile(values, 25))
                q3_volt.append(np.percentile(values, 75))
                med_volt.append(np.median(values))
            x_ax = [x for x in range(num_data)]
            max_x = max(x_ax)
            x_ax = [x / max_x for x in x_ax]
            x_ax = [10.0*x for x in x_ax]
            volt_label = 'Benign' if volt_list == benign else 'Forced Droop'
            c_volt = 'b' if volt_list == benign else 'r'
            ax[idx].plot(x_ax, med_volt, label=volt_label, color=c_volt)
            ax[idx].fill_between(x_ax, q1_volt, q3_volt, color=c_volt, alpha=0.3)
            #ax[idx].fill_between(x_ax, min_volt, max_volt, color=c_volt, alpha=0.1)
            ax[idx].set_xlabel('Time (s)', fontsize=12) #fontweight='bold')
            ax[idx].set_ylabel('Voltage (V)', fontsize=12) #fontweight='bold')
        ax[idx].set_title(f'{title}', fontsize=12) #fontweight='bold')
        #ax[idx].set_ylim((0.95, 1.3))
    ax[1].legend(ncol=2, shadow=True, fancybox=True, loc='lower center', bbox_to_anchor=(-0.15, -0.6))
    plt.show()
        

if __name__=="__main__":
    main()
