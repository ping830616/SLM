set_clock_latency -source -early -max -rise  -19.3 [get_ports {clk}] -clock clk 
set_clock_latency -source -early -max -fall  -17.9176 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -rise  -19.3 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -fall  -17.9176 [get_ports {clk}] -clock clk 
