# Author | Eduardo Ortega
import glob
import pandas as pd
from FCResNet import TabularResNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim
from pytorch_tabnet.tab_model import TabNetClassifier
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
thresh = 0.85
dist_type = 'STD'
agg_type = 'JOINT'

def do_analysis_single(csv_list, rig_type):
    df_list = {}
    for f_type in ['nom', 'sec', 'saf']:
        for score_type in ['agg', 'compute', 'memory', 'sensor']:
            df_list[f"{f_type}_{score_type}"] = []
    for csv in csv_list:
        df = pd.read_csv(csv)
        workload = csv.split('/')[-1].strip().split('_')[1].strip().split('_')[0].strip()
        for f_type in ['nom', 'sec', 'saf']:
            for score_type in ['agg', 'compute', 'memory', 'sensor']:
                key = f"{workload}_{dist_type}_{agg_type}_MICI_{thresh}_{f_type}_{score_type}"
                df_data = df[key].tolist()
                cloud_key = f"{f_type}_{score_type}"
                df_list[cloud_key] += df_data
    list_of_df = []
    for idx, f_type in enumerate(['nom', 'sec', 'saf']):
        label = idx
        df = pd.DataFrame()
        for score_type in ['agg', 'compute', 'memory', 'sensor']:
            df[f'{score_type}'] = df_list[f'{f_type}_{score_type}']
        num_data = df.shape[0]
        target = [label] * num_data
        df['target'] = target
        list_of_df.append(df)
    df = pd.concat(list_of_df, ignore_index=True)
    df.to_csv(f"{rig_type}_CLOUD.csv", index=False)
    

def create_individual():
    list_csv = glob.glob('MICI_PERF/*csv')
    ddr4_list = [l for l in list_csv if 'DDR4' in l and dist_type in l and agg_type in l]
    ddr5_list = [l for l in list_csv if 'DDR5' in l and dist_type in l and agg_type in l]
    do_analysis_single(ddr5_list, 'DDR5')


def create_comb():
    ddr4 = pd.read_csv('./CLOUD/DDR4_CLOUD.csv')
    ddr5 = pd.read_csv('./CLOUD/DDR5_CLOUD.csv')
    df_list = [ddr4, ddr5]
    df = pd.concat(df_list, ignore_index=True)
    df.to_csv(f"./CLOUD/COMB_CLOUD.csv", index=True)

def train_resnet(X_train, y_train, X_test, y_test, input_dim, output_dim, epochs=10, batch_size=64):
    # Initialize the model, loss function, and optimizer.
    model = TabularResNet(input_dim=input_dim, output_dim=output_dim)
    criterion = nn.BCEWithLogitsLoss()  # assuming binary classification
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Prepare torch datasets and loaders.
    X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).unsqueeze(1)
    train_dataset = torch.utils.data.TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # Training loop.
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0.0
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        print(f"ResNet | Epoch {epoch+1}/{epochs} - Loss: {epoch_loss/len(train_loader):.4f}")

    # Evaluation on the test set.
    model.eval()
    X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
    with torch.no_grad():
        outputs = model(X_test_tensor)
        probs = torch.sigmoid(outputs)
        preds = (probs > 0.5).float().squeeze().numpy()
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average='macro')
    return acc, f1

def train_tabnet(X_train, y_train, X_test, y_test, max_epochs=10, batch_size=64):
    # Initialize TabNetClassifier.
    tabnet = TabNetClassifier(
        optimizer_fn=torch.optim.Adam,
        optimizer_params=dict(lr=2e-2),
        scheduler_params={"step_size": 10, "gamma": 0.9},
        scheduler_fn=torch.optim.lr_scheduler.StepLR,
        mask_type='sparsemax'
    )
    # Fit the TabNet model.
    tabnet.fit(
        X_train.values, y_train.values,
        eval_set=[(X_train.values, y_train.values), (X_test.values, y_test.values)],
        eval_name=['train', 'valid'],
        eval_metric=['accuracy'],
        max_epochs=max_epochs,
        patience=5,
        batch_size=batch_size,
        virtual_batch_size=32,
        num_workers=0,
        drop_last=False,
    )
    preds = tabnet.predict(X_test.values)
    acc = (preds == y_test.values).mean()
    f1 = f1_score(y_test, preds, average='macro')
    return acc, f1

def train_xgb(X_train, y_train, X_test, y_test):
    # Initialize and fit the XGBClassifier.
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    xgb.fit(X_train, y_train)
    preds = xgb.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average='macro')
    return acc, f1

def GEN_ML_OCT_SWEEPS():
    # List of CSV data paths.
    data_csv = ['./CLOUD/DDR4_CLOUD.csv', './CLOUD/DDR5_CLOUD.csv', './CLOUD/COMB_CLOUD.csv']
    df_CLOUD_results = pd.DataFrame()
    df_CLOUD_results['MODEL_TESTSPLIT'] = ['ACC', 'MACRO F1']
    # Loop through each CSV file.
    for test_split in [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]:
        print(test_split)
        for data in data_csv:
            print(f"\nProcessing file: {data}")
            d = 'COMB' if 'COMB' in data else None
            if d is None:
                d = 'DDR4' if 'DDR4' in data else 'DDR5'
            df = pd.read_csv(data)
            # Assume the last column is the target and the first columns are features.
            X = df.iloc[:, :-1]
            y = df.iloc[:, -1]
            # Split data into training and testing sets.
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            # Define input and output dimensions.
            input_dim = X_train.shape[1]
            output_dim = 1  # For binary classification
            print('training RESNET') 
            # Train and evaluate ResNet.
            resnet_acc, resnet_f1 = train_resnet(X_train, y_train, X_test, y_test, input_dim, output_dim)
            df_CLOUD_results[f'FCRESNET18_{test_split}_{d}'] = [resnet_acc, resnet_f1]
            print(f"ResNet Model Accuracy (F1) on {data}: {resnet_acc:.4f}\n{resnet_f1:.4f}\n===================")
            print('TRAIN TABNET')
            # Train and evaluate TabNet.
            tabnet_acc, tabnet_f1 = train_tabnet(X_train, y_train, X_test, y_test)
            df_CLOUD_results[f'TABNET4_{test_split}_{d}'] = [tabnet_acc, tabnet_f1]
            print(f"TabNet Model Accuracy (F1) on {data}: {tabnet_acc:.4f}\n{tabnet_f1:.4f}\n===================")
            print('XGB')
            # Train and evaluate XGBoost.
            xgb_acc, xgb_f1 = train_xgb(X_train, y_train, X_test, y_test)
            df_CLOUD_results[f'XGB_{test_split}_{d}'] = [xgb_acc, xgb_f1]
            print(f"XGBoost Model Accuracy (F1) on {data}: {xgb_acc:.4f}\n{xgb_f1:.4f}\n=========================")
    df_CLOUD_results.to_csv('MASTER_CLOUD.csv', index=False)

def main():
    df = pd.read_csv('./CLOUD/MASTER_CLOUD.csv')
    keys = [c for c in df.columns]
    test_split = [0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    xlabels = [f"{int(100*t)}/{int(100*(1-t))}" for t in test_split]
    models = ['FCRESNET18', 'TABNET4', 'XGB']
    color_m = {'FCRESNET18':'r', 'TABNET4':'b', 'XGB':'g'}
    DATA = ['DDR4', 'DDR5', 'COMB']
    fig, ax = plt.subplots(1, 3)
    for idx, d in enumerate(DATA):
        title = 'ALL' if 'COMB' in d else None
        if title is None:
            title = 'SETUP A' if 'DDR4' in d else 'SETUP B'
        for m in models:
            acc = [df[f"{m}_{t}_{d}"].tolist()[0] for t in test_split]
            f1 = [df[f"{m}_{t}_{d}"].tolist()[1] for t in test_split]
            ax[idx].plot(test_split, acc, color=color_m[m], linestyle='-', label=f'{m} Accuracy')
            ax[idx].plot(test_split, f1, color=color_m[m], linestyle=':', label=f'{m} F1-Score')
            ax[idx].set_xticks(test_split)
            ax[idx].set_xticklabels(xlabels)
            ax[idx].set_xlabel('Test/Train Split', fontweight='bold')
            ax[idx].set_ylabel('Classification\nPerformance', fontweight='bold')
        ax[idx].set_title(title, fontweight='bold')
        if idx == 1:
            ax[idx].legend(shadow=True, fancybox=True, ncol=3, loc='lower center', bbox_to_anchor=(0.5, -1.1))
    plt.show()


if __name__=="__main__":
    main()
