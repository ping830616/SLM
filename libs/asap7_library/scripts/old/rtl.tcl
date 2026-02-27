 
# disclaimer: All the values given here are just for illustrative purpose##
# Change all the path according to your run directory
#Please go through the file before sourcing it
# Try to run all the command one by one at least for the first time
set_attribute information_level 5 ;

set_attribute lib_search_path {/afs/asu.edu/class/e/e/e/eee525b/asap7_library/setup_files}
set_attribute library {asap7sc7p5t_07_R_160418b.lib}


#set_attribute lp_insert_clock_gating true / ;

set filename "mux2" ;
set modname "multiplexer" ;

#set_attribute optimize_merge_flops true / ;
#set_attribute optimize_merge_latches true / ;
#set_attribute delete_unloaded_insts true / ;
#set_attribute delete_unloaded_seqs true / ;
#set_attribute dp_postmap_downsize true / ;
#set_attribute dp_postmap_upsize true / ;


set_attribute hdl_search_path {/afs/asu.edu/users/x/x/x/athakare/asap7_rundir/lab4/rtl}
read_hdl mux.v

elaborate
check_design

set clock [ define_clock -name clk -period 500 [find /designs/$modname/ports_in -port clk* ] ]

set_attribute max_transition 50 /designs/*


external_delay -input 100 -edge_rise [all_inputs] -clock clk
external_delay -output 100 -edge_rise [all_outputs] -clock clk
set_attribute external_pin_cap 15 /designs/$modname/ports_out/*
path_delay -delay 2 -from clk -to clk

#set_attribute max_dynamic_power 150000 /designs/$modname
#set_attribute max_leakage_power 8500 /designs/$modname
#set_attribute lp_power_analysis high

#set_attribute avoid true [find / -libcell NAND4x04]


synthesize -to_mapped -incremental -effort high

report timing
report timing -slack_limit 0   > timing_slack1.txt
report timing -worst 10 > timing10.txt

report clock_gating > clock_gating.txt

report clock_gating -multi_stage > clock_gating_multi_stage.txt

report clock_gating -detail > clock_gating_detail.txt

report power > power.txt
report area > area.txt



write -mapped > $filename.v


write_hdl > $filename.hdl

write_sdc > $filename.sdc

write_script > script
