#!/bin/bash

path="$1/*.sh"

for filename in $path
do
	sbatch $filename
done
