#!/bin/bash

if [ $1 = "-r" ]
then	

	runned=0

	directories=$(find $2 -name '*.sh' | sed -r 's|/[^/]+$||' | sort | uniq)

	for directory in $directories
	do
		filenames="$directory/*.sh"	
		
		curr=$(pwd)
		
		cd $dir

		for filename in $filenames
		do
			sbatch $filename
			runned=$((runned+1))
		done
		
		cd $curr

	done

	echo "runned scripts: $runned"

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

