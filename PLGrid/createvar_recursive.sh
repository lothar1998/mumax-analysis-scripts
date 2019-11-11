#!/bin/bash

files=$(find $1 -name '*.mx3')

echo $1
echo $2
echo $3
echo $4
echo $5
echo $6

edited=0

for file in $files
do
	python3 CreateVar.py -f $file -l $2 -i $3 -b $4 -e $5 -s $6
	edited=$((edited+1))
done

echo "edited: $edited"
