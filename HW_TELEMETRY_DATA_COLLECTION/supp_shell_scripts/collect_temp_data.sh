#!/bin/bash
# Author | Eduardo Ortega
# Follow this link to setup sensors from cmd line
# Link: https://www.cyberciti.biz/faq/howto-linux-get-sensors-information/
sleep 0.5
for ((i=1; i<=$3; i++)); do
    sensors >> "$2/logTemp_$1.txt"
    sleep 0.0001
done

echo "temp data collect ***********************"
