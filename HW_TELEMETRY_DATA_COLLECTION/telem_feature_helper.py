#Author | Eduardo Ortega
import glob, os
import pandas as pd


def number_of_telemetry_features(ddr4_paths, ddr5_paths):
    for rig in [ddr4_paths, ddr5_paths]:
        if "DDR4" in rig:
            print("DDR4")
        else:
            print("DDR5")
        print("WORKLOAD : NUM FEATURES")
        for f in rig:
            df = pd.read_csv(f, index_col=False)
            df = df.drop('Unnamed: 0', axis=1)
            num_features = len(df.keys())
            workload = f.split('_')[-1].strip().split('.')[0].strip()
            print(f"{workload} : {num_features}")

def return_paths(benign=True):
    if benign:
        ddr4_paths = glob.glob(f"{os.getcwd()}/TELEMETRY_DATA/DDR4_benign_*.csv")
        ddr5_paths = glob.glob(f"{os.getcwd()}/TELEMETRY_DATA/DDR5_benign_*.csv")
    else:
        ddr4_paths = glob.glob(f"{os.getcwd()}/TELEMETRY_DATA/DDR4_*.csv")
        ddr5_paths = glob.glob(f"{os.getcwd()}/TELEMETRY_DATA/DDR5_*.csv")
    return ddr4_paths, ddr5_paths

def copy_files_into_16_32(paths):
    for idx, f in enumerate(paths):
        if idx % 5 == 0: print(f"Progress: {idx/len(paths)}")
        path_16 = f"{os.getcwd()}/TD_16/"
        path_32 = f"{os.getcwd()}/TD_32/"
        df = pd.read_csv(f, index_col=False)
        df = df.drop('Unnamed: 0', axis=1)
        df_16, df_32 = df.astype('float16'), df.astype('float32')
        file_name = f.split('/')[-1].strip()
        path_16 += file_name
        path_32 += file_name
        df_16.to_csv(path_16, index=False)
        df_32.to_csv(path_32, index=False)

def main():
    ddr4_p, ddr5_p = return_paths(benign=True)
    number_of_telemetry_features(ddr4_p, ddr5_p)
    quit()
    print("DDR4")
    copy_files_into_16_32(ddr4_p)
    print("DDR5")
    copy_files_into_16_32(ddr5_p)

if __name__=="__main__":
    main()
