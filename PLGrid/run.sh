#!/bin/bash

curr=$(pwd)

if [ $1 = "-r" ]
then	

	echo "no. 1"

	listOfScripts=$(find $2 -name '*.sh')

	for filename in $listOfScripts
	do
		sbatch $filename
	done

else
	echo "no. 2"
	
	path="$1/*.sh"

	cd $1

	for filename in $path
	do
		sbatch $filename
	done

	cd $curr

fi

