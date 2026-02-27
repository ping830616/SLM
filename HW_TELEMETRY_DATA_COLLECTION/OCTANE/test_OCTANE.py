# Author | Eduardo Ortega
datasets = ['dft', 'dj', 'dp', 'gl', 'gs', 'ha', 'ja', 'mm', 'ni', 'oe', 'pi', 'sh', 'tr']
#datasets = datasets[0:3]
systems = ['DDR4', 'DDR5']
security = {'DDR4':'RH', 'DDR5':'SPECTRE'}
safety = ['DROOP']
MICI_PATH = 'MICI'
rank_thresh = {MICI_PATH: [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2]}
import os, glob
import pandas as pd
from scipy.stats import rankdata
from distanceClass import DISTANCE_CLASS as dist
import distanceClass as dc
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import numpy as np

def filter_df(df, rank, system, thresh):
    com_features = glob.glob(f'{os.getcwd()}/{rank}/COM_{system}_{rank}_{thresh}.csv')
    mem_features = glob.glob(f'{os.getcwd()}/{rank}/MEM_{system}_{rank}_{thresh}.csv')
    sen_features = glob.glob(f'{os.getcwd()}/{rank}/SEN_{system}_{rank}_{thresh}.csv')
    df_com = pd.read_csv(com_features[0])
    df_mem = pd.read_csv(mem_features[0])
    df_sen = pd.read_csv(sen_features[0])
    df_com = df[df_com[df_com.columns[0]]]
    df_mem = df[df_mem[df_mem.columns[0]]]
    df_sen = df[df_sen[df_sen.columns[0]]]
    return df_com.to_numpy(), df_mem.to_numpy(), df_sen.to_numpy()

def pairwise_sq_dist(d):
    G = d @ d.T
    s = np.sum(d*d, axis=1, keepdims=True)
    D2 = s + s.T - 2*G
    return D2

def similarity_TD_per_sys():
    for alpha in [0.02, 0.03, 0.04, 0.05]:
        os.system(f'echo "Platform,WA,WB,CKA" >> COMP_{alpha}.csv')
        for idx, sys in enumerate(systems):
            print(sys)
            for data in datasets:
                df_A = pd.read_csv(f'../TELEMETRY_DATA/{sys}_benign_{data}.csv')
                A = df_A.to_numpy()
                A = A.astype(np.float64, copy=True)
                A -= A.mean(axis=0, keepdims=True)
                D2A = pairwise_sq_dist(A)
                for d in datasets:
                    print(data, d, alpha)
                    df_B = pd.read_csv(f'../TELEMETRY_DATA/{sys}_benign_{d}.csv')
                    B = df_B.to_numpy()
                    B = B.astype(np.float64, copy=True)
                    B -= B.mean(axis=0, keepdims=True)
                    P = np.vstack([A, B])
                    D2P = pairwise_sq_dist(P)
                    iu = np.triu_indices(D2P.shape[0],1)
                    d_med = np.sqrt(np.median(D2P[iu]))
                    b = alpha * d_med
                    D2B = pairwise_sq_dist(B)
                    # RBF KERNELS
                    K_A = np.exp(-D2A / (2*b*b))
                    K_B = np.exp(-D2B / (2*b*b))
                    n = K_A.shape[0]
                    H = np.eye(n) - np.ones((n,n))/n
                    K_A = H @ K_A @ H
                    K_B = H @ K_B @ H
                    num = np.sum(K_A*K_B)
                    den = np.linalg.norm(K_A, 'fro')*np.linalg.norm(K_B, 'fro')
                    CKA = num / den
                    print(CKA)
                    os.system(f'echo "{sys},{data},{d},{CKA}" >> COMP_{alpha}.csv')

def similarity_TD_cross_sys():
    for alpha in [0.03, 0.04, 0.05]:
        for data in datasets:
            df_A = pd.read_csv(f'../TELEMETRY_DATA/DDR4_benign_{data}.csv')
            A = df_A.to_numpy()
            A = A.astype(np.float64, copy=True)
            A -= A.mean(axis=0, keepdims=True)
            D2A = pairwise_sq_dist(A)
            for d in datasets:
                print(data, d)
                df_B = pd.read_csv(f'../TELEMETRY_DATA/DDR5_benign_{d}.csv')
                B = df_B.to_numpy()
                B = B.astype(np.float64, copy=True)
                B -= B.mean(axis=0, keepdims=True)
                D2A = pairwise_sq_dist(A)
                iu = np.triu_indices(D2A.shape[0],1)
                d_med = np.sqrt(np.median(D2A[iu]))
                a_bandwidth = alpha * d_med
                D2B = pairwise_sq_dist(B)
                iu = np.triu_indices(D2B.shape[0],1)
                d_med = np.sqrt(np.median(D2B[iu]))
                b_bandwidth = alpha * d_med
                # RBF KERNELS
                K_A = np.exp(-D2A / (2*a_bandwidth*a_bandwidth))
                K_B = np.exp(-D2B / (2*b_bandwidth*b_bandwidth))
                n = K_A.shape[0]
                H = np.eye(n) - np.ones((n,n))/n
                K_A = H @ K_A @ H
                K_B = H @ K_B @ H
                num = np.sum(K_A*K_B)
                den = np.linalg.norm(K_A, 'fro')*np.linalg.norm(K_B, 'fro')
                CKA = num / den
                print(CKA)
                os.system(f'echo "{data},{d},{CKA}" >> CROSS_{alpha}.csv')

def automate_perf(): 
    RANK = MICI_PATH
    for sys in systems:
        for data in datasets:
            for AGG_type in dc.supp_AGG:
                for DIST_type in dc.supp_DIST:
                    df_SCORES = pd.DataFrame()
                    print(sys, DIST_type, AGG_type, data)
                    df_train = pd.read_csv(f'../TELEMETRY_DATA/{sys}_benign_{data}.csv')
                    df_security = pd.read_csv(f'../TELEMETRY_DATA/{sys}_{security[sys]}_{data}.csv')
                    df_safety = pd.read_csv(f'../TELEMETRY_DATA/{sys}_DROOP_{data}.csv')
                    for thresh in rank_thresh[RANK]:
                        print(thresh)
                        train_com, train_mem, train_sen = filter_df(df_train, RANK, sys, thresh)
                        secur_com, secur_mem, secur_sen = filter_df(df_security, RANK, sys, thresh)
                        safet_com, safet_mem, safet_sen = filter_df(df_safety, RANK, sys, thresh)
                        model = dist(train_compute=train_com, train_memory=train_mem, train_sensor=train_sen, DIST=DIST_type, AGG=AGG_type)
                        model = model.fit(train_com, train_mem, train_sen)
                        nom_agg, nom_compute, nom_memory, nom_sensor = model.predict(train_com, train_mem, train_sen)
                        sec_agg, sec_compute, sec_memory, sec_sensor = model.predict(secur_com, secur_mem, secur_sen)
                        saf_agg, saf_compute, saf_memory, saf_sensor = model.predict(safet_com, safet_mem, safet_sen)
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_nom_agg'] = nom_agg
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_nom_compute'] = nom_compute
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_nom_memory'] = nom_memory
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_nom_sensor'] = nom_sensor
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_sec_agg'] = sec_agg
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_sec_compute'] = sec_compute
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_sec_memory'] = sec_memory
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_sec_sensor'] = sec_sensor
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_saf_agg'] = saf_agg
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_saf_compute'] = saf_compute
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_saf_memory'] = saf_memory
                        df_SCORES[f'{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_saf_sensor'] = saf_sensor
                    df_SCORES.to_csv(f'{sys}_{data}_{DIST_type}_{AGG_type}_{RANK}.csv', index=False)

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

def perf_analysis(RANK=MICI_PATH):
    fig, ax = plt.subplots(1, 4)
    df_AUC = pd.DataFrame()
    for idx, sys in enumerate(systems):
        for DIST_type in dc.supp_DIST:
            for AGG_type in dc.supp_AGG:
                print(sys, DIST_type, AGG_type)
                if DIST_type == dc.STD:
                    c = 'r' if AGG_type == dc.MEAN else 'y'
                elif DIST_type == dc.COSINE:
                    c = 'b' if AGG_type == dc.MEAN else 'g'
                perf_max_sec, perf_min_sec, perf_q1_sec, perf_q3_sec, perf_m_sec = [], [], [], [], []
                perf_max_saf, perf_min_saf, perf_q1_saf, perf_q3_saf, perf_m_saf = [], [], [], [], []
                for thresh in rank_thresh[RANK]:
                    AUC_sec_dist, AUC_saf_dist = [], []
                    for data in datasets:
                        df = pd.read_csv(f'{RANK}_PERF_DEC/{sys}_{data}_{DIST_type}_{AGG_type}_{RANK}.csv')
                        print(f'DATA: {data}\tTHRESH: {thresh}')
                        norm_key = f"{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_nom_agg"
                        ano_sec_key = f"{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_sec_agg"
                        ano_saf_key = f"{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_saf_agg"
                        norm_score = df[norm_key].tolist()
                        ano_security_score = df[ano_sec_key].tolist()
                        ano_safety_score = df[ano_saf_key].tolist()
                        AUC_sec = AUCROC(norm_score, ano_security_score)
                        AUC_saf = AUCROC(norm_score, ano_safety_score)
                        df_AUC[f'{sys}_{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_sec'] = [AUC_sec]
                        df_AUC[f'{sys}_{data}_{DIST_type}_{AGG_type}_{RANK}_{thresh}_saf'] = [AUC_saf]
                        AUC_sec_dist.append(AUC_sec)
                        AUC_saf_dist.append(AUC_saf)
                    perf_max_sec.append(max(AUC_sec_dist))
                    perf_min_sec.append(min(AUC_sec_dist))
                    perf_q1_sec.append(np.percentile(AUC_sec_dist, 25))
                    perf_q3_sec.append(np.percentile(AUC_sec_dist, 75))
                    perf_m_sec.append(np.median(AUC_sec_dist))
                    perf_max_saf.append(max(AUC_saf_dist))
                    perf_min_saf.append(min(AUC_saf_dist))
                    perf_q1_saf.append(np.percentile(AUC_saf_dist, 25))
                    perf_q3_saf.append(np.percentile(AUC_saf_dist, 75))
                    perf_m_saf.append(np.median(AUC_saf_dist))
                ax[2*idx].plot(rank_thresh[RANK], perf_m_sec, color=c)
                ax[2*idx].fill_between(rank_thresh[RANK], perf_q1_sec, perf_q3_sec, color=c, alpha=0.3)
                ax[2*idx].fill_between(rank_thresh[RANK], perf_min_sec, perf_max_sec, color=c, alpha=0.1)
                ax[2*idx].set_xlabel('MICI Lower Bound Threshold', fontweight='bold')
                ax[2*idx].set_ylabel('AUCROC', fontweight='bold')
                ax[2*idx+1].plot(rank_thresh[RANK], perf_m_saf, color=c)
                ax[2*idx+1].fill_between(rank_thresh[RANK], perf_q1_saf, perf_q3_saf, color=c, alpha=0.3)
                ax[2*idx+1].fill_between(rank_thresh[RANK], perf_min_saf, perf_max_saf, color=c, alpha=0.1)
                ax[2*idx+1].set_xlabel('MICI Lower Bound Threshold', fontweight='bold')
                ax[2*idx+1].set_ylabel('AUCROC', fontweight='bold')
    df_AUC.to_csv('AUC_SCORES.csv', index=False)
    plt.show()


def color_dist_agg(DIST_type, AGG_type):
    if DIST_type == dc.STD:
        c = 'r' if AGG_type == dc.MEAN else 'y'
    elif DIST_type == dc.COSINE:
        c = 'b' if AGG_type == dc.MEAN else 'g'
    return c

def AUC_graph(RANK=MICI_PATH):
    df = pd.read_csv(f'{RANK}_PERF_DEC/AUC_SCORES.csv')
    keys = list(df.keys())
    # DDR4_dft_STD_MEAN_MICI_0.01_sec
    sys = []
    workload = []
    dist = []
    agg = []
    thresh = []
    for key in keys:
            k = key.split('_')
            sys.append(k[0])
            workload.append(k[1])
            dist.append(k[2])
            agg.append(k[3])
            thresh.append(float(k[5]))
    sys = list(set(sys))
    workload = list(set(workload))
    dist = list(set(dist))
    dist = sorted(dist)
    agg = list(set(agg))
    agg = sorted(agg)
    thresh = sorted(list(set(thresh)))
    thresh = thresh[4:-1]
    sys, perf = 'DDR5', 'saf'
    outlier_type = 'Voltage Droop' if perf != 'sec' else None
    if outlier_type is None:
        outlier_type = 'Spectre' if sys == 'DDR5' else 'TRRespass'
    sys_type = 'A' if sys == 'DDR4' else 'B'
    fig, ax = plt.subplots(2,2)
    for x, d_type in enumerate(dist):
        d_label = r'$\mathit{d_E(X)}$'if 'STD' in d_type else r'$\mathit{d_C(X)}$'
        for y, a_type in enumerate(agg):
            a_label = r'$\mathit{a_M}$' if 'MEAN' in a_type else r'$\mathit{a_J}$'
            auc_max, auc_min, auc_q1, auc_q3, auc_median = [], [], [], [], []
            for t in thresh:
                auc_scores = [df[f'{sys}_{d}_{d_type}_{a_type}_{RANK}_{t}_{perf}'].tolist()[0] for d in workload]
                auc_max.append(max(auc_scores))
                auc_min.append(min(auc_scores))
                auc_q1.append(np.percentile(auc_scores, 25))
                auc_q3.append(np.percentile(auc_scores, 75))
                auc_median.append(np.median(auc_scores))
            c = color_dist_agg(d_type, a_type)
            ax[x][y].plot(thresh, auc_median, color=c)
            ax[x][y].fill_between(thresh, auc_q1, auc_q3, color=c, alpha=0.3)
            ax[x][y].fill_between(thresh, auc_min, auc_max, color=c, alpha=0.1)
            ax[x][y].set_title(f'Scoring Function {d_label} with Aggregate {a_label}', fontsize=16)
            ax[x][y].set_xlabel(r'$\mathit{m_d}$', fontsize=16)
            ax[x][y].set_ylabel(f'AUCROC', fontsize=16)
    plt.suptitle(f'Setup {sys_type}: {outlier_type}', fontweight='bold', fontsize=20)
    plt.show()

def find_idx_auc(df, workload, sys, method, suffix, term):
    list_of_workloads = df['WORKLOADS']
    search = [idx for idx, d in enumerate(list_of_workloads) if d == workload]
    search = search[0]
    key = f'{sys}_{term}_{method}_{suffix}'
    auc = df[key].tolist()[search]
    return auc

def comp_SOTA():
    df = pd.read_csv(f'MICI_PERF/AUC_SCORES.csv')
    keys = list(df.keys())
    workload = []
    for key in keys:
            k = key.split('_')
            workload.append(k[1])
    workload = list(set(workload))
    num_vars = len(workload)
    angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    num_methods = 4
    fig, ax = plt.subplots(2, 2, subplot_kw=dict(polar=True), figsize=(12, 12))
    d_type = 'STD'
    a_type = 'JOINT'
    th = '0.85'
    for x, sys in enumerate(['DDR4', 'DDR5']):
        name = 'Setup A' if sys == 'DDR4' else 'Setup B'
        scout_suffix = '90_32' if sys == 'DDR4' else '230_32'
        for y, outlier in enumerate(['saf', 'sec']):
            test_name = 'Voltage Droop' if outlier == 'saf' else None
            if test_name is None:
                test_name = 'TRRespass' if sys == 'DDR4' else 'Spectre'
            official = f'{name}: {test_name}'
            prev_term = 'DROOP' if outlier == 'saf' else None
            if prev_term is None:
                prev_term = 'RH' if sys == 'DDR4' else 'SPECTRE' 
            df_octane = pd.read_csv('MICI_PERF/AUC_SCORES.csv')
            df_iforest = pd.read_csv('../IFOREST_MASTER_AUC_SCORES.csv')
            df_autoencoder = pd.read_csv('../AUTOENCODER_MASTER_AUC_SCORES.csv')
            df_scout = pd.read_csv('../SCOUT_MASTER_AUC_SCORES.csv')
            #print(f'SYS: {sys}\tTEST: {outlier}\n=====================')
            OCT, IF, AE, ESC = [], [], [], []
            method_labels = ['OCTANE', 'IFOREST', 'AUTOENCODER', 'E-SCOUT']
            colors = ['m', 'g', 'r', 'y']
            for d in workload:
                OCTANE_key = f'{sys}_{d}_{d_type}_{a_type}_MICI_{th}_{outlier}'
                auc_octane = df_octane[OCTANE_key].tolist()[0]
                auc_iforest = find_idx_auc(df_iforest, d, sys, 'IF', scout_suffix, prev_term)
                auc_autoencoder = find_idx_auc(df_autoencoder, d, sys, 'AE', scout_suffix, prev_term)
                auc_scout = find_idx_auc(df_scout, d, sys, 'STD', scout_suffix, prev_term)
                #print(f'{d}\n\tOCTANE: {auc_octane}\n\tIFOREST: {auc_iforest}\n\tAUTOENCODER: {auc_autoencoder}\n\tESCOUT: {auc_scout}')
                OCT.append(auc_octane)
                IF.append(auc_iforest)
                AE.append(auc_autoencoder)
                ESC.append(auc_scout)
            # Compute mean ranks per method.
            # Create a (n_workloads x 4) matrix with each column corresponding to a method.
            auc_matrix = np.stack((np.array(OCT), np.array(IF), np.array(AE), np.array(ESC)), axis=1)
            # For each workload, compute ranks (ranking in descending order: best AUC gets rank 1).
            # The negative values invert the ranking order.
            ranks = np.array([rankdata(-row, method='average') for row in auc_matrix])
            mean_ranks = np.mean(ranks, axis=0)
            std_ranks = np.var(ranks, axis=0)
            print(f"\nMean Ranks for {sys} - {outlier}:")
            for label, rank_val, std_val in zip(method_labels, mean_ranks, std_ranks):
                print(f"{label}: {rank_val:.2f} +- {std_val:.2f}")
            print('======================')
            all_auc = OCT + IF + AE + ESC
            min_val, max_val = min(all_auc), 1.0
            margin = 0.05 * (max_val - min_val) if max_val != min_val else 0.05
            ax[x][y].set_rlim(min_val-margin, max_val+margin)
            for method_data, color, label in zip([OCT, IF, AE, ESC], colors, method_labels):
                values = method_data + [method_data[0]]
                ax[x][y].plot(angles, values, color=color, label=label, linewidth=2)
            CAP_work = [w.upper() for w in workload]
            ax[x][y].set_thetagrids(np.degrees(angles[:-1]), CAP_work)
            ax[x][y].set_title(official, y=1.1, fontweight='bold')
            if x == 1 and y == 1: ax[x][y].legend(loc='lower center', ncol=4, shadow=True, fancybox=True, bbox_to_anchor=(-0.3, -0.4))
    plt.show()

def main():
    #perf_analysis()
    #AUC_graph()
    #comp_SOTA()
    #automate_perf()
    similarity_TD_per_sys()
    #similarity_TD_cross_sys()

if __name__=="__main__":
    main()


