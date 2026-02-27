set_clock_latency -source -early -max -rise  -30.697 [get_ports {clk}] -clock clk 
set_clock_latency -source -early -max -fall  -29.3606 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -rise  -30.697 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -fall  -29.3606 [get_ports {clk}] -clock clk 
