#!/bin/bash

if [ $1 = "-r" ]
then	

	listOfScripts=$(find $2 -name '*.sh')

	for filename in $listOfScripts
	do
		sbatch $filename
	done

else

	curr=$(pwd)	
	path="$1/*.sh"

	cd $1

	for filename in $path
	do
		sbatch $filename
	done

	cd $curr

fi

