source Default.globals
##set init_io_file padframe.io
init_design

floorPlan -d 50 50 20 20 20 20 

#addIoFiller -cell pfeed10000 -prefix FILLER -side n
#addIoFiller -cell pfeed10000 -prefix FILLER -side e
#addIoFiller -cell pfeed10000 -prefix FILLER -side w
#addIoFiller -cell pfeed10000 -prefix FILLER -side s

globalNetConnect VDD -type pgpin -pin VDD -inst * -module {}
globalNetConnect VSS -type pgpin -pin VSS -inst * -module {}


addWellTap -cell TAPCELL_ASAP7_75t_R -cellInterval 60 -inRowOffset 2 -prefix WELLTAP


addRing -skip_via_on_wire_shape Noshape -exclude_selected 1 -skip_via_on_pin Standardcell -center 1 -stacked_via_top_layer M6 -type core_rings -jog_distance 0.56 -threshold 0.56 -nets {VDD VSS} -follow core -stacked_via_bottom_layer M1 -layer {left M6 right M6 bottom M3 top M3} -width 6 -spacing 2 -offset 2

#addRing -nets {VDD VSS } -around default_power_domain -center 1 -width 1.224 -spacing 0.5 -layer {left M6 right M6 bottom M3 top M3} -extend_corner {lb lt rb rt bl tl br tr}

sroute -connect { blockPin padPin padRing corePin floatingStripe } -nets {VDD VSS } -layerChangeRange { M1 M6 } -blockPinTarget { nearestTarget } -padPinPortConnect { allPort oneGeom } -padPinTarget { nearestTarget } -corePinTarget { firstAfterRowEnd } -floatingStripeTarget { blockring padring ring stripe ringpin blockpin followpin } -allowJogging 1 -crossoverViaLayerRange { M1 M6 } -allowLayerChange 1 -blockPin useLef -targetViaLayerRange { M1 M6 }


getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 0 -layer 5 -spreadType side -pin {{a[0]} {a[1]}}
setPinAssignMode -pinEditInBatch false

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 2 -layer 6 -spreadType side -pin {{sum[0]} {sum[1]} cout}
setPinAssignMode -pinEditInBatch false

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 3 -layer 4 -spreadType side -pin {clk}
setPinAssignMode -pinEditInBatch false

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 1 -layer 6 -spreadType side -pin {{b[0]} {b[1]}}
setPinAssignMode -pinEditInBatch false

saveDesign adder_pins.enc

#setRouteMode -earlyGlobalMaxRouteLayer 6 -earlyGlobalMinRouteLayer 1 -earlyGlobalHonorClockSpecNDR true

# getPinAssignMode -pinEditInBatch -quiet
# setPinAssignMode -pinEditInBatch true
#editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 2 -layer 7 -spreadType side -pin {out_valid out0[*]} -skipWrappingPins -offsetEnd 6 -offsetStart 6
# editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 3 -layer 6 -spreadType side -pin {clk rst start {key[64]} {key[65]} {key[66]} {key[67]} {key[68]} {key[69]} {key[70]} {key[71]} {key[72]} {key[73]} {key[74]} {key[75]} {key[76]} {key[77]} {key[78]} {key[79]} {key[80]} {key[81]} {key[82]} {key[83]} {key[84]} {key[85]} {key[86]} {key[87]} {key[88]} {key[89]} {key[90]} {key[91]} {key[92]} {key[93]} {key[94]} {key[95]} {key[96]} {key[97]} {key[98]} {key[99]} {key[100]} {key[101]} {key[102]} {key[103]} {key[104]} {key[105]} {key[106]} {key[107]} {key[108]} {key[109]} {key[110]} {key[111]} {key[112]} {key[113]} {key[114]} {key[115]} {key[116]} {key[117]} {key[118]} {key[119]} {key[120]} {key[121]} {key[122]} {key[123]} {key[124]} {key[125]} {key[126]} {key[127]} {state[65]} {state[66]} {state[67]} {state[68]} {state[69]} {state[70]} {state[71]} {state[72]} {state[73]} {state[74]} {state[75]} {state[76]} {state[77]} {state[78]} {state[79]} {state[80]} {state[81]} {state[82]} {state[83]} {state[84]} {state[85]} {state[86]} {state[87]} {state[88]} {state[89]} {state[90]} {state[91]} {state[92]} {state[93]} {state[94]} {state[95]} {state[96]} {state[97]} {state[98]} {state[99]} {state[100]} {state[101]} {state[102]} {state[103]} {state[104]} {state[105]} {state[106]} {state[107]} {state[108]} {state[109]} {state[110]} {state[111]} {state[112]} {state[113]} {state[114]} {state[115]} {state[116]} {state[117]} {state[118]} {state[119]} {state[120]} {state[121]} {state[122]} {state[123]} {state[124]} {state[125]} {state[126]} {state[127]}} -skipWrappingPins -offsetEnd 6 -offsetStart 6
# editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 1 -layer 5 -spreadType side -pin {{key[0]} {key[1]} {key[2]} {key[3]} {key[4]} {key[5]} {key[6]} {key[7]} {key[8]} {key[9]} {key[10]} {key[11]} {key[12]} {key[13]} {key[14]} {key[15]} {key[16]} {key[17]} {key[18]} {key[19]} {key[20]} {key[21]} {key[22]} {key[23]} {key[24]} {key[25]} {key[26]} {key[27]} {key[28]} {key[29]} {key[30]} {key[31]} {key[32]} {key[33]} {key[34]} {key[35]} {key[36]} {key[37]} {key[38]} {key[39]} {key[40]} {key[41]} {key[42]} {key[43]} {key[44]} {key[45]} {key[46]} {key[47]} {key[48]} {key[49]} {key[50]} {key[51]} {key[52]} {key[53]} {key[54]} {key[55]} {key[56]} {key[57]} {key[58]} {key[59]} {key[60]} {key[61]} {key[62]} {key[63]}} -skipWrappingPins -offsetEnd 6 -offsetStart 6
# editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 0 -layer 4 -spreadType side -pin {{state[0]} {state[1]} {state[2]} {state[3]} {state[4]} {state[5]} {state[6]} {state[7]} {state[8]} {state[9]} {state[10]} {state[11]} {state[12]} {state[13]} {state[14]} {state[15]} {state[16]} {state[17]} {state[18]} {state[19]} {state[20]} {state[21]} {state[22]} {state[23]} {state[24]} {state[25]} {state[26]} {state[27]} {state[28]} {state[29]} {state[30]} {state[31]} {state[32]} {state[33]} {state[34]} {state[35]} {state[36]} {state[37]} {state[38]} {state[39]} {state[40]} {state[41]} {state[42]} {state[43]} {state[44]} {state[45]} {state[46]} {state[47]} {state[48]} {state[49]} {state[50]} {state[51]} {state[52]} {state[53]} {state[54]} {state[55]} {state[56]} {state[57]} {state[58]} {state[59]} {state[60]} {state[61]} {state[62]} {state[63]} {state[64]}} -skipWrappingPins -offsetEnd 6 -offsetStart 6


setOptMode -usefulSkew false -allEndPoints true -fixHoldAllowSetupTnsDegrade false
setPlaceMode -place_global_timing_effort medium
setPlaceMode -place_global_reorder_scan false
setPlaceMode -place_global_cong_effort low
setDontUse BUFx16f_ASAP7_75t_R true
setPlaceMode -place_detail_check_route true
setPlaceMode -place_global_timing_effort medium
setPlaceMode -place_global_reorder_scan true -place_detail_check_inst_space_group true
setPlaceMode -place_global_cong_effort auto -place_detail_check_cut_spacing true -place_detail_check_inst_space_group true -place_detail_color_aware_legal true -place_detail_legalization_inst_gap 2 -place_global_auto_blockage_in_channel partial -place_global_uniform_density true -place_global_place_io_pins true
place_opt_design
saveDesign adder_place.enc


setOptMode -fixCap true -fixTran true -fixFanoutLoad true
optDesign -preCTS
saveDesign adder_prects.enc


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
create_ccopt_clock_tree -name gcn_clk -source clk -no_skew_group
set_ccopt_property target_max_trans_sdc -delay_corner delayCorner_slow -early -clock_tree gcn_clk 0.1
set_ccopt_property target_max_trans_sdc -delay_corner delayCorner_slow -late -clock_tree gcn_clk 0.1
set_ccopt_property clock_period -pin clk 1200
create_ccopt_skew_group -name gcn_clk/common -sources clk -auto_sinks
set_ccopt_property include_source_latency -skew_group gcn_clk/common true
set_ccopt_property extracted_from_clock_name -skew_group gcn_clk/common gcn_clk
set_ccopt_property extracted_from_constraint_mode_name -skew_group gcn_clk/common common
set_ccopt_property extracted_from_delay_corners -skew_group gcn_clk/common {delayCorner_slow delayCorner_fast}
check_ccopt_clock_tree_convergence
get_ccopt_property auto_design_state_for_ilms
setDontUse BUFx16f_ASAP7_75t_R true
ccopt_design -outDir ./cts/
saveDesign adder_cts.enc


timeDesign -postCTS -expandedViews -outDir ./cts/timing/

report_ccopt_clock_trees -filename ./cts/clock_trees.rpt
report_ccopt_skew_groups -filename ./cts/skew_groups.rpt

setDontUse BUFx16f_ASAP7_75t_R true

saveDesign adder.cts.enc


optDesign -postCTS
optDesign -postCTS -hold
saveDesign addepostcts.enc


setDontUse BUFx16f_ASAP7_75t_R true
setNanoRouteMode -drouteMinimizeLithoEffectOnLayer {t t t t t t t t t t} -routeTopRoutingLayer 6 -routeWithViaInPin true -routeDesignFixClockNets true
setNanoRouteMode -quiet -drouteFixAntenna 0
setNanoRouteMode -quiet -routeWithTimingDriven 1
setNanoRouteMode -quiet -drouteEndIteration default
setNanoRouteMode -quiet -routeWithTimingDriven true
setNanoRouteMode -quiet -routeWithSiDriven false
routeDesign -globalDetail
saveDesign adder.route.enc


setAnalysisMode -analysisType onchipvariation
optDesign -postroute
saveDesign adder_post_route.enc

report_timing -late -max_path 3 > adder.apr_wc3_timing.txt
report_timing -early -max_path 3 > adder.apr_bc3_timing.txt

addFiller -cell {FILLER_ASAP7_75t_R FILLERxp5_ASAP7_75t_R } -prefix FILLER_
saveDesign adder.filler.enc

verifyConnectivity
verify_drc

rcOut -spf adder.spf
rcOut -spef adder.spef
saveNetlist adder.apr.v -excludeLeafCell -excludeCellInst {FILLERxp5_ASAP7_75t_R FILLER_ASAP7_75t_R}
saveNetlist aadder.apr_pg.v -includePowerGround -excludeLeafCell -excludeCellInst {FILLERxp5_ASAP7_75t_R FILLER_ASAP7_75t_R}
streamOut adder.gds -mapFile /home/aavyas1/libs/asap7/asap7PDK/cdslib/asap7_TechLib/asap7_fromAPR.layermap -libName DesignLib -units 4000 -mode ALL
summaryReport
setAnalysisMode -analysisType onchipvariation
saveDesign adder.enc

#saveNetlist gcn.apr.v -excludeLeafCell -excludeCellInst {FILLERxp5_ASAP7_75t_R FILLER_ASAP7_75t_R}
#saveNetlist gcn.apr_pg.v -includePowerGround -excludeLeafCell -excludeCellInst {FILLERxp5_ASAP7_75t_R FILLER_ASAP7_75t_R}


##streamOut outputs/gcn.gds -mapFile /afs/asu.edu/class/e/e/e/eee525b/asap7/asap7PDK/cdslib/asap7_TechLib/asap7_fromAPR.layermap -libName DesignLib -units 4000 -mode ALL
