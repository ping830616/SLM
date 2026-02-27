*** SPICE Circuit for Metastability
*** Eduardo Ortega
*******************************
*** MODELS ***
.include '/home/eeortega/Grad-School-Experimentation/ROWHAMMER/RH_SPICE_SIM_WORK/SPICE_MODELS/FINFET/open_road/7nm_TT_160803.pm'
.param vdd=1.0 
.param t=20
.TEMP 't'
.param lambda=10e-9
v_vdd vdd_source gnd vdd
.param init_delay=0.5ps
.param rise_fall=10.01ps
.param freq=4GHz
.param clk_period='1/freq'
.param clk_pulse='clk_period/2'
.param slack_margin_ratio=0.6
.param pulse_margin='1.0-slack_margin_ratio'
.param pulse='clk_period*pulse_margin'
.param margin_safety='clk_period*0.01'
.param delay_logic='clk_period-margin_safety'
.param logic_period='2*clk_period'
***********
.subckt PASS in out power ground en en_bar
m_nmos in en out ground nmos_lvt w='lambda' l='lambda'
m_pmos in en_bar out power pmos_lvt w='lambda*2' l='lambda'
.ends

.subckt INV in out power ground
m_nmos ground in out ground nmos_lvt w='lambda' l='lambda'
m_pmos out in power power pmos_lvt w='lambda*2' l='lambda'
.ends

.subckt DFF d q power ground clk clk_bar
x_inv_1 d 1 power ground INV
x_pass_1 1 2 power ground clk_bar clk PASS
x_inv_2 2 4 power ground INV
x_inv_3 4 3 power ground INV
x_pass_2 3 2 power ground clk clk_bar PASS
x_pass_3 4 5 power ground clk clk_bar PASS
x_pass_4 5 6 power ground clk_bar clk PASS
x_inv_4 5 7 power ground INV
x_inv_5 7 6 power ground INV
x_inv_6 7 q power ground INV
.ends

.subckt BUFFER in out power ground
x_inv_1 in intermediate power ground INV
x_inv_2 intermediate out power ground INV
.ends
***********
* PULSE
v_pulse pulse_source gnd PULSE(0v vdd 'delay_logic' rise_fall rise_fall pulse logic_period)
v_clk clk_PRE gnd PULSE(0v vdd init_delay rise_fall rise_fall clk_pulse clk_period)
x_BUFF_CLK clk_PRE clk vdd_source gnd BUFFER
x_inv_clk clk clk_bar vdd_source gnd INV
***********
x_buff_1 pulse_source d vdd_source gnd BUFFER
x_dff d q vdd_source gnd clk clk_bar DFF

.ic v(d)=0.0 v(q)=0.0

.tran 0.1ps 'clk_period*2' sweep DATA=sweeper_params
.DATA sweeper_params vdd t
1.0 20
1.0 40
1.0 60
1.0 80
1.0 100
1.0 120
0.9 20
0.9 40
0.9 60
0.9 80
0.9 100
0.9 120
0.8 20
0.8 40
0.8 60
0.8 80
0.8 100
0.8 120
0.7 20
0.7 40
0.7 60
0.7 80
0.7 100
0.7 120
.options post
.end

