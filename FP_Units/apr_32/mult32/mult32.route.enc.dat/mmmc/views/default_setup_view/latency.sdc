set_clock_latency -source -early -max -rise  -32.9091 [get_ports {clk}] -clock clk 
set_clock_latency -source -early -max -fall  -31.9788 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -rise  -32.9091 [get_ports {clk}] -clock clk 
set_clock_latency -source -late -max -fall  -31.9788 [get_ports {clk}] -clock clk 
