# Author | Eduardo Ortega
import pandas as pd
import numpy as np
import os, glob
import matplotlib.pyplot as plt
path_to_csv = f"{os.getcwd()}/ITC24_SCOUT_results/7nm.csv"

prec_16 = '16'
prec_32 = '32'
prec = [prec_16, prec_32]
ae = 'ae'
std = 'std'
loss_op = [ae, std]
add = 'Adder'
mult = 'Mult'
op = [add, mult]
area_idx, sp_idx, dp_idx = 1, 2, 3

# NOTE area is in um^2, power is in mW
# setup area is in mm^2
area_A = 125
area_B = 215.25
idle_power_B = 35.5*(10**3) # milliwatts

def loss_operator_info(df, loss_type, precision, r=1.0):
    adder_prec = df[f"{add}{precision}"]
    add_sp, add_dp, adder_area = adder_prec[sp_idx], adder_prec[dp_idx], adder_prec[area_idx]
    add_dp *= r
    adder_p = add_sp + add_dp
    mult_prec = df[f"{mult}{precision}"]
    mult_sp, mult_dp, mult_area = mult_prec[sp_idx], mult_prec[dp_idx], mult_prec[area_idx]
    mult_dp *= r
    mult_p = mult_sp + mult_dp
    if loss_type == ae:
        power = adder_p + mult_p
        area = adder_area + mult_area
    else:
        power = adder_p + (2*mult_p)
        area = adder_area + (2*mult_area)
    return power, area

def adder_info(df, precision, r=1.0):
    adder_prec = df[f"{add}{precision}"]
    add_sp, add_dp, adder_area = adder_prec[sp_idx], adder_prec[dp_idx], adder_prec[area_idx]
    add_dp *= r
    adder_p = add_sp + add_dp
    return adder_p, adder_area

def get_power(df, loss_type, precision, nf, freq=900, per=False):
    ratio = freq / 900
    op_power, op_area = loss_operator_info(df, loss_type, precision, r=ratio)
    adder_power, adder_area = adder_info(df, precision, r=ratio)
    result = relationship(nf, op_power, adder_power)
    if per:
        result /= idle_power_B
        result *= 100
    return result

def get_area(df, loss_type, precision, nf):
    op_power, op_area = loss_operator_info(df, loss_type, precision)
    adder_power, adder_area = adder_info(df, precision)
    result = relationship(nf, op_area, adder_area)
    return result

def relationship(nf, operator, adder):
    result = (nf*operator) + ((nf-1)*adder)
    return result

def convert_to_mm(a):
    a = a * ((1/1000)**2)
    return a

def convert_da_per(area_list):
    new_area_list = []
    for area in area_list:
        data = [convert_to_mm(a) for a in area]
        per_data = [(100*(d/area_B)) for d in data]
        new_area_list.append(per_data)
    return new_area_list

def gen_area_graph(df, feature_range):
    area_16_ae = [get_area(df, ae, prec_16, f) for f in feature_range]
    area_16_std = [get_area(df, std, prec_16, f) for f in feature_range]
    area_32_ae = [get_area(df, ae, prec_32, f) for f in feature_range]
    area_32_std = [get_area(df, std, prec_32, f) for f in feature_range]
    area_list = [area_16_ae, area_16_std, area_32_ae, area_32_std]
    [da_16_ae, da_16_std, da_32_ae, da_32_std] = convert_da_per(area_list)
    fig, ax = plt.subplots(1, 2)
    ax[0].plot(feature_range, area_16_ae, label='16-bit L\u2081' , c='r', ls='solid')
    ax[0].plot(feature_range, area_16_std, label='16-bit L\u2082', c='r', ls='dashed')
    ax[0].plot(feature_range, area_32_ae, label='32-bit L\u2081', c='b', ls='solid')
    ax[0].plot(feature_range, area_32_std, label='32-bit L\u2082', c='b', ls='dashed')
    ax[0].set_yscale('log', base=10)
    ax[0].set_xlabel('Number of Features', fontweight='bold')
    ax[0].set_ylabel('Area (um\u00b2)', fontweight='bold')
    ax[1].plot(feature_range, da_16_ae, label='16-bit L\u2081' , c='r', ls='solid')
    ax[1].plot(feature_range, da_16_std, label='16-bit L\u2082', c='r', ls='dashed')
    ax[1].plot(feature_range, da_32_ae, label='32-bit L\u2081', c='b', ls='solid')
    ax[1].plot(feature_range, da_32_std, label='32-bit L\u2082', c='b', ls='dashed')
    ax[1].set_yscale('log', base=10)
    ax[1].set_xlabel('Number of Features', fontweight='bold')
    ax[1].set_ylabel('Additional Die Area %\n(Setup B)', fontweight='bold')
    ax[0].legend(loc='upper center', 
                bbox_to_anchor=(1.15, 1.2), 
                fancybox=True, 
                shadow=True, 
                ncol=4)
    plt.show()


def compute_z(feature_range, freq_range, scout_type, precision, df, type_power):
    z = []
    for nf in feature_range:
        z_y = []
        for f in freq_range:
            p = get_power(df, scout_type, precision, nf, freq=f, per=type_power)
            z_y.append(p)
        z.append(np.array(z_y))
    z = np.array(z)
    return z

def gen_power_plots(df):
    ratio = [0.2, 0.4, 0.6, 0.8, 1.0]
    feature_range = [int(r*460) for r in ratio]
    feature_range.reverse()
    freq_range = [int(r*900) for r in ratio]
    z_ae_16_mw = compute_z(feature_range, freq_range, ae, prec_16, df, False)
    z_ae_32_mw = compute_z(feature_range, freq_range, ae, prec_32, df, False)
    z_std_16_mw = compute_z(feature_range, freq_range, std, prec_16, df, False)
    z_std_32_mw = compute_z(feature_range, freq_range, std, prec_32, df, False)
    mw = [z_ae_16_mw, z_ae_32_mw, z_std_16_mw, z_std_32_mw]
    z_ae_16_per = compute_z(feature_range, freq_range, ae, prec_16, df, True)
    z_ae_32_per = compute_z(feature_range, freq_range, ae, prec_32, df, True)
    z_std_16_per = compute_z(feature_range, freq_range, std, prec_16, df, True)
    z_std_32_per = compute_z(feature_range, freq_range, std, prec_32, df, True)
    per = [z_ae_16_per, z_ae_32_per, z_std_16_per, z_std_32_per]
    ylabel = [("Power (mW)", "Number of Features"), ("Additional Idle Power (%)", "Number of Features")]
    xlabel = ["Frequency (MHz)", "Frequency (MHz)"]
    fig, ax = plt.subplots(2, 4)
    title_labels = ['16-bit L\u2081', '32-bit L\u2081', 
                    '16-bit L\u2082', '32-bit L\u2082']
    min_v = [20, 0.05]
    max_v = [700, 2.00]
    for row, label in enumerate(ylabel):
        z = mw if row == 0 else per
        mi = min_v[row]
        ma = max_v[row]
        for col in range(4):
            ax[row][col].set_xticks(np.arange(len(freq_range)))
            ax[row][col].set_xticklabels(freq_range)
            ax[row][col].set_yticks(np.arange(len(feature_range)))
            ax[row][col].set_yticklabels(feature_range)
            ax[row][col].set_xlabel(xlabel[row], fontweight='bold')
            if col != 0:
                ax[row][col].set_ylabel(label[1], fontweight='bold')
            else:
                ax[row][col].set_ylabel(f"{label[0]}\n{label[1]}", fontweight='bold')
            if row == 0:
                ax[row][col].set_title(f"{title_labels[col]}", fontweight='bold')
    
        im_ae_16 = ax[row][0].imshow(z[0], cmap='jet', vmin=mi, vmax=ma)
        im_ae_32 = ax[row][1].imshow(z[1], cmap='jet', vmin=mi, vmax=ma)
        im_std_16 = ax[row][2].imshow(z[2], cmap='jet', vmin=mi, vmax=ma)
        im_std_32 = ax[row][3].imshow(z[3], cmap='jet', vmin=mi, vmax=ma)
        fig.colorbar(im_ae_16, ax=ax[row][0], shrink=0.9)
        fig.colorbar(im_ae_32, ax=ax[row][1], shrink=0.9) 
        fig.colorbar(im_std_16, ax=ax[row][2], shrink=0.9) 
        fig.colorbar(im_std_32, ax=ax[row][3], shrink=0.9)
    plt.show()

def area():
    df = pd.read_csv(path_to_csv)
    feature_range = list(range(2, 460))
    gen_area_graph(df, feature_range)

def power():
    df = pd.read_csv(path_to_csv)
    gen_power_plots(df)

def compute_power_SCOUT(f=500):
    df = pd.read_csv(path_to_csv)
    p = get_power(df, std, prec_32, int(0.5*460), freq=f, per=False)
    per = get_power(df, std, prec_32, int(0.5*460), freq=f, per=True)
    return p, per

def bar_chart_power_workloads():
    path = f"{os.getcwd()}/power.csv"
    df = pd.read_csv(path, index_col=False)
    labels = df['Workload']
    power = df['POWER (WATTS)']
    power *= 1000
    power_scout = power + compute_power_SCOUT()[0]
    norm_power = power_scout / power
    x_range = list(range(0,len(norm_power)))
    print(labels, norm_power, x_range)
    fig, ax = plt.subplots()
    width=1.0
    p = ax.bar(labels, norm_power, width, tick_label=x_range, label=labels)
    ax.bar(p, label_type='center')
    plt.show()

def main():
    #area()
    #power()
    p, per = compute_power_SCOUT(f=900)
    print(p, per)
    
    #bar_chart_power_workloads()

if __name__=="__main__":
    main()
