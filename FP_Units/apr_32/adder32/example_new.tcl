source Default.globals
init_design

#floorPlan -d 180 180 20 20 20 20 
floorPlan -r 1 0.7 20 20 20 20

globalNetConnect VDD -type pgpin -pin VDD -inst * -module {}
globalNetConnect VSS -type pgpin -pin VSS -inst * -module {}


addWellTap -cell TAPCELL_ASAP7_75t_R -cellInterval 60 -inRowOffset 2 -prefix WELLTAP


addRing -skip_via_on_wire_shape Noshape -exclude_selected 1 -skip_via_on_pin Standardcell -center 1 -stacked_via_top_layer M3 -type core_rings -jog_distance 0.56 -threshold 0.56 -nets {VDD VSS} -follow core -stacked_via_bottom_layer M1 -layer {left M3 right M3 bottom M2 top M2} -width 6 -spacing 2 -offset 2

sroute -connect { blockPin padPin padRing corePin floatingStripe } -nets {VDD VSS } -layerChangeRange { M1 M3 } -blockPinTarget { nearestTarget } -padPinPortConnect { allPort oneGeom } -padPinTarget { nearestTarget } -corePinTarget { firstAfterRowEnd } -floatingStripeTarget { blockring padring ring stripe ringpin blockpin followpin } -allowJogging 1 -crossoverViaLayerRange { M1 M3 } -allowLayerChange 1 -blockPin useLef -targetViaLayerRange { M1 M3 }


getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 0 -layer 2 -spreadType side -pin {   {b[0]} {b[1]} {b[2]} {b[3]} {b[4]} {b[5]} {b[6]} {b[7]} {b[8]} {b[9]} {b[10]} {b[11]} {b[12]} {b[13]} {b[14]} {b[15]} {b[16]} {b[17]} {b[18]} {b[19]} {b[20]} {b[21]} {b[22]} {b[23]} {b[24]} {b[25]} {b[26]} {b[27]} {b[28]} {b[29]} {b[30]} {b[31]}}
setPinAssignMode -pinEditInBatch false

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 2 -layer 2 -spreadType side -pin {  {a[0]} {a[1]} {a[2]} {a[3]} {a[4]} {a[5]} {a[6]} {a[7]} {a[8]} {a[9]} {a[10]} {a[11]} {a[12]} {a[13]} {a[14]} {a[15]} {a[16]} {a[17]} {a[18]} {a[19]} {a[20]} {a[21]} {a[22]} {a[23]} {a[24]} {a[25]} {a[26]} {a[27]} {a[28]} {a[29]} {a[30]} {a[31]} }
setPinAssignMode -pinEditInBatch false

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 3 -layer 3 -spreadType side -pin {   {z[0]} {z[1]} {z[2]} {z[3]} {z[4]} {z[5]} {z[6]} {z[7]} {z[8]} {z[9]} {z[10]} {z[11]} {z[12]} {z[13]} {z[14]} {z[15]} {z[16]} {z[17]} {z[18]} {z[19]} {z[20]} {z[21]} {z[22]} {z[23]} {z[24]} {z[25]} {z[26]} {z[27]} {z[28]} {z[29]} {z[30]} {z[31]} }
setPinAssignMode -pinEditInBatch false

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 1 -layer 3 -spreadType side -pin {clk rst en output_ready}
setPinAssignMode -pinEditInBatch false

saveDesign adder16.enc

### Placement of Standard Cells.....without any optimization......
setPlaceMode -fp false
placeDesign -noPrePlaceOpt
saveDesign adder16.place.enc




setNanoRouteMode -drouteMinimizeLithoEffectOnLayer {f t t t t t t t t t} -routeTopRoutingLayer 3 -routeBottomRoutingLayer 1 -routeWithViaInPin true
set_ccopt_property buffer_cells {BUFx10_ASAP7_75t_R BUFx12_ASAP7_75t_R BUFx12f_ASAP7_75t_R BUFx24_ASAP7_75t_R BUFx2_ASAP7_75t_R BUFx3_ASAP7_75t_R BUFx4_ASAP7_75t_R BUFx5_ASAP7_75t_R BUFx4f_ASAP7_75t_R BUFx6f_ASAP7_75t_R BUFx8_ASAP7_75t_R HB1xp67_ASAP7_75t_R HB2xp67_ASAP7_75t_R}
set_ccopt_property cts_add_wire_delay_in_detailed_balancer true
set_ccopt_property cts_compute_fastest_drivers_and_slews_for_clustering multi_corner
set_ccopt_property cts_clustering_net_skew_limit_as_proportion_of_skew_target 0.5
set_ccopt_property routing_top_min_fanout 2000
set_ccopt_property cell_density 0.3
set_ccopt_property adjacent_rows_legal false
set_ccopt_property ccopt_auto_limit_insertion_delay_factor 1.0
set_ccopt_property skew_band_size 0.1
set_ccopt_property useful_skew_use_gigaopt_for_mfn_chain_speed true
set_ccopt_property useful_skew_implement_using_wns_windows false
set_ccopt_property target_max_trans 100ps
setDontUse BUFx16f_ASAP7_75t_R true
create_ccopt_clock_tree_spec -filename ./cts/ccopt.spec
ccopt_check_and_flatten_ilms_no_restore
create_ccopt_clock_tree -name adder16_clk -source clk -no_skew_group
set_ccopt_property target_max_trans_sdc -delay_corner delayCorner_slow -early -clock_tree adder16_clk 0.1
set_ccopt_property target_max_trans_sdc -delay_corner delayCorner_slow -late -clock_tree adder16_clk 0.1
set_ccopt_property clock_period -pin clk 2000
create_ccopt_skew_group -name adder16_clk/common -sources clk -auto_sinks
set_ccopt_property include_source_latency -skew_group adder16_clk/common true
set_ccopt_property extracted_from_clock_name -skew_group adder16_clk/common adder16_clk
set_ccopt_property extracted_from_constraint_mode_name -skew_group adder16_clk/common common
set_ccopt_property extracted_from_delay_corners -skew_group adder16_clk/common {delayCorner_slow delayCorner_fast}
check_ccopt_clock_tree_convergence
get_ccopt_property auto_design_state_for_ilms
setDontUse BUFx16f_ASAP7_75t_R true
ccopt_design -outDir ./cts/
saveDesign adder16.cts.enc


timeDesign -postCTS -expandedViews -outDir ./cts/timing/

report_ccopt_clock_trees -filename ./cts/clock_trees.rpt
report_ccopt_skew_groups -filename ./cts/skew_groups.rpt

setDontUse BUFx16f_ASAP7_75t_R true

saveDesign adder16.cts.enc



setDontUse BUFx16f_ASAP7_75t_R true
setNanoRouteMode -drouteMinimizeLithoEffectOnLayer {t t t t t t t t t t} -routeTopRoutingLayer 3 -routeWithViaInPin true -routeDesignFixClockNets true
setNanoRouteMode -quiet -drouteFixAntenna 0
setNanoRouteMode -quiet -routeWithTimingDriven 1
setNanoRouteMode -quiet -drouteEndIteration default
setNanoRouteMode -quiet -routeWithTimingDriven true
setNanoRouteMode -quiet -routeWithSiDriven false
routeDesign -globalDetail
saveDesign adder16.route.enc


report_timing -late -max_path 100 > adder16.apr_wc100_timing.txt
report_timing -early -max_path 100 > adder16.apr_bc100_timing.txt

addFiller -cell {FILLER_ASAP7_75t_R FILLERxp5_ASAP7_75t_R } -prefix FILLER_
saveDesign adder16.filler.enc

verifyConnectivity
#verify_drc

extractRC
rcOut -spf adder16.spf
rcOut -spef adder16.spef.gz
defOut  -floorplan -netlist adder16.def
saveNetlist adder16.apr.v -excludeLeafCell -excludeCellInst {FILLERxp5_ASAP7_75t_R FILLER_ASAP7_75t_R}
saveNetlist adder16.apr_pg.v -includePowerGround -excludeLeafCell -excludeCellInst {FILLERxp5_ASAP7_75t_R FILLER_ASAP7_75t_R}
streamOut adder16.gds -mapFile /home/aavyas1/libs/asap7/asap7PDK/cdslib/asap7_TechLib/asap7_fromAPR.layermap -libName DesignLib -units 4000 -mode ALL

setAnalysisMode -analysisType onchipvariation
saveDesign adder16.enc

