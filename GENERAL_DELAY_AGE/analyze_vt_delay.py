#Author | Eduardo Ortega
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

driver = 'driver'
stage_one = 'stage_one'
stage_two = 'stage_two'
stage_three = "stage_three"
stage_four = "stage_four"

def collect_timing_info(voltages, temp, df):
    info_list = [driver, stage_one, stage_two, stage_three, stage_four]
    dr_info = {}
    s1_info, s2_info, s3_info, s4_info = {}, {}, {}, {}
    info_dict = {driver:dr_info, stage_one:s1_info, stage_two:s2_info, stage_three:s3_info, stage_four:s4_info}
    time = df['t']
    for v in voltages:
        for t in temp:
             for i in info_list:
                key = f"{i}_{v}_{t}"
                print(i, key)
                time_series_data = df[key].to_list()
                idx, idx_found = 5000, False
                while idx < len(time_series_data) and not idx_found:
                    curr_volt = time_series_data[idx]
                    if curr_volt < 0.5: idx_found = True
                    idx += 1
                info_dict[i][f'{v}_{t}'] = time[idx]*(10**12)
    return info_dict
                
def compute_delays(info_dict, voltages, temp, plot=True):
    d1_dict = []
    d2_dict = []
    d3_dict = []
    d4_dict = []
    dr_dict = []
    bl_key = '1_20'
    driver_bl = info_dict[driver][bl_key]
    s1_bl = info_dict[stage_one][bl_key]
    s2_bl = info_dict[stage_two][bl_key]
    s3_bl = info_dict[stage_three][bl_key]
    s4_bl = info_dict[stage_four][bl_key]
    dl1_bl = s1_bl - driver_bl
    dl2_bl = s2_bl - driver_bl
    dl3_bl = s3_bl - driver_bl
    dl4_bl = s4_bl - driver_bl
    fig, ax = plt.subplots(1, 4)
    color_V = {voltages[0]:'m', voltages[1]:'b', voltages[2]:'g', voltages[3]:'r'}
    for v in voltages:
        d1_dict_y = []
        d2_dict_y = []
        d3_dict_y = []
        d4_dict_y = []
        dr_dict_y = []
        for t in temp:
            inner_key = f"{v}_{t}"
            driver_time = info_dict[driver][inner_key]
            s1_time = info_dict[stage_one][inner_key]
            s2_time = info_dict[stage_two][inner_key]
            s3_time = info_dict[stage_three][inner_key]
            s4_time = info_dict[stage_four][inner_key]
            delta_1_buffer = s1_time - driver_time
            delta_2_buffer = s2_time - driver_time
            delta_3_buffer = s3_time - driver_time
            delta_4_buffer = s4_time - driver_time
            #print(f"Voltage: {v}\t Temp: {t}")
            #print(f"delta 1 buffer              => {delta_1_buffer}")
            #print(f"delta 2 buffers             => {delta_2_buffer}")
            #print(f"delta 3 buffer              => {delta_3_buffer}")
            #print(f"delta 4 buffers             => {delta_4_buffer}")
            #print(f"====================================")
            #d1_dict_y.append(delta_1_buffer)
            #d2_dict_y.append(delta_2_buffer)
            #d3_dict_y.append(delta_3_buffer)
            #d4_dict_y.append(delta_4_buffer)
            d1_dict_y.append(delta_1_buffer/dl1_bl)
            d2_dict_y.append(delta_2_buffer/dl2_bl)
            d3_dict_y.append(delta_3_buffer/dl3_bl)
            d4_dict_y.append(delta_4_buffer/dl4_bl)
            dr_dict_y.append(driver_time)
        d1_dict.append(np.array(d1_dict_y))
        d2_dict.append(np.array(d2_dict_y))
        d3_dict.append(np.array(d3_dict_y))
        d4_dict.append(np.array(d4_dict_y))
        dr_dict.append(np.array(dr_dict_y))
        for idx, d_dict in enumerate([d1_dict_y, d2_dict_y, d3_dict_y, d4_dict_y]):
            print(f"{idx+1}, voltage: {v}")
            y_delta = d_dict[-1] - d_dict[0]
            x_delta = temp[-1] - temp[0]
            slope = y_delta / x_delta
            print(slope)
            print("============")
        ax[0].plot(temp, d1_dict_y, label=f'@ Voltage: {v}', c=color_V[v])
        ax[1].plot(temp, d2_dict_y, label=f'@ Voltage: {v}', c=color_V[v])
        ax[2].plot(temp, d3_dict_y, label=f'@ Voltage: {v}', c=color_V[v])
        ax[3].plot(temp, d4_dict_y, label=f'@ Voltage: {v}', c=color_V[v])
    for x in range(4):
        ax[x].set_ylabel('Norm. Slack')
        ax[x].set_xlabel('Temperature (C)')
        ax[x].set_title(f'Num of Buffer: {x+1}')
    ax[1].legend(shadow=True, 
                fancybox=True, 
                loc='upper center', 
                bbox_to_anchor=(1.05, 1.1), 
                ncol=4)
    #plt.show()
    for idx, d_dict in enumerate([d1_dict, d2_dict, d3_dict, d4_dict]):
        bl = [d_dict[0][t] for t in range(len(temp))]
        print(f"{idx+1}")
        for v_idx, v in enumerate(voltages):
            d_info = [d_dict[v_idx][t] for t in range(len(temp))]
            d_info = [d_info[i]/bl[i] for i in range(len(d_info))]
            d_mean = np.mean(d_info)
            d_std = np.std(d_info)
            print(f"Voltage: {v}")
            print(f"mean and std: {d_mean}±{d_std}")
        print("================")
    quit()
    fig, ax = plt.subplots(2, 2)
    d1_dict = np.array(d1_dict)
    d2_dict = np.array(d2_dict)
    d3_dict = np.array(d3_dict)
    d4_dict = np.array(d4_dict)
    dr_dict = np.array(dr_dict)
    d_list = [d1_dict, d2_dict, d3_dict, d4_dict]
    for x in range(2):
        for y in range(2):
            idx = x+(2*y)
            im = ax[x][y].imshow(d_list[idx], cmap='jet', vmin=1.0, vmax=15.0)
            fig.colorbar(im, ax=ax[x][y], shrink=0.9)
            ax[x][y].set_xticks(np.arange(len(temp)))
            ax[x][y].set_xticklabels(temp)
            ax[x][y].set_xlabel('Temperature (C)')
            ax[x][y].set_yticks(np.arange(len(voltages)))
            ax[x][y].set_yticklabels(voltages)
            ax[x][y].set_ylabel('VDD-Vdroop')
            ax[x][y].set_title(f'Num. of Buffer: {idx+1}')
    plt.suptitle('Norm. Delay Increase from Nomimal No Droop/20 Degree C')
    plt.show()
     
def plot_3D(info_dict, voltages, temp):
    from mpl_toolkits.mplot3d import Axes3D
    from scipy.interpolate import griddata
    # Create a figure and 3D axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Define the plane equation: ax + by + cz + d = 0
    x = []
    y = []
    z = []
    for v in voltages:
        for t in temp:
            key = f"{v}_{t}"
            driver_time = info_dict[driver][key]
            b1_time = info_dict[stage_one][key]
            slack_b1 = b1_time - driver_time
            x.append(v)
            y.append(y)
            z.append(slack_b1)
    print('here')
    grid_x = np.linspace(min(x), max(x), 50)
    print('x good')
    grid_y = np.linspace(min(y), max(y), 50)
    print('y good')
    grid_x, grid_y = np.meshgrid(grid_x, grid_y)
    print('mesh made')
    grid_z = griddata((x, y), z, (grid_x, grid_y), method="linear")
    print('z')
    surface = ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis', edgecolor='none')
    print('surface gen')
    cbar = fig.colorbar(surface, ax=ax, shrink=0.5, aspect=10)
    print('cbar')
    ax.plot_surface(X, Y, Z)
    print('plot')
    # Set labels and title
    ax.set_xlabel('VDD-Vdroop')
    ax.set_ylabel('Temperature (C)')
    ax.set_zlabel('slack (ps)')
    plt.title('Voltage/Temperature Delay Vis.')
    print('set up, now show')
    plt.show()
 
def needed_slack_reduction():
    FREQ = [1, 2, 3, 4, 5]
    slack_margin = [30, 20, 10, 5]
    z_p = []
    for f in FREQ:
        z_p_y = []
        for s in slack_margin:
            t_clk_ps = 1000 / f
            slack_ps = math.log10(s/100 * t_clk_ps)
            z_p_y.append(slack_ps)
        z_p_y = np.array(z_p_y)
        z_p.append(z_p_y)
    z_p = np.array(z_p)
    fig, ax = plt.subplots(1)
    im = ax.imshow(z_p, cmap='twilight')
    fig.colorbar(im, ax=ax, shrink=0.9)
    ax.set_yticks(np.arange(len(FREQ)))
    ax.set_yticklabels(FREQ)
    ax.set_ylabel('Core Frequency (GHz)')
    ax.set_xticks(np.arange(len(slack_margin)))
    ax.set_xticklabels(slack_margin)
    ax.set_xlabel('Slack Margin (%)')
    ax.set_title('log 10 of Raw Slack (ps)')
    plt.show()

def compare_equations(info_dict, voltages, temp):
    VDD = 1.0
    VTH = 0.125
    t = 20
    d1_list, d2_list, df_list = [], [], []
    d3_list, d4_list = [], []
    for v in voltages:
        inner_key = f"{v}_{t}"
        driver_time = info_dict[driver][inner_key]
        s1_time = info_dict[stage_one][inner_key]
        s2_time = info_dict[stage_two][inner_key]
        s3_time = info_dict[stage_three][inner_key]
        s4_time = info_dict[stage_four][inner_key]
        delta_1_buffer = s1_time - driver_time
        delta_2_buffer = s2_time - driver_time
        delta_3_buffer = s3_time - driver_time
        delta_4_buffer = s4_time - driver_time
        d1_list.append(1+delta_1_buffer/driver_time)
        d2_list.append(1+delta_2_buffer/driver_time)
        d3_list.append(1+delta_3_buffer/driver_time)
        d4_list.append(1+delta_4_buffer/driver_time)
        top = 1-(VTH/VDD)
        bottom = 1-(VTH/v)
        df = top / bottom
        df_list.append(df)
    plt.plot(voltages, d1_list, color='r', label='1 Buffer Delay')
    plt.plot(voltages, d2_list, color='b', label='2 Buffer Delay')
    plt.plot(voltages, d3_list, color='m', label='3 Buffer Delay')
    plt.plot(voltages, d4_list, color='k', label='4 Buffer Delay')
    plt.plot(voltages, df_list, color='g', label='SK Delay Factor')
    plt.xlabel('Voltages (VDD-Vdroop)')
    plt.ylabel('Normalized Delay @ Temperature 20 C')
    plt.legend(ncol=3, shadow=True, fancybox=True, loc='upper center', bbox_to_anchor=(0.5, 1.25))
    plt.show()

def main():
    df = pd.read_csv("sim_data_buffer_vt_sweep.csv")
    voltages = [1, 0.9, 0.8, 0.7]
    temp = [20, 40, 60, 80, 100, 120]
    info_dict = collect_timing_info(voltages, temp, df)
    #plot_3D(info_dict, voltages, temp)
    #compute_delays(info_dict, voltages, temp)
    compare_equations(info_dict, voltages, temp)
    #needed_slack_reduction()

if __name__=="__main__":
    main()
