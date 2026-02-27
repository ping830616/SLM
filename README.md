# SLM RAS
SLM => SIlicon Lifecycle Management, RAS => Reliability, Availability, and Servicability

This repo is built off of two projects, hardware telmetry anomaly detection and telemetry sensor design.

# (1) HARDWARE TELEMETRY ANOMALY DETECTION
This portion will be for real-silicon hardware telemetry data collection. The current method of obtaining results are through INTEL PCM (https://github.com/intel/pcm).

The specific anomaly detection will is in Eduardo's main grad school experimental repo - it will be copied here once complete.


The description below is for voltage droop analysis and eventual telemetry sesnor design.

# (2) VOLTAGE DROOP AUTOMATION
VOLTAGE DROOP FLOW AUTOMATION - FLOW is based off of Hardware Trojan Work from Jonti & Akshay

Picture Describing the flow is below
![alt text](https://github.com/eduardoortegathethird/SLM_RAS/blob/main/pics/voltage_telemetry.png)

**FLOW FOR ONE BENCHMARK**

(1) Synopsys VCS uses TB on $name_rtl.v (provided by CEP github) => VCD file ($name_rtl.vcd) & .elf file (CHECK SIMULATION FOLDER OUTPUT log file,, EDIT TB)

(2) Synopsys Design Compiler use $name_rtl.v => generates synthesized netlist ($name_syn.v) & SDC file ($name_syn.sdc) & SDF file ($name_syn.sdf)

(3) Synopsys VCS uses TB on $name_syn.v (TB provided by CEP github) => VCD file ($name_syn.vcd) & .elf file (CHECK SIMULATION OUTPUT log file, EDIT TB)

(4) Cadence Innovus uses $name_syn.v & SDC file ($name_syn.sdc) & SDF file ($name_syn.sdf) => generate GDSII file ($name_apr.gds), post layout $name_apr.v, timing file (WC) $name_apr.txt, static timing and parasitic file $name_apr.spf, definition file $name_apr.def, specification zip $name_apr.spef.gz, and folder $name_apr.enc.dat/ (run innovus in APR)

(5) Check timing file from Innovus $name_apr.txt to see if it pass, go back to (2) and adjust Synopsys DC commands (frequency), if pass continue

(6) Synopsys VCS uses TB on $name_apr.v (TB provided by CEP github) => VCD file ($name_apr.vcd) & .elf file (CHECK SIMULATION OUTPUT log file, EDIT TB) GOLDEN VCD FILE FOR VOLTUS

MANUAL STEP (7)

(7) Cadence Voltus uses golden VCD file ($name_apr.vcd) & GDSII file ($name_apr.gds) & folder $name_apr.enc.dat/ & specification zip $name_apr.spef.gz

TODO: RTL FOLDER HOLDS ALL BENCHMARKS

Synopsys DC call on RTL (RTL/$name.v), outputs synthesized gate netlist (synthesis/$name.v)

### Verify Tools are Installed correctly
**SYNOPSYS DESIGN COMPILER**
``` console
foo@bar: which dc_shell
/usr/local/tools/Synopsys/syn/S-2021.06-SP5-4/bin/dc_shell
```
**SYNOPSYS VCS**
``` console
foo@bar: which vcs
/usr/local/tools/Synopsys/vcs_vQ-2020.03-SP2.dve/vcs/Q-2020.03-SP2/bin/vcs
```
**CADENCE INNOVUS**
``` console
foo@bar: which innovus
/usr/local/tools/cadence/INNOVUS2114/bin/innovus
```

**BASHRC edits**
I recommend editing your path on BASHRC to ensure thateach tool is able to be seen on your current bash path. For example, see the console below.
``` console
# TOOL PATH
foo@bar: tool_path="PATH_TO_TOOL"
# VIM into ~/.bashrc file (rc stands for register cache)
foo@bar: vim ~/.bashrc
# Edit your $PATH to the following notation
PATH="$PATH:$TOOL_PATH"
```
