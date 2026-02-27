#!/bin/bash
# Author | Eduardo Ortega
# install msrtoosl for rdmsr
sleep 0.5
for ((i=1; i<=$3; i++)); do
    echo "scale=8; $(sudo rdmsr 0x198 -u --bitfield 47:32)/8192" | bc >> "$2/logVolt_$1.txt"
    sleep 0.0001
done

echo "volt data collect ***********************"
