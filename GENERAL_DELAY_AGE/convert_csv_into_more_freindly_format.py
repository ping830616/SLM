# Author | Eduardo Ortega
import pandas as pd

def main():
    path_to_csv = "data_buffer.csv" #"driver_stages_buff_analysis.csv"
    df = pd.read_csv(path_to_csv)
    num_data = df.shape[0]
    df = df.tail(int(num_data/2))
    df_new = pd.DataFrame()
    key_list = list(df.keys())
    print(key_list[0])
    df_new['t'] = df[key_list[0]]
    #key_list = [key for key in key_list if "driver" in key or "stage_one" in key or "stage_two" in key]
    for key in key_list[1:]:
        print(key)
        options = key.split(":")
        placement = options[0].split("(")[-1].strip().split(")")[0].strip()
        voltage = options[1].split("=")[-1].strip()
        voltage = voltage if 'm' not in voltage else int(voltage.split("m")[0].strip())/1000
        temp = options[2]
        temp = temp.split('=')[-1]
        new_key = f"{placement}_{voltage}_{temp}".strip()
        df_new[new_key] = df[key]
    df_new.to_csv('sim_data_buffer_vt_sweep.csv', index=False)

if __name__=="__main__":
    main()
