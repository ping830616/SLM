set_clock_latency -source -early -max -rise  -32.5606 [get_ports {clk}] -clock clk 
set_clock_latency -source -early -max -fall  -31.4455 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -rise  -32.5606 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -fall  -31.4455 [get_ports {clk}] -clock clk 
