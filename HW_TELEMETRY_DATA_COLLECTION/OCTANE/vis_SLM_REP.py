# Author | Eduardo Ortega
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
PLATFORMS = ['DDR4', 'DDR5']
datasets = ['dft', 'dj', 'dp', 'gl', 'gs', 'ha', 'ja', 'mm', 'ni', 'oe', 'pi', 'sh', 'tr']

def vis_COMP():
    fig, ax = plt.subplots(2,2)
    for r, sigma in enumerate([0.01, 0.02]):
        df = pd.read_csv(f'COMP_{sigma}.csv')
        for i, p in enumerate(PLATFORMS):
            df_w = df[df['Platform'] == p]
            z = []
            for a in datasets:
                z_y = []
                for b in datasets:
                    print(p,a,b)
                    vals = df_w[(df_w['WA'] == a) & (df_w['WB'] == b)]['CKA'].tolist()[0]
                    z_y.append(vals)
                z.append(np.array(z_y))
            z = np.array(z)
            im = ax[i][r].imshow(z, cmap='viridis', vmin=0.0, vmax=1.0)
            fig.colorbar(im, ax=ax[i][r], shrink=0.6)
            ax[i][r].set_xticks(range(len(datasets)))
            ax[i][r].set_xticklabels(datasets)
            ax[i][r].set_yticks(range(len(datasets)))
            ax[i][r].set_yticklabels(datasets)
            p_title = 'Platform A' if 'DDR4' in p else 'Platform B'
            ax[i][r].set_title(f'{p_title} ({sigma})', fontweight='bold')
    plt.show()


def vis_CROSS():
    fig, ax = plt.subplots(1,5)
    for i, p in enumerate([0.01, 0.02, 0.03, 0.04, 0.05]):
        df_w  = pd.read_csv(f'CROSS_{p}.csv')
        z = []
        for a in datasets:
            z_y = []
            for b in datasets:
                print(p,a,b)
                vals = df_w[(df_w['WA'] == a) & (df_w['WB'] == b)]['CKA'].tolist()[0]
                z_y.append(vals)
            z.append(np.array(z_y))
        z = np.array(z)
        im = ax[i].imshow(z, cmap='viridis', vmin=0.0, vmax=1.0)
        fig.colorbar(im, ax=ax[i], shrink=0.8)
        ax[i].set_xticks(range(len(datasets)))
        ax[i].set_xticklabels(datasets)
        ax[i].set_yticks(range(len(datasets)))
        ax[i].set_yticklabels(datasets)
        p_title = r'RBF $\sigma$ Ratio: '
        p_title = f"{p_title}{p}"
        ax[i].set_title(f'{p_title}', fontweight='bold')
    plt.show()

def main():
    vis_COMP()
    #vis_CROSS()

if __name__=="__main__":
    main()
