source ./Default.globals
init_design

# this is example tcl to make a flexible floorplan size

#set cellheight [expr 0.270 * 4 ]
#set cellhgrid  0.216

#set fpxdim [expr $cellhgrid * 400 ]
#set fpydim [expr $cellheight * 74 ]

#floorPlan -site coreSite -s $fpxdim $fpydim 0 0 0 0
#You might want to change floorplan according to your design
floorPlan -site CoreSite -noSnapToGrid -d 71 71 0 0 0 0

# puts "Floorplan is $fpxdim by $fpydim"
# puts "Total area is [expr $fpxdim * $fpydim ] square um"
# puts "[expr $fpydim / $cellheight] standard cell rows tall"

# Innovus is not putting tracks on the bottom cell row. That causes problems
# since it won't route to them on proper tracks.

# This moves the core up one.
# Weirdly, it moves it up 1.008, but that seems to fix the track issue.
#changeFloorplan -coreToBottom 1.08

add_tracks -honor_pitch 

clearGlobalNets
#global net names are case sensitive.

#globalNetConnect VDD -type pgpin -pin vdd -inst * -module {}
#globalNetConnect VSS -type pgpin -pin vss -inst * -module {}
globalNetConnect VDD -type pgpin -pin VDD -inst * -module {}
globalNetConnect VSS -type pgpin -pin VSS -inst * -module {}

addWellTap -cell TAPCELL_ASAP7_75t_R -cellInterval 150 -inRowOffset 10.564


#####Power Planning 
#Note: You can add power rings: Commands to put power rings are given below in comments.

##Power rings
#addRing -nets {VDD VSS } -around default_power_domain -center 1 -width 1.224 -spacing 0.5 -layer {left M3 right M3 bottom M2 top M2} -extend_corner {lb lt rb rt bl tl br tr}
#saveDesign conv_pool.power.enc

#Sprecial routing using M1
#sroute -connect { blockPin padPin padRing corePin floatingStripe } -nets {VDD VSS } -layerChangeRange { M1 M3 } -blockPinTarget { nearestTarget } -padPinPortConnect { allPort oneGeom } -padPinTarget { nearestTarget } -corePinTarget { firstAfterRowEnd } -floatingStripeTarget { blockring padring ring stripe ringpin blockpin followpin } -allowJogging 1 -crossoverViaLayerRange { M1 Pad } -allowLayerChange 1 -blockPin useLef -targetViaLayerRange { M1 Pad }
#saveDesign conv_pool_specialRoute.enc

setAddStripeMode -stacked_via_bottom_layer M1 \
    -stacked_via_top_layer M2

sroute -connect { blockPin padPin padRing corePin floatingStripe } \
    -layerChangeRange { M1 Pad } \
    -blockPinTarget { nearestTarget } \
    -padPinPortConnect { allPort oneGeom } \
    -padPinTarget { nearestTarget } \
    -corePinTarget { firstAfterRowEnd } \
    -floatingStripeTarget { blockring padring ring stripe ringpin blockpin followpin } \
    -allowJogging 1 \
    -crossoverViaLayerRange { M1 Pad } \
    -nets { VDD VSS } \
    -allowLayerChange 1 \
    -blockPin useLef \
    -targetViaLayerRange { M1 }

### Intervene Here. Manually fix the Top M1 Follow Rail

# setViaGenMode -viarule_preference { M2_M1p }
source "m2followRail.tcl"

setViaGenMode -viarule_preference { M6_M5widePWR1p152 M5_M4widePWR0p864 M4_M3widePWR0p864 }

# ! VALUES BELOW MAY NEED TO BE ADJUSTED FOR HOW innovus INTERPRETS YOUR FLOORPLAN

# has to be 5, 9, 13, ... change the 8 to widen by 4 min widths

set m3pwrwidth [expr 0.072 * (5 + (4 * 2))]
set m3pwrset2settracks  220
set m3pwrset2setdist    [expr $m3pwrset2settracks * 0.144]
print "M3 PWR width, temp and set to set distance: $m3pwrwidth $m3pwrset2settracks $m3pwrset2setdist"

# must be odd multiple of width and space so we get an even number of intervening tracks and stay on grid

set m3pwrspacing [expr 0.072 * 21]

# the xoffset specifies the left edge of the 1st wire.
# since the 1st track is wire (not 1/2 space) now we need an even number (width + space) for xoffset

set m3pwrxoffset [expr (0.072 * 26) + 0.036]
print "M3 PWR spacing and offset: $m3pwrspacing $m3pwrxoffset"

addStripe -extend_to design_boundary \
    -skip_via_on_wire_shape Noshape \
    -max_same_layer_jog_length 0.32 \
    -set_to_set_distance $m3pwrset2setdist \
    -skip_via_on_pin Standardcell \
    -stacked_via_top_layer Pad \
    -spacing $m3pwrspacing \
    -xleft_offset $m3pwrxoffset \
    -merge_stripes_value 0.16 \
    -layer M3 \
    -width $m3pwrwidth \
    -nets {VDD VSS} \
    -stacked_via_bottom_layer M2

set m4pwrwidth [expr 0.096 * (5 + (4 * 1))]
set m4pwrset2settracks  320
set m4pwrset2setdist    [expr $m4pwrset2settracks * 0.192]
print "M4 PWR width, temp and set to set distance: $m4pwrwidth $m4pwrset2settracks $m4pwrset2setdist"

# must be odd multiple of width and space so we get an even number of intervening tracks and stay on grid

set m4pwrspacing [expr 0.096 * 21]

# the xoffset specifies the left edge of the 1st wire.
# since the 1st track is wire (not 1/2 space) now we need an even number (width + space) for xoffset

set m4pwrxoffset [expr (0.096 * 26) - 0.036]
print "M4 PWR spacing and offset: $m4pwrspacing $m4pwrxoffset"

setAddStripeMode \
    -max_via_size { Stripe 100 100 100 } \
    -via_using_exact_crossover_size true \
    -stacked_via_bottom_layer M3 \
    -stacked_via_top_layer M4

addStripe -extend_to design_boundary \
    -direction horizontal \
    -skip_via_on_wire_shape Noshape \
    -max_same_layer_jog_length 0.32 \
    -set_to_set_distance $m4pwrset2setdist \
    -skip_via_on_pin Standardcell \
    -spacing $m4pwrspacing \
    -start_offset $m4pwrxoffset \
    -merge_stripes_value 0.16 \
    -layer M4 \
    -width $m4pwrwidth \
    -nets {VDD VSS}

set m5pwrwidth [expr 0.096 * (5 + (4 * 1))]
set m5pwrset2settracks  320
set m5pwrset2setdist    [expr $m5pwrset2settracks * 0.192]
print "M5 PWR width, temp and set to set distance: $m5pwrwidth $m5pwrset2settracks $m5pwrset2setdist"

# must be odd multiple of width and space so we get an even number of intervening tracks and stay on grid

set m5pwrspacing [expr 0.096 * 21]

# the xoffset specifies the left edge of the 1st wire.
# since the 1st track is wire (not 1/2 space) now we need an even number (width + space) for xoffset

set m5pwrxoffset [expr (0.096 * 70) + 0.024 ]
print "M5 PWR spacing and offset: $m5pwrspacing $m5pwrxoffset"

setAddStripeMode -stacked_via_bottom_layer M4 \
    -stacked_via_top_layer M5

setViaGenMode -bar_cut_orientation horizontal

addStripe -extend_to design_boundary \
    -direction vertical \
    -skip_via_on_wire_shape Noshape \
    -max_same_layer_jog_length 0.32 \
    -set_to_set_distance $m5pwrset2setdist \
    -skip_via_on_pin Standardcell \
    -spacing $m5pwrspacing \
    -start_offset $m5pwrxoffset \
    -merge_stripes_value 0.16 \
    -layer M5 \
    -width $m5pwrwidth \
    -nets {VDD VSS}

set m6pwrwidth [expr 0.128 * (5 + (4 * 1))]
set m6pwrset2settracks  220
set m6pwrset2setdist    [expr $m6pwrset2settracks * 0.256]
print "M6 PWR width, temp and set to set distance: $m6pwrwidth $m6pwrset2settracks $m6pwrset2setdist"

# must be odd multiple of width and space so we get an even number of intervening tracks and stay on grid

set m6pwrspacing [expr 0.128 * 21]

# the xoffset specifies the left edge of the 1st wire.
# since the 1st track is wire (not 1/2 space) now we need an even number (width + space) for xoffset

set m6pwrxoffset [expr (0.128 * 50) + 0.008 ]
print "M6 PWR spacing and offset: $m6pwrspacing $m6pwrxoffset"

setAddStripeMode -stacked_via_bottom_layer M5 \
    -stacked_via_top_layer M6

setViaGenMode -bar_cut_orientation vertical

addStripe -extend_to design_boundary \
    -direction horizontal \
    -skip_via_on_wire_shape Noshape \
    -max_same_layer_jog_length 0.32 \
    -set_to_set_distance $m6pwrset2setdist \
    -skip_via_on_pin Standardcell \
    -spacing $m6pwrspacing \
    -start_offset $m6pwrxoffset \
    -merge_stripes_value 0.16 \
    -layer M6 \
    -width $m6pwrwidth \
    -nets {VDD VSS}

timeDesign -prePlace

createBasicPathGroups

setMaxRouteLayer 6
set_interactive_constraint_modes common
create_clock -name clk  -period 2000 -waveform {0 150} [get_ports clk]
report_clocks
setOptMode -usefulSkew false \
    -allEndPoints true \
    -fixHoldAllowSetupTnsDegrade false 

#placement of pins

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 0 -layer 5 -spreadType side -pin {{inData[0]} {inData[1]} {inData[2]} {inData[3]} {inData[4]} {inData[5]} {inData[6]} {inData[7]} {inData[8]} {inData[9]} {inData[10]} {inData[11]} {inData[12]} {inData[13]} {inData[14]} {inData[15]} {inData[16]} {inData[17]} {inData[18]} {inData[19]} {inData[20]} {inData[21]} {inData[22]} {inData[23]} {inData[24]} {inData[25]} {inData[26]} {inData[27]} {inData[28]} {inData[29]} {inData[30]} {inData[31]}}
setPinAssignMode -pinEditInBatch false

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 2 -layer 6 -spreadType side -pin {{outData[0]} {outData[1]} {outData[2]} {outData[3]} {outData[4]} {outData[5]} {outData[6]} {outData[7]} {outData[8]} {outData[9]} {outData[10]} {outData[11]} {outData[12]} {outData[13]} {outData[14]} {outData[15]} {outData[16]} {outData[17]} {outData[18]} {outData[19]} {outData[20]} {outData[21]} {outData[22]} {outData[23]} {outData[24]} {outData[25]} {outData[26]} {outData[27]} {outData[28]} {outData[29]} {outData[30]} {outData[31]}}
setPinAssignMode -pinEditInBatch false

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 3 -layer 4 -spreadType side -pin {reset}
setPinAssignMode -pinEditInBatch false

getPinAssignMode -pinEditInBatch -quiet
setPinAssignMode -pinEditInBatch true
editPin -fixedPin 1 -fixOverlap 1 -spreadDirection clockwise -edge 1 -layer 6 -spreadType side -pin {clk}
setPinAssignMode -pinEditInBatch false

saveDesign fir_pins.enc

# placement pre-clock cts goes here... place your standard cells
#### Place Design
setPlaceMode -place_global_timing_effort medium
setPlaceMode -place_global_reorder_scan false
setPlaceMode -place_global_cong_effort low
place_opt_design

# CTS

setNanoRouteMode -drouteMinimizeLithoEffectOnLayer {f t t t t t t t t t} \
    -routeTopRoutingLayer 6 -routeBottomRoutingLayer 2 \
    -routeWithViaInPin true 

# set desired clock cells here...
set_ccopt_property buffer_cells {BUFx10_ASAP7_75t_R BUFx12_ASAP7_75t_R BUFx12f_ASAP7_75t_R BUFx16f_ASAP7_75t_R BUFx24_ASAP7_75t_R BUFx2_ASAP7_75t_R BUFx3_ASAP7_75t_R BUFx4_ASAP7_75t_R BUFx5_ASAP7_75t_R BUFx4f_ASAP7_75t_R BUFx6f_ASAP7_75t_R BUFx8_ASAP7_75t_R HB1xp67_ASAP7_75t_R HB2xp67_ASAP7_75t_R}

#set_ccopt_property inverter_cells {INVx11_ASAP7_75t_R INVx13_ASAP7_75t_R INVx1_ASAP7_75t_R INVx2_ASAP7_75t_R INVx3_ASAP7_75t_R INVx4_ASAP7_75t_R INVx5_ASAP7_75t_R INVx6_ASAP7_75t_R INVx8_ASAP7_75t_R INVxp67_ASAP7_75t_R INVxp33_ASAP7_75t_R}

#set_ccopt_property target_skew 5ps 
#set_ccopt_property target_max_trans 30ps
#setNanoRouteMode -routeTopRoutingLayer 5 -routeBottomRoutingLayer 2
#create_route_type -name ccopt_route_group -bottom_preferred_layer 4 -top_preferred_layer 5
#create_ccopt_clock_tree_spec
#ccopt_design -cts

set_ccopt_property cts_add_wire_delay_in_detailed_balancer true
set_ccopt_property cts_compute_fastest_drivers_and_slews_for_clustering multi_corner
set_ccopt_property cts_clustering_net_skew_limit_as_proportion_of_skew_target 0.5
set_ccopt_property routing_top_min_fanout 2000
set_ccopt_property cell_density 0.5
set_ccopt_property adjacent_rows_legal false
set_ccopt_property ccopt_auto_limit_insertion_delay_factor 1.0
set_ccopt_property skew_band_size 0.1
set_ccopt_property useful_skew_use_gigaopt_for_mfn_chain_speed true
set_ccopt_property useful_skew_implement_using_wns_windows false
set_ccopt_property target_max_trans  100ps


# Create CTS specification
create_ccopt_clock_tree_spec -filename ./cts/ccopt.spec
source ./cts/ccopt.spec
    
# Run CCopt
ccopt_design -outDir ./cts/
    
# Report timing
timeDesign -postCTS -expandedViews -outDir ./cts/timing/
    
# Report clock trees to check area and other statistics
report_ccopt_clock_trees -filename ./cts/clock_trees.rpt
report_ccopt_skew_groups -filename ./cts/skew_groups.rpt

#Post CTS
optDesign -postCTS
optDesign -postCTS -hold
saveDesign fir_post_cts.enc

#Nano routing
setNanoRouteMode -drouteMinimizeLithoEffectOnLayer {t t t t t t t t t t}
setNanoRouteMode -routeWithViaInPin true -routeDesignFixClockNets true -routeTopRoutingLayer 6
setNanoRouteMode -quiet -drouteFixAntenna 0
setNanoRouteMode -quiet -routeWithTimingDriven 1
setNanoRouteMode -quiet -drouteEndIteration default
setNanoRouteMode -quiet -routeWithTimingDriven true
setNanoRouteMode -quiet -routeWithSiDriven false
routeDesign 

# all done--finish up with decap and finally filler

addFiller -cell {FILLER_ASAP7_75t_R FILLERxp5_ASAP7_75t_R } -prefix FILLER_

#Verify Geometry & Connectivity
verify_drc
verifyGeometry  -error 1000000 -warning 50
verifyConnectivity -type all -noAntenna -error 1000000 -warning 50

#Save final Design
saveNetlist aes_128.apr.v
saveNetlist aes_128.apr_pg.v -includePowerGround -excludeLeafCell
saveDesign fir_final.enc

##StreamOutGds

rcOut -spf FIR_filter.spf
rcOut -spef FIR_filter.spef
saveNetlist FIR_filter.apr.v -excludeLeafCell -excludeCellInst {FILLERxp5_ASAP7_75t_R FILLER_ASAP7_75t_R}
saveNetlist FIR_filter.apr_pg.v -includePowerGround -excludeLeafCell -excludeCellInst {FILLERxp5_ASAP7_75t_R FILLER_ASAP7_75t_R}
streamOut FIR_filter.gds -mapFile /home/aavyas1/libs/asap7/asap7PDK/cdslib/asap7_TechLib/asap7_fromAPR.layermap -libName DesignLib -units 4000 -mode ALL
summaryReport
setAnalysisMode -analysisType onchipvariation
saveDesign FIR_filter.enc

