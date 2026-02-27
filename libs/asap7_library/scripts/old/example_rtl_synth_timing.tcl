#Make sure you know the meaning of each attribute/constraint. This will help you in meeting design goal.


#Define clock
define_clock -name clk -period 2000 [find designs/$modname/ports_in -port clk ] ;


set_attribute fixed_slew 100 clk;
set_attribute max_transition 100 /designs/* ;
set_attribute max_fanout 32 /designs/* ;
set_attribute tns_opto false ;

#List the external delay of your inputs with respect to the clock edge.
external_delay -input 200 -edge_rise [find designs/$modname/ports_in -port reset_b] -clock clk ;
external_delay -input 600 -edge_rise [find designs/$modname/ports_in -port a*] -clock clk ;

set_attribute clock_hold_uncertainty 50 clk ;
set_attribute clock_setup_uncertainty 50 clk ;

set_attribute external_pin_cap 50 /designs/$modname/ports_out/* ;


# Some attributes for power (note weird units)
set_attribute max_dynamic_power 1000000 /designs/$modname
set_attribute max_leakage_power 100000 /designs/$modname
set_attribute lp_power_analysis high

# Defined gates that you don't want to use, *example* command is as follows. This will be useful as we move ahead in the project and throw out the bad designs.
# set_attribute avoid true /libraries/*/libcells/INVCLK04*

#Synthesis command. For incremental synthesis, use synthesize -to_mapped -incremental -effort <low/medium/high>
synth -to_mapped -effort medium;

report clock_gating -detail -multi_stage > clock_gating1.txt ;
report timing > timing.txt;
report timing -worst 10 >> worsttiming.txt;
report power > power.txt

#For reporting clock gating instances, use following commands
#report instance [find /designs/$modname/*/instances_seq -instance RC_CG*INST* ]
#report instance [find /designs/$modname/instances_seq -instance RC_CG*INST* ]

#After synthesis generate following files for encounter
#Save the structural verilog
write -mapped > $filename.synth.v
# Write the design out for encounter. This generates an entire directory of information
write_design -encounter
write_hdl > $filename.synth.hdl
write_sdc > $filename.synth.sdc # timing file

