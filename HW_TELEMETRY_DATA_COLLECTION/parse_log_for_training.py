#Author | Eduardo Ortega
import pandas as pd
import numpy as np
import glob, os, time, shutil
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
DDR4 = "DDR4"
DDR5 = "DDR5"
DDR4_ATTACK = "RH"
DDR5_ATTACK = "SPECTRE"
DROOP = "DROOP"
workloads = [dft, dp, dj, gs, gl, ha, ja, mm, ni, oe, pi, sh, tr]


def parse_regen_logs_pcm(folder):
    wd = f'{folder}/log_*.csv'
    for idx, name in enumerate(glob.glob(f"{wd}")):
        df = pd.read_csv(name)
        df_new = pd.DataFrame()
        for key in list(df.keys())[2:-1]:
            col = df[key]
            new_key = f"{key}_{col[0]}"
            new_col = col[1:]
            df_new[new_key] = new_col
        df_new.to_csv(f'{folder}/logT_{idx}.csv', index=False)

def parse_regen_logs_volt(folder):
    wd = f"{folder}/logVolt_*.txt"
    for idx, name in enumerate(glob.glob(f"{wd}")):
        f = open(name, 'r')
        info = f.read()
        info = info.split("\n")[0:-1]
        df = pd.DataFrame()
        df["CPU Voltage"] = info
        f.close()
        df.to_csv(f"{folder}/logVoltT_{idx}.csv", index=False)

def temp_parse(fline):
    val = float(fline.split("+")[1].strip().split("°")[0].strip())
    return val

def parse_regen_logs_temp_DDR5(folder):
    wd = f"{folder}/logTemp_*.txt"
    for idx, name in enumerate(glob.glob(f"{wd}")):
        core_t0, core_t4, core_t8, core_t12 = [], [], [], []
        core_t16, core_t20, core_t28, core_t29 = [], [], [], []
        core_t30, core_t31 = [], []
        acpi_t1 = []
        pci_sensor_t1, pci_sensor_t2 = [], []
        f = open(name, "r")
        for fline in f.read().split("\n"):
            if "Core 0:" in fline: core_t0.append(temp_parse(fline))
            if "Core 4:" in fline: core_t4.append(temp_parse(fline))
            if "Core 8:" in fline: core_t8.append(temp_parse(fline))
            if "Core 12:" in fline: core_t12.append(temp_parse(fline))
            if "Core 16:" in fline: core_t16.append(temp_parse(fline))
            if "Core 20:" in fline: core_t20.append(temp_parse(fline))
            if "Core 28:" in fline: core_t28.append(temp_parse(fline))
            if "Core 29:" in fline: core_t29.append(temp_parse(fline))
            if "Core 30:" in fline: core_t30.append(temp_parse(fline))
            if "Core 31:" in fline: core_t31.append(temp_parse(fline))
            if "temp1:" in fline: acpi_t1.append(temp_parse(fline))
            if "Sensor 1:" in fline: pci_sensor_t1.append(temp_parse(fline))
            if "Sensor 2:" in fline: pci_sensor_t2.append(temp_parse(fline))
        df = pd.DataFrame()
        df["TEMP_CORE_0"] = core_t0
        df["TEMP_CORE_4"] = core_t4
        df["TEMP_CORE_8"] = core_t8
        df["TEMP_CORE_12"] = core_t12
        df["TEMP_CORE_16"] = core_t16
        df["TEMP_CORE_20"] = core_t20
        df["TEMP_CORE_28"] = core_t28
        df["TEMP_CORE_29"] = core_t29
        df["TEMP_CORE_30"] = core_t30
        df["TEMP_CORE_31"] = core_t31
        df.to_csv(f"{folder}/logTempT_{idx}.csv", index=False)

def parse_regen_logs_temp_DDR4(folder):
    wd = f"{folder}/logTemp_*.txt"
    for idx, name in enumerate(glob.glob(f"{wd}")):
        core_t0, core_t1, core_t2, core_t3 = [], [], [], []
        acpi_t1, acpi_t2 = [], []
        pci_sensor_t1, pci_sensor_t2 = [], []
        f = open(name, "r")
        for fline in f.read().split("\n"):
            if "Core 0" in fline: core_t0.append(temp_parse(fline))
            if "Core 1" in fline: core_t1.append(temp_parse(fline))
            if "Core 2" in fline: core_t2.append(temp_parse(fline))
            if "Core 3" in fline: core_t3.append(temp_parse(fline))
            if "temp1:" in fline: acpi_t1.append(temp_parse(fline))
            if "temp2:" in fline: acpi_t2.append(temp_parse(fline))
            if "Sensor 1:" in fline: pci_sensor_t1.append(temp_parse(fline))
            if "Sensor 2:" in fline: pci_sensor_t2.append(temp_parse(fline))
        df = pd.DataFrame()
        df["TEMP_CORE_0"] = core_t0
        df["TEMP_CORE_1"] = core_t1
        df["TEMP_CORE_2"] = core_t2
        df["TEMP_CORE_3"] = core_t3
        df["TEMP_ACPI_1"] = acpi_t1
        df["TEMP_ACPI_2"] = acpi_t2
        df["TEMP_PCI_1"] = pci_sensor_t1
        df["TEMP_PCI_2"] = pci_sensor_t2
        df.to_csv(f"{folder}/logTempT_{idx}.csv", index=False)

def combine_logT(folder, name_file):
    df_pcm_list = [pd.read_csv(name) for name in glob.glob(f"{folder}/logT_*.csv")]
    df_volt_list = [pd.read_csv(name) for name in glob.glob(f"{folder}/logVoltT_*.csv")]
    df_temp_list = [pd.read_csv(name) for name in glob.glob(f"{folder}/logTempT_*.csv")]
    df_pcm = pd.concat(df_pcm_list, axis=0)
    df_volt = pd.concat(df_volt_list, axis=0)
    df_temp = pd.concat(df_temp_list, axis=0)
    df_pcm.to_csv(f"{folder}/{name_file}_pcm.csv", index=False)
    df_volt.to_csv(f"{folder}/{name_file}_volt.csv", index=False)
    df_temp.to_csv(f"{folder}/{name_file}_temp.csv", index=False)

def combine_log(folder, name_file):
    td = f"{folder}/{name_file}"
    df_pcm, df_volt, df_temp = pd.read_csv(f"{td}_pcm.csv"), pd.read_csv(f"{td}_volt.csv"), pd.read_csv(f"{td}_temp.csv")
    for df in [df_volt, df_temp]:
        for k in df.keys():
            data = []
            for ele in df[k].to_list():
                data.extend([ele]*5)
            df_pcm[k] = data
    df_pcm.to_csv(f"{td}.csv")
    return f"{td}.csv"

def parse_regen_logs(folder, rig):
    print(f"=================\n{folder}\n==================")
    parse_regen_logs_pcm(folder)
    parse_regen_logs_volt(folder)
    if rig == "DDR4":
        parse_regen_logs_temp_DDR4(folder)
    else:
        parse_regen_logs_temp_DDR5(folder)
   
def combine_logs(folder, name_file):
    combine_logT(folder, name_file)
    path_to_master_log = combine_log(folder, name_file)
    return path_to_master_log

def copy_master_log_to_telemetry(name_file, ml_path):
    file_name = ml_path.split("/")[-1].strip()
    td_path = f"{os.getcwd()}/TELEMETRY_DATA/{file_name}"
    shutil.copy(ml_path, td_path)
    print(f"{name_file}'s data is in TELEMETRY_DATA, ready for processing")

def master_recombine():
    for rig in ["DDR5"]: #, ["DDR4", "DDR5"]:
        for situation in ["benign", "attack", "DROOP"]:
            if situation == "attack": 
                situation_type = "RH" if rig == "DDR4" else "SPECTRE"
            else:
                situation_type = situation
            bchmrk_type = rig if situation == "benign" else f"{rig}_{situation_type}"
            for bchmrk in workloads:
                print(f"{bchmrk}")
                path_to_folder = f"{os.getcwd()}/{bchmrk_type}/{bchmrk}"
                parse_regen_logs(path_to_folder, rig)
                name_file = f"{rig}_{situation_type}_{bchmrk}"
                master_log_path = combine_logs(path_to_folder, name_file)
                copy_master_log_to_telemetry(name_file, master_log_path)
def main():
    master_recombine()

if __name__=="__main__":
    main()
