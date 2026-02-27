# Author | Eduardo Ortega
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
setup_a_nf = 181
setup_b_nf = 460
ratio = 0.5
prec = 32
RH = "RH"
SPECTRE = "SPECTRE"
DROOP_DDR4 = "DROOP_4"
DROOP_DDR5 = "DROOP_5"
DROOP = "DROOP"

def plot_box_plot(scout, autoencoder, iforest, memory=False):
    fig, ax = plt.subplots(4, 1)
    for row, case in enumerate([RH, SPECTRE, DROOP_DDR4, DROOP_DDR5]):
        if case == RH or case == DROOP_DDR4:
            rig = "DDR4"
            nf = int(ratio*setup_a_nf)
            if case == RH: situation = "TRRespass"
        else:
            rig = "DDR5"
            nf = int(ratio*setup_b_nf)
            if case == SPECTRE: situation = case
        if case == DROOP_DDR4 or case == DROOP_DDR5:
            case = DROOP
            situation = "V-DROOP"
        if_key = f"{rig}_{case}_IF_{nf}_{prec}"
        if_data = iforest[if_key]
        sc_key = f"{rig}_{case}_STD_{nf}_{prec}"
        sc_data = scout[sc_key]
        ae_key = f"{rig}_{case}_AE_{nf}_{prec}"
        ae_data = autoencoder[ae_key]
        print(f"{rig} and {case} and {situation}")
        print(f"AUC: SCOUT AUTOENCODER IFOREST")
        print(f"AUC: {np.average(sc_data)} {np.average(ae_data)} {np.average(if_data)}")
        print("=======================")
        ax[row].boxplot([sc_data, if_data, ae_data], 
                    positions=[0, 1, 2],
                    whis=(0, 100),
                    labels=["SCOUT", "IFOREST", "AUTOENCODER"])
        if case != DROOP:
            ax[row].set_ylabel(f"{situation}\nAUC", fontweight='bold')
        else:
            if rig == "DDR4":
                ax[row].set_ylabel(f"{situation}\n(SETUP A)\nAUC", fontweight='bold')
            else:
                ax[row].set_ylabel(f"{situation}\n(SETUP B)\nAUC", fontweight='bold')
        #if not memory: ax[row].set_ylim([0.5, 1.0])
    plt.show()


def auc_plot():
    scout_data = pd.read_csv(f"{os.getcwd()}/SCOUT_MASTER_AUC_SCORES.csv", index_col=False)
    ae_data = pd.read_csv(f"{os.getcwd()}/AUTOENCODER_MASTER_AUC_SCORES.csv", index_col=False)
    if_data = pd.read_csv(f"{os.getcwd()}/IFOREST_MASTER_AUC_SCORES.csv", index_col=False)
    plot_box_plot(scout_data, ae_data, if_data)

def memory_plot():
    scout_data = pd.read_csv(f"{os.getcwd()}/SCOUT_MASTER_MEMORY.csv", index_col=False)
    ae_data = pd.read_csv(f"{os.getcwd()}/AUTOENCODER_MASTER_MEMORY.csv", index_col=False)
    if_data = pd.read_csv(f"{os.getcwd()}/IFOREST_MASTER_MEMORY.csv", index_col=False)
    plot_box_plot(scout_data, ae_data, if_data, memory=True)

def main():
    #auc_plot()
    memory_plot()

if __name__=="__main__":
    main()
