set_clock_latency -source -early -max -rise  -15.6176 [get_ports {clk}] -clock clk 
set_clock_latency -source -early -max -fall  -14.0118 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -rise  -15.6176 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -fall  -14.0118 [get_ports {clk}] -clock clk 
