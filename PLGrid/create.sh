#!/bin/bash

module add plgrid/tools/python/3.6.5

x=""

for var in "$@"
do
	x="$x $var" 
done

echo $x

python3 CreateVar.py $x
