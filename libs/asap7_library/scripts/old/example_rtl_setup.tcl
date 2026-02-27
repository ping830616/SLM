###########################################################################
# Include in your .cshrc file :
# set path = (/usr/local/cadence/edi91/bin $path)
# set path = (/usr/local/synopsys/ptD-2009. 12-SP1/bin $path)
# 
# Invoke with:
# rc -gui
# Do NOT put it in the background with '&'
# It is a good idea to have another window open to the same directory
# Commands go into the shell (non-graphical window)
# I prefer to cut/paste them from a script like this one to run the tool
# That way, when they are correct, I have the correct thing saved 
# Don't be afraid to exit out and start over, tool is pretty fast
###########################################################################

# For info about attributes type "rc:/> get_attribute attribute_name * -help"
# You can get a list of all the available attributes by typing the following command: "rc:/> get_attribute * * -h"

#Controls the amount of info that RC throws up during running.
set_attribute information_level 5 ;

#Timing library search path and name
set_attribute lib_search_path {<absolute path of your lib files> }; 
set_attribute library {<name of the lib file>};

#Name of Verilog file containing top level module definition and its name. These are just variables
set filename "MYDESIGN" ;
set modname "MYDESIGN" ;

#Set use of clock gating attribute to yes.
set_attribute lp_insert_clock_gating true / ;

#Some attributes whose definition can be found in user guide
set_attribute optimize_merge_flops true / ;
set_attribute optimize_merge_latches true / ;
set_attribute delete_unloaded_insts true / ;
set_attribute delete_unloaded_seqs true / ;
set_attribute dp_postmap_downsize true / ;
set_attribute dp_postmap_upsize true / ;

#Verilog files search path
set_attribute hdl_search_path { /afs/asu.edu/users/x/x/x/xxx/525/xxx/verilog } ;

#Name of verilog files required
read_hdl $filename.v file2.v file3.v

# Compiles the design. Now it exists, so you can set timings, etc.
# Read the log files! This is where latch inference happens (good to know what worked and what didn't)
elaborate ;

#Now you navigate like in Unix, but through your design
# The design hierarchy can be a bit confusing, so use this to look through it and get commands right
# For instance "ls designs" prints out the current designs like files in Unix
