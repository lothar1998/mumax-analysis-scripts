#!/bin/bash

curr=$(pwd)
path="$1/*.sh"

cd $1

for filename in $path
do
	sbatch $filename
done

cd $curr
