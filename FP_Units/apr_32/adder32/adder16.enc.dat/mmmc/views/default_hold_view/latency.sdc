set_clock_latency -source -early -max -rise  -30.1515 [get_ports {clk}] -clock clk 
set_clock_latency -source -early -max -fall  -28.9182 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -rise  -30.1515 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -fall  -28.9182 [get_ports {clk}] -clock clk 
