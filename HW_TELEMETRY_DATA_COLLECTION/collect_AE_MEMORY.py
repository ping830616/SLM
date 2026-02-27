#Author | Eduardo Ortega
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob, os, statistics
from scipy.stats import entropy
from simpleL2Class import L2_CLASS as SCOUT
from matplotlib import colors as mcolors
from scipy.stats import skew
from autoencoderClass import autoencoder
AE = "AE"
STD = "STD"
dft = "dft"
dj = "dj"
dp = "dp"
gs = "gs"
gl = "gl"
ha = "ha"
ja = "ja"
mm = "mm"
oe = "oe"
ni = "ni"
pi = "pi"
sh = "sh"
tr = "tr"
workloads = [dft, dj, dp, gs, gl, ha, ja, mm, oe, ni, pi, sh, tr]
RH, SPECTRE, DROOP_DDR4, DROOP_DDR5 = "RH", "SPECTRE", "DROOP_4", "DROOP_5"
mark_style = {RH:"+",
            SPECTRE:"d",
            DROOP_DDR4:".",
            DROOP_DDR5:".",
            "DROOP":".",
            AE:"d",
            STD:"+"}
color = {dft:"rosybrown",
        dj:"firebrick",
        dp:"red",
        gs:"sienna",
        gl:"gold",
        ha:"darkkhaki",
        ja:"olivedrab",
        mm:"palegreen",
        oe:"darkgreen",
        ni:"mediumspringgreen",
        pi:"darkcyan",
        sh:"deepskyblue",
        tr:"slategray",
        AE:"red",
        STD:"blue",
        RH:"rosybrown",
        SPECTRE:"palegreen",
        DROOP_DDR4:"darkcyan",
        DROOP_DDR5:"darkcyan",
        "DROOP":"darkcyan"}
label_w = {dft:"DFT",
        dj:"DJ",
        dp:"DP",
        gs:"GS",
        gl:"GL",
        ha:"HA",
        ja:"JA",
        mm:"MM",
        oe:"OE",
        ni:"NI",
        pi:"PI",
        sh:"SH",
        tr:"TR"}

def split_into_ddr4_ddr5(file_paths):
    l1, l2 = [], []
    for f in file_paths:
        if "DDR4" in f: l1.append(f)
        else: l2.append(f)
    return l1, l2


def transform_hist_bins_to_pk(bin_counts):
    sum_hist = sum(bin_counts)
    return np.array([(count/sum_hist) for count in bin_counts])

def get_entropy(data, base_val=2):
    num_bins = 10**6
    bin_counts, bin_edges = np.histogram(data, bins=num_bins)
    pk = transform_hist_bins_to_pk(bin_counts)
    h = entropy(pk, base=base_val)
    return h

def value_ranking(df):
    key_value_list = []
    for idx, key in enumerate(df.keys()):
        if idx % 10 == 0: print(f"PROGRESS: {idx/len(df.keys())}")
        data = df[key].to_numpy()
        ### CURRENT VALUE - ENTROPY FI
        value = get_entropy(data, base_val=2)
        tuple_value = (key, value)
        key_value_list.append(tuple_value)
    key_value_list = sorted(key_value_list, key=lambda x: x[1], reverse=True)
    return key_value_list

def rank_values(file_path):
    df = pd.read_csv(file_path, index_col=False)
    print(f"file: {file_path}")
    workload = file_path.split('_')[-1].strip().split('.')[0].strip()
    print(f"workload key: {workload}")
    df = df.drop('Unnamed: 0', axis=1)
    tuple_list = value_ranking(df)
    feature_list = [x[0] for x in tuple_list]
    entropy_list = [x[1] for x in tuple_list]
    return workload, feature_list, f"{workload}_h", entropy_list


def rank():
    file_paths = glob.glob(f"{os.getcwd()}/TELEMETRY_DATA/DDR*_benign_*.csv")
    DDR4_LIST, DDR5_LIST = split_into_ddr4_ddr5(file_paths)
    ddr4_df, ddr5_df = pd.DataFrame(), pd.DataFrame()
    for x in range(0, len(DDR4_LIST)):
        ddr4_key, ddr4_labels, ddr4_key_v, ddr4_values  = rank_values(DDR4_LIST[x])
        ddr4_df[ddr4_key] = ddr4_labels
        ddr4_df[ddr4_key_v] = ddr4_values
        ddr5_key, ddr5_labels, ddr5_key_v, ddr5_values  = rank_values(DDR5_LIST[x])
        ddr5_df[ddr5_key] = ddr5_labels
        ddr5_df[ddr5_key_v] = ddr5_values
    ddr4_df.to_csv('DDR4_ENTROPY_FI.csv', index=False)
    ddr5_df.to_csv('DDR5_ENTROPY_FI.csv', index=False)


def grab_features(nf, workload, file_path):
    if "DDR4" in file_path: fi_rank = pd.read_csv(f"{os.getcwd()}/DDR4_ENTROPY_FI.csv")
    else: fi_rank = pd.read_csv(f"{os.getcwd()}/DDR5_ENTROPY_FI.csv")
    features = fi_rank[workload].tolist()
    subset_features = features[0:nf]
    return subset_features

def eval_rank_on_feat(num_features=10, rig="DDR4", SCOUT_TYPE=AE):
    if rig == "DDR4":
        file_paths_16 = glob.glob(f"{os.getcwd()}/TD_16/DDR4_benign_*.csv")
        file_paths_32 = glob.glob(f"{os.getcwd()}/TD_32/DDR4_benign_*.csv")
    else:
        file_paths_16 = glob.glob(f"{os.getcwd()}/TD_16/DDR5_benign_*.csv")
        file_paths_32 = glob.glob(f"{os.getcwd()}/TD_32/DDR5_benign_*.csv")
    cv_16, cv_32 = {}, {}
    for f in file_paths_16:
        df = pd.read_csv(f, index_col=False)
        workload = f.split("_")[-1].strip().split(".")[0].strip()
        features = grab_features(num_features, workload, f)
        x_train = df[features].to_numpy(dtype='float32')
        scout = SCOUT(x_train=x_train, l2=SCOUT_TYPE)
        scout = scout.fit()
        scout = scout.adjust_for_16_precision()
        s = scout.predict(x_train)
        mu_s, std_s = np.mean(s), np.std(s)
        cv_s = std_s / mu_s
        cv_16[workload] = cv_s
        print(cv_s)
    for f in file_paths_32:
        df = pd.read_csv(f, index_col=False)
        workload = f.split("_")[-1].strip().split(".")[0].strip()
        features = grab_features(num_features, workload, f)
        x_train = df[features].to_numpy(dtype='float32')
        scout = SCOUT(x_train=x_train, l2=SCOUT_TYPE)
        scout = scout.fit()
        s = scout.predict(x_train)
        mu_s, std_s = np.mean(s), np.std(s)
        cv_s = std_s / mu_s
        cv_32[workload] = cv_s
        print(cv_s)
    print(f"FINISHED THE JOB: {num_features} {rig} {SCOUT_TYPE}")
    return cv_16, cv_32

def automate_feature_analysis():
    # DDR4 181
    ddr4_nf = 181
    ratio = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    x_nf = [int(r*ddr4_nf) for r in ratio]
    fig, ax = plt.subplots(2, 4)
    print("DDR4")
    for col, sc_type in enumerate([AE, STD]):
        print(f"SCOUT TYPE: {sc_type}")
        cv_16_master, cv_32_master = {}, {}
        for nf in x_nf:
            print(f"NUM FEATURES: {nf}")
            cv_16, cv_32 = eval_rank_on_feat(num_features=nf, rig="DDR4", SCOUT_TYPE=sc_type)
            cv_16_master[nf] = cv_16
            cv_32_master[nf] = cv_32
        for w in workloads:
            y_cv_16 = [cv_16_master[x][w] for x in x_nf]
            y_cv_32 = [cv_32_master[x][w] for x in x_nf]
            lw = label_w[w]
            ax[0][2*col].plot(x_nf, y_cv_16, c=color[w], label=f"{lw}")
            ax[0][2*col+1].plot(x_nf, y_cv_32, c=color[w], label=f"{lw}")
        if col == 0:
            ax[0][2*col].set_title("16-bit L\u2081", fontweight='bold')
            ax[0][2*col+1].set_title("32-bit L\u2081", fontweight='bold')
            ax[0][2*col].set_ylabel("SETUP A\n Coefficient of Variation", fontweight='bold')
        else:
            ax[0][2*col].set_title("16-bit L\u2082", fontweight='bold')
            ax[0][2*col+1].set_title("32-bit L\u2082", fontweight='bold')
            ax[0][2*col].set_ylabel("Coefficient of Variation", fontweight='bold')
        ax[0][2*col].set_xlabel("Number of Features", fontweight='bold')
        ax[0][2*col+1].set_xlabel("Number of Features", fontweight='bold')
        ax[0][2*col+1].set_ylabel("Coefficient of Variation", fontweight='bold')
        ax[0][2*col].set_xscale('log', base=2)
        ax[0][2*col+1].set_xscale('log', base=2)
    ax[0][1].legend(loc='upper center', 
                fancybox=True, 
                shadow=True, 
                ncol=7, 
                bbox_to_anchor=(1.05, 1.6))
    # DDR5 460
    print("DDR5")
    ddr5_nf = 460
    x_nf = [int(r*ddr5_nf) for r in ratio]
    for col, sc_type in enumerate([AE, STD]):
        print(f"SCOUT TYPE: {sc_type}")
        cv_16_master, cv_32_master = {}, {}
        for nf in x_nf:
            print(f"NUM FEATURES: {nf}")
            cv_16, cv_32 = eval_rank_on_feat(num_features=nf, rig="DDR5", SCOUT_TYPE=sc_type)
            cv_16_master[nf] = cv_16
            cv_32_master[nf] = cv_32
        for w in workloads:
            y_cv_16 = [cv_16_master[x][w] for x in x_nf]
            y_cv_32 = [cv_32_master[x][w] for x in x_nf]
            lw = label_w[w]
            ax[1][2*col].plot(x_nf, y_cv_16, c=color[w], label=f"{lw}")
            ax[1][2*col+1].plot(x_nf, y_cv_32, c=color[w], label=f"{lw}")
        if col == 0:
            ax[1][2*col].set_title("16-bit L\u2081", fontweight='bold')
            ax[1][2*col+1].set_title("32-bit L\u2081", fontweight='bold')
            ax[1][2*col].set_ylabel("SETUP B\n Coefficient of Variation", fontweight='bold')
        else:
            ax[1][2*col].set_title("16-bit L\u2082", fontweight='bold')
            ax[1][2*col+1].set_title("32-bit L\u2082", fontweight='bold')
            ax[1][2*col].set_ylabel("Coefficient of Variation", fontweight='bold')
        ax[1][2*col].set_xlabel("Number of Features", fontweight='bold')
        ax[1][2*col+1].set_xlabel("Number of Features", fontweight='bold')
        ax[1][2*col+1].set_ylabel("Coefficient of Variation", fontweight='bold')
        ax[1][2*col].set_xscale('log', base=2)
        ax[1][2*col+1].set_xscale('log', base=2)
    plt.show()
    quit()


def AUCROC(score_nom, score_ano):
    num_nom, num_ano, AUCROC = len(score_nom), len(score_ano), 0
    score_nom_sorted = np.sort(score_nom)
    score_ano_sorted = np.sort(score_ano)
    for i in range(num_ano):
        exit = 0
        for j in range(num_nom):
            if score_nom_sorted[j] >= score_ano_sorted[i] and exit == 0:
                AUCROC += ((1/num_ano) * (j/num_nom))
                exit = 1
        if exit == 0:
            AUCROC += (1/num_ano)
    return AUCROC

def get_case_data_path_f(list_of_paths, wkld):
    for f in list_of_paths:
        if wkld in f: return f

def eval_mem_on_feat(num_features=10, rig="DDR4", DATA_TYPE=RH):
    benign_file_paths_16 = glob.glob(f"{os.getcwd()}/TD_16/{rig}_benign_*.csv")
    benign_file_paths_32 = glob.glob(f"{os.getcwd()}/TD_32/{rig}_benign_*.csv")
    case_file_paths_16 = glob.glob(f"{os.getcwd()}/TD_16/{rig}_{DATA_TYPE}_*.csv")
    case_file_paths_32 = glob.glob(f"{os.getcwd()}/TD_32/{rig}_{DATA_TYPE}_*.csv")
    mem_16, mem_32 = {}, {}
    print(f"AE {DATA_TYPE}")
    print("---------------------------")
    print(f"mem")
    print("Precision: 16")
    print("Workload: bytes")
    print("====================")
    for f in benign_file_paths_16:
        df_train = pd.read_csv(f, index_col=False)
        wkld = f.split("_")[-1].strip().split(".")[0].strip()
        features = grab_features(num_features, wkld, f)
        x_train = df_train[features].to_numpy(dtype='float16')
        df_test = pd.read_csv(get_case_data_path_f(case_file_paths_16, wkld), index_col=False)
        x_test = df_test[features].to_numpy(dtype='float16')
        ae = autoencoder(x_train)
        ae = ae.fit()
        memory = ae.get_memory_size()
        mem_16[wkld] = memory
        print(f"{wkld}: {memory}")
    print(f"AE")
    print("Precision: 32")
    print("Workload: bytes")
    print("====================")
    for f in benign_file_paths_32:
        df = pd.read_csv(f, index_col=False)
        wkld = f.split("_")[-1].strip().split(".")[0].strip()
        features = grab_features(num_features, wkld, f)
        x_train = df[features].to_numpy(dtype='float32')
        df_test = pd.read_csv(get_case_data_path_f(case_file_paths_32, wkld), index_col=False)
        x_test = df_test[features].to_numpy(dtype='float32')
        ae = autoencoder(x_train)        
        ae = ae.fit()
        memory = ae.get_memory_size()
        mem_32[wkld] = memory
        print(f"{wkld}: {memory}")
    print(f"FINISHED THE JOB: {num_features} {rig} AE")
    return mem_16, mem_32

def autoencoder_mem_feature_data_collection():
    ddr4_nf = 181
    ddr5_nf = 460
    ratio = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    df_save = pd.DataFrame()
    df_save["WORKLOADS"] = workloads
    for row, case in enumerate([RH, SPECTRE, DROOP_DDR4, DROOP_DDR5]):
        print(f"{case}")
        if case == RH or case == DROOP_DDR4:
            x_nf = [int(r*ddr4_nf) for r in ratio]
            rig = "DDR4"
        else:
            x_nf = [int(r*ddr5_nf) for r in ratio]
            rig = "DDR5"
        if case == DROOP_DDR4 or case == DROOP_DDR5:
            case = "DROOP"
        for nf in x_nf:
            print(f"NUM FEATURES: {nf}")
            mem_16, mem_32 = eval_mem_on_feat(num_features=nf, rig=rig, DATA_TYPE=case)
            mem_16 = [mem_16[w] for w in workloads]
            mem_32 = [mem_32[w] for w in workloads]
            df_save[f"{rig}_{case}_AE_{nf}_16"] = mem_16
            df_save[f"{rig}_{case}_AE_{nf}_32"] = mem_32
    df_save.to_csv(f'AUTOENCODER_MASTER_MEMORY.csv', index=False)

def autoencoder_AUC_feature_analysis():
    ddr4_nf = 181
    ddr5_nf = 460
    ratio = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    df = pd.read_csv(f"{os.getcwd()}/AUTOENCODER_MASTER_AUC_SCORES.csv", index_col=False)
    fig, ax = plt.subplots(4, 2)
    for row, case in enumerate([RH, SPECTRE, DROOP_DDR4, DROOP_DDR5]):
        print(f"row: {row}")
        print(f"{case}")
        if case == RH or case == DROOP_DDR4:
            x_nf = [int(r*ddr4_nf) for r in ratio]
            rig = "DDR4"
        else:
            x_nf = [int(r*ddr5_nf) for r in ratio]
            rig = "DDR5"
        if case == DROOP_DDR4 or case == DROOP_DDR5:
            case = "DROOP"
        AUC_16_master, AUC_32_master = {}, {}
        for idx, w in enumerate(workloads):
            AUC_16_master[w] = [df[f"{rig}_{case}_AE_{nf}_16"][idx] for nf in x_nf]
            AUC_32_master[w] = [df[f"{rig}_{case}_AE_{nf}_32"][idx] for nf in x_nf]
        for w in workloads:
            y_AUC_16 = AUC_16_master[w]
            y_AUC_32 = AUC_32_master[w] 
            lw = label_w[w]
            ax[row][0].plot(x_nf, y_AUC_16, c=color[w], label=f"{lw}")
            ax[row][1].plot(x_nf, y_AUC_32, c=color[w], label=f"{lw}")
        if row == 0:
            ax[row][0].set_title("16-bit Autoencoder", fontweight='bold')
            ax[row][1].set_title("32-bit Autoencoder", fontweight='bold')
        if row == 0:
            ax[row][0].set_ylabel("TRRespass\nAUC", fontweight='bold')
        elif row == 1:
            ax[row][0].set_ylabel("SPECTRE\nAUC", fontweight="bold")
        elif row == 2:
            ax[row][0].set_ylabel("V-Droop\n(SETUP A)\nAUC", fontweight="bold")
        elif row == 3:
            ax[row][0].set_ylabel("V-Droop\n(SETUP B)\nAUC", fontweight="bold")
        ax[row][1].set_ylabel("AUC", fontweight='bold')
        ax[row][0].set_xlabel("Number of Features", fontweight='bold')
        ax[row][1].set_xlabel("Number of Features", fontweight='bold')
        ax[row][0].set_xscale('log', base=2)
        ax[row][1].set_xscale('log', base=2)
        ax[row][0].set_ylim([0.0, 1.0])
        ax[row][1].set_ylim([0.0, 1.0])
    ax[0][0].legend(shadow=True,
                    fancybox=True,
                    ncol=7,
                    loc='upper center',
                    bbox_to_anchor=(1.05, 2.0))
    plt.show()

def autoencoder_AVE_AUC_feature_analysis():
    ddr4_nf = 181
    ddr5_nf = 460
    ratio = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    df = pd.read_csv(f"{os.getcwd()}/AUTOENCODER_MASTER_AUC_SCORES.csv", index_col=False)
    fig, ax = plt.subplots(1, 2)
    for row, case in enumerate([RH, SPECTRE, DROOP_DDR4, DROOP_DDR5]):
        print(f"row: {row}")
        print(f"{case}")
        if case == RH or case == DROOP_DDR4:
            x_nf = [int(r*ddr4_nf) for r in ratio]
            rig = "DDR4"
        else:
            x_nf = [int(r*ddr5_nf) for r in ratio]
            rig = "DDR5"
        if case == DROOP_DDR4 or case == DROOP_DDR5:
            case = "DROOP"
            situation = "V-DROOP"
        if case == SPECTRE: situation = SPECTRE
        if case == RH: situation = "TRRespass"
        AUC_16_master, AUC_32_master = {}, {}
        for nf in x_nf:
            auc_16_ave = np.average(df[f"{rig}_{case}_AE_{nf}_16"])
            auc_32_ave = np.average(df[f"{rig}_{case}_AE_{nf}_32"])
            AUC_16_master[nf] = auc_16_ave
            AUC_32_master[nf] = auc_32_ave
        y_auc_16 = [AUC_16_master[nf] for nf in x_nf]
        y_auc_32 = [AUC_32_master[nf] for nf in x_nf]
        r = 0 if rig == "DDR4" else 1
        c = color[case]
        m = mark_style[list(mark_style.keys())[0]]
        if r == 0:
            ax[r].set_title("SETUP A", fontweight="bold")
        else:
            ax[r].set_title("SETUP B", fontweight="bold")
        ax[r].plot(x_nf, y_auc_16, marker=m, color=c, linestyle='solid', label=f"{situation} 16-bit Autoencoder")
        ax[r].plot(x_nf, y_auc_32, marker=m, color=c, linestyle='dotted', label=f"{situation} 32-bit Autoencoder")
        ax[r].set_ylabel("Average AUC", fontweight="bold")
        ax[r].set_xscale("log", base=2)
        ax[r].set_xlabel("Number of Features", fontweight="bold")
    ax[0].legend(fancybox=True, shadow=True, ncol=2, loc='upper center', bbox_to_anchor=(0.5, 1.3))
    ax[1].legend(fancybox=True, shadow=True, ncol=2, loc='upper center', bbox_to_anchor=(0.5, 1.3))
    plt.show()

def main():
    autoencoder_mem_feature_data_collection()
    #autoencoder_AUC_feature_analysis()
    #autoencoder_AVE_AUC_feature_analysis()

if __name__=="__main__":
    main()


