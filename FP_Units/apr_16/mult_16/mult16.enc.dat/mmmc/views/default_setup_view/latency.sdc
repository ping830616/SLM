set_clock_latency -source -early -max -rise  -17.5765 [get_ports {clk}] -clock clk 
set_clock_latency -source -early -max -fall  -15.6941 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -rise  -17.5765 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -fall  -15.6941 [get_ports {clk}] -clock clk 
