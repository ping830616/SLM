# ####################################################################

#  Created by Encounter(R) RTL Compiler v12.10-s012_1 on Wed Dec 03 10:07:01 -0700 2014

# ####################################################################

#set sdc_version 1.7

#set_units -capacitance 1000.0fF
#set_units -time 1000.0ps

# Set the current design
#current_design multiplier_32b

create_clock -name "clk" -add -period 2.0 -waveform {0.0 1.0} [get_ports clk]

set_clock_gating_check -setup 0.0 
set_input_transition 0.05 [get_ports clk]
set_clock_uncertainty -hold 0.02 [get_ports clk]
set_clock_uncertainty -setup 0.02 [get_ports clk]
 
# optional
# set_false_path -from [list \
  [get_ports clk]  \
  [get_ports en]  \
  [get_ports {a[1]}]  \
  [get_ports {a[0]}]  \
  [get_ports {b[1]}]  \
  [get_ports {b[0]}] ]

# optional 
# set_clock_latency -max 0 [get_pins aa_reg_0_/CLK]
# set_clock_latency -max 0 [get_pins aa_reg_10_/CLK]

#################
