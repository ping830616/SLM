# Author | Eduardo Ortega
import os, glob
import pandas as pd
from simpleL2Class import L2_CLASS as SCOUT
import fi_rankings as helper
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

SCOUT_CLOUD_DATA = f"{os.getcwd()}/SCOUT_CLOUD_DATA/"
SCOUT_DIAGNOSIS = f"{os.getcwd()}/SCOUT_DIAGNOSIS/"
path_32_data = f"{os.getcwd()}/TD_32/"
dft = "dft"
dj = "dj"
dp = "dp"
gs = "gs"
gl = "gl"
ha = "ha"
ja = "ja"
mm = "mm"
ni = "ni"
oe = "oe"
pi = "pi"
sh = "sh"
tr = "tr"
workloads = [dft, dj, dp, gs, gl, ha, ja, mm, ni, oe, pi, sh, tr]
benign = "benign"
rig_ddr4 = "DDR4"
rig_ddr5 = "DDR5"
droop = "DROOP"
rh = "RH"
spectre = "SPECTRE"
SCOUT_TYPE = "STD"
rigs = [rig_ddr4, rig_ddr5]
security = {rig_ddr4: f"{rig_ddr4}_{rh}", rig_ddr5:f"{rig_ddr5}_{spectre}"}
safety = {rig_ddr4:f"{rig_ddr4}_{droop}", rig_ddr5:f"{rig_ddr5}_{droop}"}
nominal = {rig_ddr4:f"{rig_ddr4}_{benign}", rig_ddr5:f"{rig_ddr5}_{benign}"}

def write_data():
    for w in workloads:
        for r in rigs:
            print(f"WORKLOAD: {w}\tRIG: {r}")
            sec_key = security[r]
            safe_key = safety[r]
            nom_key = nominal[r]
            nom_path = f"{path_32_data}{nom_key}_{w}.csv"
            sec_path = f"{path_32_data}{sec_key}_{w}.csv"
            saf_path = f"{path_32_data}{safe_key}_{w}.csv"
            print(saf_path)
            print(sec_path)
            print(nom_path)
            df_nom = pd.read_csv(nom_path, index_col=False)
            df_sec = pd.read_csv(sec_path, index_col=False)
            df_saf = pd.read_csv(saf_path, index_col=False)
            nf = int(0.5*df_nom.shape[1])
            features = helper.grab_features(nf, w, nom_path)
            x_train = df_nom[features].to_numpy(dtype='float32') 
            x_test_nom = x_train
            x_test_security = df_sec[features].to_numpy(dtype='float32')
            x_test_safety = df_saf[features].to_numpy(dtype='float32')
            scout = SCOUT(x_train=x_train, l2=SCOUT_TYPE)
            scout = scout.fit()
            s_nom = scout.predict(x_test_nom)
            s_sec = scout.predict(x_test_security)
            s_saf = scout.predict(x_test_safety)
            df_list = []
            for idx, s in enumerate([s_nom, s_saf, s_sec]):
                df_cloud = pd.DataFrame()
                df_cloud['scores'] = s
                target_nom = [idx] * len(s)
                df_cloud['target'] = target_nom
                df_list.append(df_cloud)
            df_master = pd.concat(df_list, axis=0)
            cloud_data_path = f"{SCOUT_CLOUD_DATA}{r}_{w}.csv"
            print(f"saving to {cloud_data_path}")
            df_master.to_csv(cloud_data_path, index=False)

def automate_learning():
    df_cloud = pd.DataFrame()
    df_cloud['workloads'] = workloads
    for r in rigs:
        rfc_acc, rfc_f1 = [], []
        dtc_acc, dtc_f1 = [], []
        gbc_acc, gbc_f1 = [], []
        nnc_acc, nnc_f1 = [], []
        for w in workloads:
            path = f"{SCOUT_CLOUD_DATA}{r}_{w}.csv"
            print(f"learning: {path}")
            df = pd.read_csv(path, index_col=False)
            x = df['scores'].to_numpy('float32')
            y = df['target'].to_numpy('float32')
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
            x_train = x_train.reshape(-1, 1)
            x_test = x_test.reshape(-1, 1)
            rfc = RandomForestClassifier()
            dtc = DecisionTreeClassifier()
            gbc = GradientBoostingClassifier()
            nnc = MLPClassifier()
            print(f"TRAINING ALL MODELS")
            rfc.fit(x_train, y_train)
            dtc.fit(x_train, y_train)
            gbc.fit(x_train, y_train)
            nnc.fit(x_train, y_train)
            print(f"PREDICTING...")
            y_pred_rfc = rfc.predict(x_test)
            y_pred_dtc = dtc.predict(x_test)
            y_pred_gbc = gbc.predict(x_test)
            y_pred_nnc = nnc.predict(x_test)
            print("====================")
            acc_rfc = accuracy_score(y_test, y_pred_rfc)
            acc_dtc = accuracy_score(y_test, y_pred_dtc)
            acc_gbc = accuracy_score(y_test, y_pred_gbc)
            acc_nnc = accuracy_score(y_test, y_pred_nnc)
            rfc_acc.append(acc_rfc)
            dtc_acc.append(acc_dtc)
            gbc_acc.append(acc_gbc)
            nnc_acc.append(acc_nnc)
            f1_rfc = f1_score(y_test, y_pred_rfc, average='macro')
            f1_dtc = f1_score(y_test, y_pred_dtc, average='macro')
            f1_gbc = f1_score(y_test, y_pred_gbc, average='macro')
            f1_nnc = f1_score(y_test, y_pred_nnc, average='macro')
            rfc_f1.append(f1_rfc)
            dtc_f1.append(f1_dtc)
            gbc_f1.append(f1_gbc)
            nnc_f1.append(f1_nnc)
            print("ClassifierModel: ACC\tF1")
            print(f"RandomForest: {acc_rfc}\t{f1_rfc}")
            print(f"DecisionTree: {acc_dtc}\t{f1_dtc}")
            print(f"XGBoost: {acc_gbc}\t{f1_gbc}")
            print(f"MLPerceptron: {acc_nnc}\t{f1_nnc}")
            print("Done...")
        df_cloud[f"{r}_RF_ACC"] = rfc_acc
        df_cloud[f"{r}_RF_F1"] = rfc_f1 
        df_cloud[f"{r}_DT_ACC"] = dtc_acc
        df_cloud[f"{r}_DT_F1"] = dtc_f1
        df_cloud[f"{r}_GB_ACC"] = gbc_acc
        df_cloud[f"{r}_GB_F1"] = gbc_f1
        df_cloud[f"{r}_NN_ACC"] = nnc_acc
        df_cloud[f"{r}_NN_F1"] = nnc_f1
    df_cloud.to_csv("SCOUT_CLOUD_RESULTS.csv", index=False)

def make_diagram():
    df = pd.read_csv('SCOUT_CLOUD_RESULTS.csv', index_col=False)
    fig, ax = plt.subplots(2, 2)
    for col, r in enumerate(rigs):
        for row, metric in enumerate(['ACC', 'F1']):
            yl = "Accuracy" if metric == 'ACC' else "F1-Score"
            title = "SETUP A" if col == 0 else "SETUP B"
            data_rf = df[f"{r}_RF_{metric}"]
            data_dt = df[f"{r}_DT_{metric}"]
            data_gb = df[f"{r}_GB_{metric}"]
            data_nn = df[f"{r}_NN_{metric}"]
            ax[row][col].boxplot([data_rf, data_dt, data_gb, data_nn], 
                                positions=[0, 1, 2, 3],
                                whis=(0, 100),
                                labels=["Random Forest", "Decision Forest", "XGBoost", "ML-Perceptron"])
            ax[row][col].set_ylabel(yl, fontweight='bold')
            if row == 0: 
                ax[row][col].set_title(title, fontweight='bold')
                ax[row][col].set_ylim([0.3, 1.0])
            else:
                ax[row][col].set_ylim([0.3, 1.0])
    plt.show()

def main():
    #write_data()
    #automate_learning()
    make_diagram()

if __name__=="__main__":
    main()
