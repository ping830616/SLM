####################################
# ASU EEE525 Fall 2017
# Encounter Basic Script for version 14
####################################

puts "####################"
puts "###"
puts "### Init Design ..."
puts "###"
puts "####################"
set top_level adder_2bit
# Use your Default.globals here
source ./Default.globals
init_design

puts "####################"
puts "###"
puts "### Floor Plan ..."
puts "###"
puts "####################"
# floorPlan  -r 1 0.3 3.8 3.8 3.8 3.8 use this floor plan if you are using power rings
floorPlan  -r 1 0.3 0 0 0 0
saveDesign ${top_level}.fp.enc

puts "####################"
puts "###"
puts "### Power Planning ..."
puts "###"
puts "####################"
globalNetConnect vdd -type tiehi -inst * -verbose
globalNetConnect vss -type tielo -inst * -verbose
# addRing (Optional), use command man addRing for more details
#addRing -nets {vss vdd } -around default_power_domain -center 1 \
#	-width 1.1 \
#	-spacing 0.5 \
#	-layer {left M2 right M2 bottom M1 top M1} \
#	-extend_corner {lb lt rb rt bl tl br tr}
#add power stripes
addStripe -skip_via_on_wire_shape Noshape -block_ring_top_layer_limit M4 -max_same_layer_jog_length 0.32 -padcore_ring_bottom_layer_limit M2 -set_to_set_distance 7.6 -skip_via_on_pin Standardcell -stacked_via_top_layer Pad -padcore_ring_top_layer_limit M4 -spacing 0.072 -xleft_offset 2 -merge_stripes_value 0.16 -layer M3 -block_ring_bottom_layer_limit M2 -width 0.16 -nets {vss vdd} -stacked_via_bottom_layer M1

#add the following statement to restrict routing on layer above Metal 7 as the rules are not well defined ## shivangi
setNanoRouteMode -routeTopRoutingLayer 7
sroute -connect { corePin } -layerChangeRange { M1 M2 } -allowJogging 0 -crossoverViaTopLayer M2 -nets { vss vdd }
saveDesign ${top_level}.pg.enc
addWellTap -cell TAPCELL_ASAP7_75t  -cellInterval 7.6 -inRowOffset 2

puts "####################"
puts "###"
puts "### Place Blockage ..."
puts "###"
puts "####################"
setDrawView fplan
uiSetTool obstruct
createPlaceBlockage -box 5.646 3.910 6.596 20.037 # change co-ordinates if required
createPlaceBlockage -box 13.100 3.969 14.170 20.096
createPlaceBlockage -box 20.852 3.880 21.565 20.155
saveDesign ${top_level}.pg.enc

puts "####################"
puts "###"
puts "### Place Design ..."
puts "###"
puts "####################"
puts "PLACE ITER 0"
setTrialRouteMode -highEffort true 
setPlaceMode  -timingDriven true -congEffort high 
placeDesign  -inPlaceOpt
puts "PLACE ITER 1"
placeDesign  -inPlaceOpt -incremental
puts "PLACE ITER 2"
optDesign -preCTS
saveDesign ${top_level}.place.enc


puts "##############"
puts "###"
puts "### Run CTS..."
puts "###"
puts "##############"

# Create Clock Tree Spec
setCTSMode -engine ck -traceDPinAsLeaf true -traceIoPinAsLeaf true -bottomPreferredLayer 6 -topPreferredLayer 8 -addClockRootProp true
exec /bin/rm -f ${top_level}.cts
createClockTreeSpec -output ${top_level}.cts
# Modify Clock Tree Skey and Latency Requirements
exec sed -i -r "s/^MaxDelay .*/MaxDelay 1000ps/g" ${top_level}.cts
exec sed -i -r "s/^MaxSkew .*/MaxSkew 30ps/g" ${top_level}.cts
exec sed -i -r "s/^Buffer .*/Buffer INVx11_ASAP7_75t_R INVx13_ASAP7_75t_R INVx1_ASAP7_75t_R INVx2_ASAP7_75t_R INVx3_ASAP7_75t_R INVx4_ASAP7_75t_R INVx5_ASAP7_75t_R INVx6_ASAP7_75t_R INVx8_ASAP7_75t_R INVxp67_ASAP7_75t_R INVxp33_AS BUFx10_ASAP7_75t_R BUFx12_ASAP7_75t_R BUFx12f_ASAP7_75t_R BUFx4_ASAP7_75t_R BUFx6f_ASAP7_75t_R BUFx8_ASAP7_75t_R HB1xp67_ASAP7_75t_R HB2xp67_ASAP7_75t_R/g" ${top_level}.cts
specifyClockTree -file ${top_level}.cts
ckSynthesis -rguide ${top_level}.cts.rguide -report ${top_level}.ctsrpt -macromodel ${top_level}.ctsmdl -forceReconvergent 
# Output Results of CTS
trialRoute -guide ${top_level}.cts.rguide
redraw

puts "##############"
puts "###"
puts "### Post CTS..."
puts "###"
puts "##############"
# Post CTS timing checks
puts "POSTCTS ITER 0"
optDesign -postCTS
puts "POSTCTS ITER 1"
optDesign -postCTS -hold
saveDesign ${top_level}.clock.enc  

  
puts "################################"
puts "###"
puts "### Routing   .... "
puts "###"
puts "################################"
    
globalNetConnect vdd -type tiehi -module {}
globalNetConnect vss -type tielo -module {}
applyGlobalNets
generateVias
setNanoRouteMode -routeTopRoutingLayer 7
setNanoRouteMode -quiet -drouteFixAntenna 0
setNanoRouteMode -quiet -routeWithTimingDriven 1
setNanoRouteMode -quiet -drouteEndIteration default
setNanoRouteMode -quiet -routeWithTimingDriven true
setNanoRouteMode -quiet -routeWithSiDriven false
routeDesign -globalDetail

# Post-routing optimization
setDelayCalMode -engine aae -SIAware false
puts "POSTROUTE ITER 0"
extractRC
optDesign -postRoute 
puts "POSTROUTE ITER 1"
extractRC
optDesign -postRoute -drv
puts "POSTROUTE ITER 2"
extractRC
optDesign -postRoute -hold
saveDesign ${top_level}.route.enc 

puts "################################"
puts "###"
puts "### Final Steps   .... "
puts "###"
puts "################################"

addFiller -cell TAPCELL_ASAP7_75t FILLER_TEST1_ASAP7_75t FILLER_TEST_ASAP7_75t FILLER_ASAP7_75t DECAPxp33_ASAP7_75t DECAPx1_ASAP7_75t -prefix FILLER

globalNetConnect vdd -type pgpin -pin vdd -inst * -verbose
globalNetConnect vss -type pgpin -pin vss -inst * -verbose

verifyGeometry -noWireExt -noSameNet 
verifyConnectivity -type all -noAntenna -error 1000000 -warning 50
saveNetlist ${top_level}.apr.v
saveNetlist ${top_level}.apr_pg.v -includePowerGround -excludeLeafCell
extractRC -outfile ${top_level}.cap
rcOut -spf ${top_level}.spf
rcOut -spef ${top_level}.spef
delayCal -sdf ${top_level}.apr.sdf -version 3.0

# Save Final Design
saveDesign ${top_level}.final.enc


