#!/bin/bash
# Author | Eduardo Ortega

#echo "ensuring perf mode is on"

sleep 3

echo "starting pcm"
for i in {1..10} 
do
    echo "$i"
    sleep 3
    sudo ~/pcm/build/bin/pcm 0.013 -i=200 -csv="benign_rh/log_$i.csv"
done
