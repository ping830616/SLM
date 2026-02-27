# Author | Eduardo Ortega
import glob
import pandas as pd
import os, math
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import KBinsDiscretizer, MinMaxScaler
from scipy.stats import entropy

def get_PAMPAR_data(memory="DDR4"):
    csv_list = glob.glob(f'../TELEMETRY_DATA/{memory}_benign_*.csv')
    return csv_list

def compute_entropy(df):
    value_counts = df.apply(lambda x: x.astype(str)).agg('-'.join, axis=1).value_counts(normalize=True)
    return entropy(value_counts)


def compute_JER(df_category, category_name):
    if df_category is None or df_category.empty:
        return [], []
    jer_values = {}
    # Compute full dataset entropy
    full_entropy = compute_entropy(df_category)
    for idx, feature in enumerate(df_category.columns):
        if 'TIME' in feature:
            continue  # Skip time-related columns
        if idx % 10 == 0: print(f"{category_name.upper()} - {100*(idx/len(df_category.columns)):.2f}% processed")
        reduced_df = df_category.drop(columns=[feature])
        reduced_entropy = compute_entropy(reduced_df)
        jer_values[feature] = abs(full_entropy - reduced_entropy)
    jer_rank = sorted(jer_values.items(), key=lambda x: x[1], reverse=True)
    if jer_rank:
        jer_feature, jer_value = zip(*jer_rank)
        return list(jer_feature), list(jer_value)
    return [], []

def ranking_JER_breakdown(list_csv_data, mem='DDR4'):
    df_JER_compute = pd.DataFrame()
    df_JER_memory = pd.DataFrame()
    df_JER_sensor = pd.DataFrame()
    for csv in list_csv_data:
        print(f"Computing for: {csv}")
        workload = csv.split('_')[-1].strip().split('.csv')[0]
        df = pd.read_csv(csv)
        f_memory, f_sensor, f_compute = [], [], []
        del df['Unnamed: 0']
        for key in df.keys():
            if 'L2' in key or 'L3' in key or 'READ' in key or 'WRITE' in key: 
                f_memory.append(key)
            elif 'Joules' in key or 'TEMP' in key or 'Voltage' in key:
                f_sensor.append(key)
            else:
                f_compute.append(key)
        df_compute = df[f_compute]
        df_memory = df[f_memory]
        df_sensor = df[f_sensor]
        compute_feature, compute_value = compute_JER(df_compute, 'compute')
        memory_feature, memory_value = compute_JER(df_memory, 'memory')
        sensor_feature, sensor_value = compute_JER(df_sensor, 'sensor')
        if compute_feature:
            df_JER_compute[f'{workload}_feature_compute'] = compute_feature
            df_JER_compute[f'{workload}_value_compute'] = compute_value
        if memory_feature:
            df_JER_memory[f'{workload}_feature_memory'] = memory_feature
            df_JER_memory[f'{workload}_value_memory'] = memory_value
        if sensor_feature:
            df_JER_sensor[f'{workload}_feature_sensor'] = sensor_feature
            df_JER_sensor[f'{workload}_value_sensor'] = sensor_value
    df_JER_compute.to_csv(f'JER_{mem}_compute.csv', index=False)
    df_JER_memory.to_csv(f'JER_{mem}_memory.csv', index=False)
    df_JER_sensor.to_csv(f'JER_{mem}_sensor.csv', index=False)

def ranking_JER(list_csv_data, mem='DDR4'):
    df_JER = pd.DataFrame()
    for csv in list_csv_data:
        print(f"Computing for: {csv}")
        workload = csv.split('_')[-1].strip().split('.csv')[0]
        df = pd.read_csv(csv)
        del df['Unnamed: 0']
        full_entropy = compute_entropy(df)
        jer_values = {}
        for idx, k in enumerate(list(df.keys())):
            if 'TIME' in k: 
                pass
            else:
                if idx % 10 == 0: print(f"{100*(idx/df.shape[1])}%")
                reduced_df = df.drop(columns=[k])
                reduced_entropy = compute_entropy(reduced_df)
                jer_values[k] = abs(full_entropy - reduced_entropy)
        jer_rank = sorted(jer_values.items(), reverse=True, key=lambda x: x[1])
        jer_feature, jer_value = zip(*jer_rank)
        jer_feature, jer_value = list(jer_feature), list(jer_value)
        df_JER[f'{workload}_feature'] = jer_feature
        df_JER[f'{workload}_value'] = jer_value
    df_JER.to_csv(f'JER_{mem}.csv', index=False)

def ranking_MICI_breakdown(list_csv_data, mem='DDR4'):
    df_MICI_compute = pd.DataFrame()
    df_MICI_memory = pd.DataFrame()
    df_MICI_sensor = pd.DataFrame()
    for csv in list_csv_data:
        print(f"Computing for: {csv}")
        workload = csv.split('_')[-1].strip().split('.csv')[0]
        df = pd.read_csv(csv)
        f_memory, f_sensor, f_compute = [], [], []
        del df['Unnamed: 0']
        for key in df.keys():
            if 'L2' in key or 'L3' in key or 'READ' in key or 'WRITE' in key: 
                f_memory.append(key)
            elif 'Joules' in key or 'TEMP' in key or 'Voltage' in key:
                f_sensor.append(key)
            else:
                f_compute.append(key)
        df_compute = df[f_compute]
        df_memory = df[f_memory]
        df_sensor = df[f_sensor]
        for name, df in [('compute', df_compute), ('memory', df_memory), ('sensor', df_sensor)]:
            mici_values = {}
            n_bins = int(math.ceil(math.log2(df.shape[0]+1)))
            for idx, k in enumerate(list(df.keys())):
                if 'TIME' in k: 
                    pass
                else:
                    if idx % 10 == 0: print(f"{100*(idx/df.shape[1])}%")
                    x = df[k].values.reshape(-1,1)
                    discretizer = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy='quantile')
                    x_d = discretizer.fit_transform(x).flatten()
                    H_x = entropy(np.histogram(x, bins=n_bins)[0])
                    I_x_xd = mutual_info_classif(x, x_d, discrete_features=True)[0]
                    mici_values[k] = I_x_xd / H_x if H_x > 0 else 0
            mici_rank = [(key, val) for key, val in mici_values.items()]
            mici_rank = sorted(mici_rank, reverse=True, key=lambda x: x[1])
            mici_feature, mici_value = zip(*mici_rank)
            mici_feature, mici_value = list(mici_feature), list(mici_value)
            if 'compute' in name:
                df_MICI_compute[f'{workload}_feature_{name}'] = mici_feature
                df_MICI_compute[f'{workload}_value_{name}'] = mici_value
            elif 'memory' in name:
                df_MICI_memory[f'{workload}_feature_{name}'] = mici_feature
                df_MICI_memory[f'{workload}_value_{name}'] = mici_value
            else:
                df_MICI_sensor[f'{workload}_feature_{name}'] = mici_feature
                df_MICI_sensor[f'{workload}_value_{name}'] = mici_value
    df_MICI_compute.to_csv(f'MICI_{mem}_compute.csv', index=False)
    df_MICI_memory.to_csv(f'MICI_{mem}_memory.csv', index=False)
    df_MICI_sensor.to_csv(f'MICI_{mem}_sensor.csv', index=False)

def ranking_MICI(list_csv_data, mem='DDR4'):
    df_MICI = pd.DataFrame()
    for csv in list_csv_data:
        print(f"Computing for: {csv}")
        workload = csv.split('_')[-1].strip().split('.csv')[0]
        df = pd.read_csv(csv)
        del df['Unnamed: 0']
        mici_values = {}
        n_bins = int(math.ceil(math.log2(df.shape[0]+1)))
        for idx, k in enumerate(list(df.keys())):
            if 'TIME' in k: 
                pass
            else:
                if idx % 10 == 0: print(f"{100*(idx/df.shape[1])}%")
                x = df[k].values.reshape(-1,1)
                discretizer = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy='quantile')
                x_d = discretizer.fit_transform(x).flatten()
                H_x = entropy(np.histogram(x, bins=n_bins)[0])
                I_x_xd = mutual_info_classif(x, x_d, discrete_features=True)[0]
                mici_values[k] = I_x_xd / H_x if H_x > 0 else 0
        mici_rank = [(key, val) for key, val in mici_values.items()]
        mici_rank = sorted(mici_rank, reverse=True, key=lambda x: x[1])
        mici_feature, mici_value = zip(*mici_rank)
        mici_feature, mici_value = list(mici_feature), list(mici_value)
        df_MICI[f'{workload}_feature'] = mici_feature
        df_MICI[f'{workload}_value'] = mici_value
    df_MICI.to_csv(f'MICI_{mem}.csv', index=False)

def ranking_variance(list_csv_data, mem='DDR4'):
    df_MICI = pd.DataFrame()
    for csv in list_csv_data:
        print(f"Computing for: {csv}")
        workload = csv.split('_')[-1].strip().split('.csv')[0]
        df = pd.read_csv(csv)
        del df['Unnamed: 0']
        mici_values = {}
        n_bins = int(math.ceil(math.log2(df.shape[0]+1)))
        for idx, k in enumerate(list(df.keys())):
            if 'TIME' in k: 
                pass
            else:
                if idx % 10 == 0: print(f"{100*(idx/df.shape[1])}%")
                x = df[k].values.reshape(-1,1)
                scaler = MinMaxScaler()
                norm = scaler.fit_transform(x)
                mici_values[k] = np.var(norm)
        mici_rank = [(key, val) for key, val in mici_values.items()]
        mici_rank = sorted(mici_rank, reverse=True, key=lambda x: x[1])
        mici_feature, mici_value = zip(*mici_rank)
        mici_feature, mici_value = list(mici_feature), list(mici_value)
        df_MICI[f'{workload}_feature'] = mici_feature
        df_MICI[f'{workload}_value'] = mici_value
    df_MICI.to_csv(f'variance_{mem}.csv', index=False)

def ranking_variance_breakdown(list_csv_data, mem='DDR4'):
    df_MICI_compute = pd.DataFrame()
    df_MICI_memory = pd.DataFrame()
    df_MICI_sensor = pd.DataFrame()
    for csv in list_csv_data:
        print(f"Computing for: {csv}")
        workload = csv.split('_')[-1].strip().split('.csv')[0]
        df = pd.read_csv(csv)
        f_memory, f_sensor, f_compute = [], [], []
        del df['Unnamed: 0']
        for key in df.keys():
            if 'L2' in key or 'L3' in key or 'READ' in key or 'WRITE' in key: 
                f_memory.append(key)
            elif 'Joules' in key or 'TEMP' in key or 'Voltage' in key:
                f_sensor.append(key)
            else:
                f_compute.append(key)
        df_compute = df[f_compute]
        df_memory = df[f_memory]
        df_sensor = df[f_sensor]
        for name, df in [('compute', df_compute), ('memory', df_memory), ('sensor', df_sensor)]:
            mici_values = {}
            n_bins = int(math.ceil(math.log2(df.shape[0]+1)))
            for idx, k in enumerate(list(df.keys())):
                if 'TIME' in k: 
                    pass
                else:
                    if idx % 10 == 0: print(f"{100*(idx/df.shape[1])}%")
                    x = df[k].values.reshape(-1,1)
                    scaler = MinMaxScaler()
                    norm = scaler.fit_transform(x)
                    mici_values[k] = np.var(norm)
            mici_rank = [(key, val) for key, val in mici_values.items()]
            mici_rank = sorted(mici_rank, reverse=True, key=lambda x: x[1])
            mici_feature, mici_value = zip(*mici_rank)
            mici_feature, mici_value = list(mici_feature), list(mici_value)
            if 'compute' in name:
                df_MICI_compute[f'{workload}_feature_{name}'] = mici_feature
                df_MICI_compute[f'{workload}_value_{name}'] = mici_value
            elif 'memory' in name:
                df_MICI_memory[f'{workload}_feature_{name}'] = mici_feature
                df_MICI_memory[f'{workload}_value_{name}'] = mici_value
            else:
                df_MICI_sensor[f'{workload}_feature_{name}'] = mici_feature
                df_MICI_sensor[f'{workload}_value_{name}'] = mici_value
    df_MICI_compute.to_csv(f'variance_{mem}_compute.csv', index=False)
    df_MICI_memory.to_csv(f'variance_{mem}_memory.csv', index=False)
    df_MICI_sensor.to_csv(f'variance_{mem}_sensor.csv', index=False)

def create_MICI(memory='DDR4'):
    list_csv_data = get_PAMPAR_data(memory=memory)
    ranking_MICI(list_csv_data, mem=memory)
    ranking_MICI_breakdown(list_csv_data, mem=memory)

def create_JER(memory='DDR4'):
    list_csv_data = get_PAMPAR_data(memory=memory)
    ranking_JER(list_csv_data, mem=memory)
    ranking_JER_breakdown(list_csv_data, mem=memory)

def create_variance(memory='DDR4'):
    list_csv_data = get_PAMPAR_data(memory=memory)
    ranking_variance(list_csv_data, mem=memory)
    ranking_variance_breakdown(list_csv_data, mem=memory)

def vis(memory='DDR4', method="variance"):
    df_main = pd.read_csv(f'{method}_{memory}.csv')
    df_com = pd.read_csv(f'{method}_{memory}_compute.csv')
    df_mem = pd.read_csv(f'{method}_{memory}_memory.csv')
    df_sen = pd.read_csv(f'{method}_{memory}_sensor.csv')
    key_names = [k for k in df_main.keys() if 'feature' in k]
    df_main = df_main[key_names]
    key_names = [k for k in df_com.keys() if 'feature' in k]
    df_com = df_com[key_names]
    key_names = [k for k in df_mem.keys() if 'feature' in k]
    df_mem = df_mem[key_names]
    key_names = [k for k in df_sen.keys() if 'feature' in k]
    df_sen = df_sen[key_names]
    shared_p_main = []
    shared_p_com, shared_p_mem, shared_p_sen = [], [], []
    top_per = np.linspace(0.1, 1.0, 100)
    for p in top_per:
        for shared_p, df in [(shared_p_main, df_main), (shared_p_com, df_com), (shared_p_mem, df_mem), (shared_p_sen, df_sen)]:
            top_n = int(len(df)*p)
            feature_sets = [set(df[col].iloc[:top_n]) for col in df.columns]
            shared_strings = set.intersection(*feature_sets)
            shared_percentage = (len(shared_strings) / top_n) * 100
            shared_p.append(shared_percentage)
    top_per = [100*p for p in top_per]
    for shared_p, name in [(shared_p_main, 'ALL'), (shared_p_com, 'COMPUTE'), (shared_p_mem, 'MEMORY'), (shared_p_sen, 'SENSORS')]:
        plt.plot(top_per, shared_p, label=name)
    plt.xlabel(f'Top % of Features ({method} Ranking)', fontweight='bold')
    plt.ylabel('Shared % of Features\nacross PAMPAR', fontweight='bold')
    plt.legend(shadow=True, fancybox=True)
    plt.show()

def extract_feature_columns(df, suffix_bool=False, suffix=None):
    workloads = set(col.split('_')[0] for col in df.columns if '_feature' in col)
    if not suffix_bool:
        return {workload: (df[f"{workload}_feature"], df[f"{workload}_value"]) for workload in workloads}
    else:
        return {workload: (df[f"{workload}_feature_{suffix}"], df[f"{workload}_value_{suffix}"]) for workload in workloads}

def compute_shared_features(workloads, threshold):
    feature_sets = [
        set(features[values >= threshold])  # Filter based on threshold
        for features, values in workloads.values()
    ]
    if feature_sets:
        shared_features = set.intersection(*feature_sets)
        return len(shared_features), list(shared_features)
    return 0, []

def threshold(memory='DDR4', method="MICI", path="STURGE_NBINS"):
    df_main = pd.read_csv(f'{path}/{method}_{memory}.csv')
    df_com = pd.read_csv(f'{path}/{method}_{memory}_compute.csv')
    df_mem = pd.read_csv(f'{path}/{method}_{memory}_memory.csv')
    df_sen = pd.read_csv(f'{path}/{method}_{memory}_sensor.csv')
    workloads_main = extract_feature_columns(df_main)
    workloads_com = extract_feature_columns(df_com, suffix_bool=True, suffix='compute')
    workloads_mem = extract_feature_columns(df_mem, suffix_bool=True, suffix='memory')
    workloads_sen = extract_feature_columns(df_sen, suffix_bool=True, suffix='sensor')
    value_thresholds = [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2]
    shared_p_main, shared_p_com, shared_p_mem, shared_p_sen = [], [], [], []
    sys_type = 'SETUP B' if memory == 'DDR5' else 'SETUP A'
    for threshold in value_thresholds:
        num_shared_features, shared_features = compute_shared_features(workloads_main, threshold)
        shared_p_main.append(num_shared_features)
        df = pd.DataFrame()
        df[f"{method}_{threshold}"] = shared_features
        df.to_csv(f'ALL_{memory}_{method}_{threshold}.csv', index=False)
        num_shared_features, shared_features = compute_shared_features(workloads_com, threshold)
        shared_p_com.append(num_shared_features)
        df = pd.DataFrame()
        df[f"{method}_{threshold}"] = shared_features
        df.to_csv(f'COM_{memory}_{method}_{threshold}.csv', index=False)
        num_shared_features, shared_features = compute_shared_features(workloads_mem, threshold)
        shared_p_mem.append(num_shared_features)
        df = pd.DataFrame()
        df[f"{method}_{threshold}"] = shared_features
        df.to_csv(f'MEM_{memory}_{method}_{threshold}.csv', index=False)
        num_shared_features, shared_features = compute_shared_features(workloads_sen, threshold)
        shared_p_sen.append(num_shared_features)
        df = pd.DataFrame()
        df[f"{method}_{threshold}"] = shared_features
        df.to_csv(f'SEN_{memory}_{method}_{threshold}.csv', index=False)
    for shared_p, name in [
        (shared_p_com, 'COMPUTE'),
        (shared_p_mem, 'MEMORY'),
        (shared_p_sen, 'SENSORS')
    ]:
        plt.plot(value_thresholds, shared_p, label=name)

    plt.xlabel(f'Feature Value Threshold ({method} Ranking)', fontweight='bold')
    plt.ylabel(f'Number of Shared Features\nAcross Workloads ({sys_type})', fontweight='bold')
    plt.legend(shadow=True, fancybox=True, ncol=3, loc='upper center', bbox_to_anchor=(0.5, 1.2))
    plt.show()

def main():
    #create_MICI()
    #create_JER(memory='DDR5')
    #vis()
    threshold(memory='DDR4', method="MICI", path="STURGE_NBINS")

if __name__=="__main__":
    main()
