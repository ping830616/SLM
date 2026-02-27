# Author | Eduardo Ortega
import pandas as pd
import matplotlib.pyplot as plt
df_HW = pd.read_csv('hw.csv')
SETUP_B_AREA = 215.25
IDLE, DFT, DJ, DP, GS, GL, HA, JA, MM, NI, OE, PI, SH, TR = 'IDLE', 'DFT', 'DJ', 'DP', 'GS', 'GL', 'HA', 'JA', 'MM', 'NI', 'OE', 'PI', 'SH', 'TR'
POWER = {IDLE:35.5, DFT:139.5, DJ:64.7, DP:99.3, GS:96.55, GL:69.1, HA:87.5, JA:89.8, MM:141.5, NI:97.5, OE:114.7, PI:96.8, SH:113.0, TR:94.9}

def get_add_area():
    value = df_HW['add'].to_list()[0]
    value /= (1000**2)
    return value

def get_add_pow(scale_GH=1.0):
    value = df_HW['add'].tolist()[1]
    value *= scale_GH
    return value

def get_mult_area():
    value = df_HW['mult'].to_list()[0]
    value /= (1000**2)
    return value

def get_mult_pow(scale_GH=1.0):
    value = df_HW['mult'].tolist()[1]
    value *= scale_GH
    return value

def find_num_features(thresh=0.85):
    val = {}
    for factor in ['COM', 'MEM', 'SEN']:
        df = pd.read_csv(f'../MICI/{factor}_DDR5_MICI_{thresh}.csv')
        features = df[f'MICI_{thresh}'].tolist()
        val[factor] = len(features)
    return val['COM'], val['MEM'], val['SEN']

def STD_area(nf):
    total_area = 0.0
    for f in range(int(nf)):
        mult_area = get_mult_area()
        mult_area *= 2
        add_area = get_add_area()
        total_area += (mult_area + add_area) # STD EUCLIDEAN ERROR PER FEATURE
    add_area = get_add_area()
    add_area *= (nf-1) # ADDER TREE
    total_area += add_area
    return total_area

def STD_power(nf, scale=1.0):
    total_power = 0.0
    for f in range(int(nf)):
        mult_power = get_mult_pow(scale_GH=scale)
        mult_power *= 2
        add_power = get_add_pow(scale_GH=scale)
        total_power += (mult_power + add_power) # STD EUCLIDEAN ERROR PER FEATURE
    add_power = get_add_pow(scale_GH=scale)
    add_power *= (nf-1) # ADDER TREE
    total_power += add_power
    return total_power

def AGG_area(nf):
    mult_area = get_mult_area()
    return 2 * mult_area

def AGG_power(nf, scale=1.0):
    mult_power = get_mult_pow(scale_GH=scale)
    return 2 * mult_power

def compute_power_from_features(num_features, GH=1.0, STD=True):
    power = STD_power(num_features, scale=GH) if STD else AGG_power(num_features, scale=GH)
    return power

def compute_area_from_features(nf, STD=True):
    area = STD_area(nf) if STD else AGG_area(nf)
    return area

def POWER_STUDY():
    comp_f, mem_f, sen_f = find_num_features(thresh=0.85)
    freq_list = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.5, 5.0]
    power_per_dict = {}
    power_mw_dict = {}
    for k in POWER.keys():
        power_per_dict[k] = []
        power_mw_dict[k] = []
    for freq in freq_list:
        comp = compute_power_from_features(comp_f, GH=freq)
        mem = compute_power_from_features(mem_f, GH=freq)
        sen = compute_power_from_features(sen_f, GH=freq)
        agg = compute_power_from_features(3, GH=freq, STD=False)
        total_power = comp + mem + sen + agg
        total_power /= 1000
        for k in power_mw_dict.keys():
            power_mw_dict[k].append(total_power)
            power_per_dict[k].append(100*(total_power/POWER[k]))
    for k in power_mw_dict.keys():
        plt.plot(freq_list, power_mw_dict[k], label=f'{k}')
    plt.yscale('log', base=10)
    plt.ylim((10**-1, 10**1))
    plt.xlim((min(freq_list), max(freq_list)))
    plt.legend(ncol=7, shadow=True, fancybox=True, loc='lower center', bbox_to_anchor=(0.5, -0.6))
    plt.xlabel('OCTANE Frequency (GHz)', fontsize=14) #fontweight='bold')
    plt.ylabel('OCTANE Power Consumption (W)', fontsize=14) #fontweight='bold')
    #plt.ylabel('SETUP B Increased\nPower Consumption (%)', fontweight='bold')
    plt.grid(True, which='both')
    plt.show()
    
def AREA():
    comp_f, mem_f, sen_f = find_num_features(thresh=0.85)
    comp = compute_area_from_features(comp_f)
    mem = compute_area_from_features(mem_f)
    sen = compute_area_from_features(sen_f)
    agg = compute_area_from_features(3, STD=False)
    area = comp + mem + sen + agg
    print(area)

def main():
    POWER_STUDY()

if __name__ == "__main__":
    main()
