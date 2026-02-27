*** SPICE Circuit for RowHammer
*** Eduardo Ortega
*******************************
*** MODELS ***
.include '/home/eeortega/Grad-School-Experimentation/ROWHAMMER/RH_SPICE_SIM_WORK/SPICE_MODELS/FINFET/open_road/7nm_TT_160803.pm'
.PARAM vdd=GAUSS(1.0, 0.05)
.PARAM vth=0.5
.param lambda=100e-9
v_vdd vdd gnd vdd
.param init_delay=1.01ps
.param rise_fall=10.01ps
.param PWM=0.1
.param period=500.01ns
.param pulse_width='period*PWM'
.param c_load=20fF
* TSV PARAMS
.param r_0=GAUSS(63e-3, 0.05)
.param r_1=GAUSS(38e-3, 0.05)
.param r_si=GAUSS(1.4e3,0.05)
.param r_dep=GAUSS(124,0.05)
.param c_ox=GAUSS(122fF, 0.05)
.param c_si=GAUSS(7fF, 0.05)
.param c_dep=GAUSS(78fF,0.05)
.param l_0=GAUSS(14pH,0.05)
.param l_1=GAUSS(5pH,0.05)
***********

.subckt INV in out power ground
m_nmos ground in out ground nmos_lvt w='lambda' l='lambda'
m_pmos out in power power pmos_lvt w='lambda*2' l='lambda'
.ends

.subckt BUFFER in out power ground
x_inv_1 in intermediate power ground INV
x_inv_2 intermediate out power ground INV
.ends

.subckt TSV in out ground
r_r1 in a r_1
r_r0 in b r_0
l_l1 a b l_1
c_cox in c c_ox
r_rdep c d r_dep
c_cdep c d c_dep
r_rsi d ground r_si
c_csi d ground c_si
l_l0 b e l_0
l_l1_1 e f l_1
r_r1_1 f out r_1
r_r0_1 e out r_0
c_cox_1 e g c_ox
r_rdep_1 g h r_dep
c_cdep_1 g h c_dep
r_rsi_1 h ground r_si
c_rsi_1 h ground c_si
.ends

*x_buff pulse_source driver vdd gnd BUFFER
x_inv_1 out stage_a vdd gnd INV
x_tsv_1_1 stage_a stage_b gnd TSV
x_tsv_1_2 stage_a stage_b gnd TSV
x_tsv_1_3 stage_a stage_b gnd TSV
x_tsv_1_4 stage_a stage_b gnd TSV
x_tsv_1_5 stage_a stage_b gnd TSV
x_tsv_1_6 stage_a stage_b gnd TSV
x_tsv_1_7 stage_a stage_b gnd TSV
x_tsv_1_8 stage_a stage_b gnd TSV
x_tsv_1_9 stage_a stage_b gnd TSV
x_inv_2 stage_b stage_c vdd gnd INV
x_tsv_2_1 stage_c stage_d gnd TSV
x_tsv_2_2 stage_c stage_d gnd TSV
x_tsv_2_3 stage_c stage_d gnd TSV
x_tsv_2_4 stage_c stage_d gnd TSV
x_tsv_2_5 stage_c stage_d gnd TSV
x_tsv_2_6 stage_c stage_d gnd TSV
x_tsv_2_7 stage_c stage_d gnd TSV
x_tsv_2_8 stage_c stage_d gnd TSV
x_tsv_2_9 stage_c stage_d gnd TSV
x_inv_3 stage_d out vdd gnd INV
c_cload out gnd c_load

.ic v(out)=0.0v v(stage_a)=1.0v v(stage_b)=1.0v v(stage_c)=0.0v v(stage_d)=0.0v

.tran 1.01ps 300.01ns sweep monte=100
.options post
.end

