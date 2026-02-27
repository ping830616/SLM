#!/bin/bash
echo "DFT"
date +"%T.%3N"
~/PAMPAR/Apps/DFT/pthread 16 32768
date +"%T.%3N"

sleep 3

echo "DJ"
date +"%T.%3N"
~/PAMPAR/Apps/DJ/pthread 16 16384 ~/PAMPAR/Apps/DJ/inputDJ/1024.txt
date +"%T.%3N"

sleep 3

echo "DP"
date +"%T.%3N"
~/PAMPAR/Apps/DP/pthread 16 50000000000
date +"%T.%3N"

sleep 3

echo "GL"
date +"%T.%3N"
./GL_bchmark.sh
date +"%T.%3N"

sleep 3

echo "GS"
date +"%T.%3N"
~/PAMPAR/Apps/GS/pthread 16 1300
date +"%T.%3N"

sleep 3

echo "HA"
date +"%T.%3N"
~/PAMPAR/Apps/HA/pthread 16 10000 300000
date +"%T.%3N"

sleep 3

echo "JA"
date +"%T.%3N"
~/PAMPAR/Apps/JA/pthread 16 4096
date +"%T.%3N"

sleep 3

echo "MM"
date +"%T.%3N"
~/PAMPAR/Apps/MM/pthread 16 4096
date +"%T.%3N"

sleep 3

echo "NI"
date +"%T.%3N"
~/PAMPAR/Apps/NI/pthread 16 5000000000
date +"%T.%3N"

sleep 3

echo "OE"
date +"%T.%3N"
~/PAMPAR/Apps/OE/pthread 16 300000
date +"%T.%3N"

sleep 3

echo "PI"
date +"%T.%3N"
~/PAMPAR/Apps/PI/pthread 16 4000000000
date +"%T.%3N"

sleep 3

echo "SH"
date +"%T.%3N"
~/PAMPAR/Apps/SH/pthread moon_3000.jpg 3000 3000 16
date +"%T.%3N"

sleep 3

echo "TR"
date +"%T.%3N"
~/PAMPAR/Apps/TR/pthread 16 2500
date +"%T.%3N"

sleep 3

