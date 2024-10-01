#!/bin/bash

cd /home/navpi/reeds_shepp-1.0.7/Python-3.8.10

source /path/to/your/venv/bin/activate

cx = $1
cy = $2
ct = $3

fx = $4 
fy = $5
ft = $6

result=$(python getPath.py $cx $cy $ct $fx $fy $ft)

echo "$result"