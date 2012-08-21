#!/bin/bash

#loads the parameter file
. ../../parameters/parameters-global.txt
echo "These are the parameters designated by ../../parameters/parameters-global.txt"
echo "FIELD = " $FIELD
echo "RUN = " $RUN
echo "START_YEAR = " $START_YEAR
echo "END YEAR = "$END_YEAR
echo "TYPE = " $TYPE
echo "SIZE = " $SIZE
echo "NET_PATH =  " $NET_PATH
echo "DATA_PATH =  " $DATA_PATH

ROOT_PATH="../../"
FULL_DATA_PATH=${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/data/$DATA_PATH
FULL_RUN_PATH=${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/
slicing=${TYPE}${START_YEAR}-${END_YEAR}_${SIZE}years

declare -a subdir=("collaboration" "generic" "transfer")
declare -a net_types=("2ndlargest_component" "components" "large_component" "whole_net")

echo "  "
echo "------------------------------------------------------"
echo "  "




# Check that the data file exists in this path
if [ -e $FULL_DATA_PATH ]
then
	bool_data=true
else
	bool_data=false
fi

#check that the field structure is ready for the run
if [ -e $FULL_RUN_PATH ]
then
	bool_run=true
else
	bool_run=false
fi

if ! $bool_run
then
	echo "Please run /pre-processing/make_core_dirs.sh to make sure the directory structure is prepared for the run"
	echo "before running this script"
	exit 1
fi

if ! $bool_data
then
	echo "The parameters-global.txt file specifies that there should be data at $FULL_DATA_PATH"
	echo "However, there does not appear to be any data at this location."
	echo "Either change the parameter file to reflect where the data is or place the data in this directory"
	exit 1
fi

if $bool_data && $bool_run
then
	echo "Setting up directories for $FIELD $RUN $START_YEAR - $END_YEAR with $TYPE $SIZE year slicing"
else
	exit 1	
fi

# Set up slicing scheme
thisrun_net=${FULL_RUN_PATH}$RUN/output/networks/${slicing}
thisrun_stat=${FULL_RUN_PATH}$RUN/output/statistics/${slicing}
for i in ${subdir[*]}
do
	mkdir -p ${thisrun_net}/$i
	mkdir -p ${thisrun_stat}/$i
done

# Set up individual slices
if [ "$TYPE" = "accumulative" ]
then
	#initialize array to accumulative
	echo "Setting up slicing for accumulative"
	let "window=${END_YEAR}-${START_YEAR}"
	#echo "window is $window"
	let "numslices=$window/$SIZE"
	let "firstendyear=$START_YEAR+$SIZE-1"
	for ((i=${firstendyear}; i <=$END_YEAR; i+=${SIZE}))
	do
		echo $i
		endyears[${#endyears[*]}]="${START_YEAR}-${i}"
	done
	endyears[${#endyears[*]}]="allyears"
	#echo ${endyears[*]}
	
	for i in ${endyears[*]}
	do	
		mkdir -p ${thisrun_net}/generic/$i
		for j in ${net_types[*]}
		do
			echo ${thisrun_net}/generic/$i/$j
			mkdir -p ${thisrun_net}/generic/$i/$j
		done
		mkdir -p ${thisrun_net}/generic/$i/components/4alluvial
		mkdir -p ${thisrun_net}/generic/$i/large_component/images
		mkdir -p ${thisrun_net}/generic/$i/large_component/pajek
		mkdir -p ${thisrun_net}/generic/$i/2ndlargest_component/images
		mkdir -p ${thisrun_net}/generic/$i/2ndlargest_component/pajek
		mkdir -p ${thisrun_net}/generic/$i/whole_net/hubs/
		mkdir -p ${thisrun_net}/generic/$i/whole_net/images/
		mkdir -p ${thisrun_net}/generic/$i/whole_net/pajek/
	done

	
	for i in ${endyears[*]}
	do
		mkdir -p "${thisrun_net}/collaboration/${i}"
		mkdir -p "${thisrun_net}/transfer/${i}"
		mkdir -p "${thisrun_net}/collaboration/${i}/author_level_net"
		mkdir -p "${thisrun_net}/transfer/${i}/author_level_net"
		mkdir -p "${thisrun_net}/collaboration/${i}/cluster_level_net"
		mkdir -p "${thisrun_net}/transfer/${i}/cluster_level_net"

		for j in ${net_types[*]}
		do
			mkdir -p "${thisrun_net}/collaboration/${i}/author_level_net/${j}"
			mkdir -p "${thisrun_net}/transfer/${i}/author_level_net/${j}"
			mkdir -p "${thisrun_net}/collaboration/${i}/cluster_level_net/${j}"
			mkdir -p "${thisrun_net}/transfer/${i}/cluster_level_net/${j}"
		done
	done


	for i in ${endyears[*]}
	do	
		for h in ${subdir[*]}
		do
			mkdir -p ${thisrun_stat}/$h/$i
			for j in ${net_types[*]}
			do
				echo ${thisrun_stat}/$h/$i/$j
				mkdir -p ${thisrun_stat}/$h/$i/$j
				mkdir -p ${thisrun_stat}/$h/$i/$j/images
				mkdir -p ${thisrun_stat}/$h/$i/$j/tables
			done
		done
	done

elif [ "$TYPE" = "discrete" ]
then
	#initialize array to discrete
	echo "Setting up slicing for discrete"
	let "window=${END_YEAR}-${START_YEAR}"
	echo "window is $window"
	let "numslices=$window/$SIZE"
	let "firstendyear=$START_YEAR+$SIZE-1"
	firststartyear=${START_YEAR}
	for ((i=${firststartyear}, k=${firstendyear}; k <=$END_YEAR; i+=${SIZE}, k+=${SIZE}))
	do
		echo "$i - $k"
		years[${#years[*]}]="${i}-${k}"
	done
	years[${#years[*]}]="allyears"
	#echo ${endyears[*]}
	
	for i in ${years[*]}
	do	
		mkdir -p ${thisrun_net}/generic/$i
		for j in ${net_types[*]}
		do
			echo ${thisrun_net}/generic/$i/$j
			mkdir -p ${thisrun_net}/generic/$i/$j
		done
		mkdir -p ${thisrun_net}/generic/$i/components/4alluvial
		mkdir -p ${thisrun_net}/generic/$i/large_component/images
		mkdir -p ${thisrun_net}/generic/$i/large_component/pajek
		mkdir -p ${thisrun_net}/generic/$i/2ndlargest_component/images
		mkdir -p ${thisrun_net}/generic/$i/2ndlargest_component/pajek
		mkdir -p ${thisrun_net}/generic/$i/whole_net/hubs/
		mkdir -p ${thisrun_net}/generic/$i/whole_net/images/
		mkdir -p ${thisrun_net}/generic/$i/whole_net/pajek/
	done

	for i in ${years[*]}
	do
		mkdir -p "${thisrun_net}/collaboration/${i}"
		mkdir -p "${thisrun_net}/transfer/${i}"
		mkdir -p "${thisrun_net}/collaboration/${i}/author_level_net"
		mkdir -p "${thisrun_net}/transfer/${i}/author_level_net"
		mkdir -p "${thisrun_net}/collaboration/${i}/cluster_level_net"
		mkdir -p "${thisrun_net}/transfer/${i}/cluster_level_net"

		for j in ${net_types[*]}
		do
			mkdir -p "${thisrun_net}/collaboration/${i}/author_level_net/${j}"
			mkdir -p "${thisrun_net}/transfer/${i}/author_level_net/${j}"
			mkdir -p "${thisrun_net}/collaboration/${i}/cluster_level_net/${j}"
			mkdir -p "${thisrun_net}/transfer/${i}/cluster_level_net/${j}"
		done
	done

	
	for i in ${years[*]}
	do	
		for h in ${subdir[*]}
		do
			mkdir -p ${thisrun_stat}/$h/$i
			for j in ${net_types[*]}
			do
				echo ${thisrun_stat}/$h/$i/$j
				mkdir -p ${thisrun_stat}/$h/$i/$j
				mkdir -p ${thisrun_stat}/$h/$i/$j/images
				mkdir -p ${thisrun_stat}/$h/$i/$j/tables
			done
		done
	done

elif [ "$TYPE" = "sliding" ]
then
	#initialize array to sliding
	echo "Setting up slicing for sliding"
	let "window=${END_YEAR}-${START_YEAR}"
	echo "window is $window"
	let "numslices=$window/$SIZE"
	let "firstendyear=$START_YEAR+$SIZE-1"
	firststartyear=${START_YEAR}
	for ((i=${firststartyear}, k=${firstendyear}; k <=$END_YEAR; i+=1, k+=1))
	do
		echo "$i - $k"
		years[${#years[*]}]="${i}-${k}"
	done
	years[${#years[*]}]="allyears"

	for i in ${years[*]}
	do	
		mkdir -p ${thisrun_net}/generic/$i
		for j in ${net_types[*]}
		do
			echo ${thisrun_net}/generic/$i/$j
			mkdir -p ${thisrun_net}/generic/$i/$j
		done
		mkdir -p ${thisrun_net}/generic/$i/components/4alluvial
		mkdir -p ${thisrun_net}/generic/$i/large_component/images
		mkdir -p ${thisrun_net}/generic/$i/large_component/pajek
		mkdir -p ${thisrun_net}/generic/$i/2ndlargest_component/images
		mkdir -p ${thisrun_net}/generic/$i/2ndlargest_component/pajek
		mkdir -p ${thisrun_net}/generic/$i/whole_net/hubs/
		mkdir -p ${thisrun_net}/generic/$i/whole_net/images/
		mkdir -p ${thisrun_net}/generic/$i/whole_net/pajek/
	done

	for i in ${years[*]}
	do
		mkdir -p "${thisrun_net}/collaboration/${i}"
		mkdir -p "${thisrun_net}/transfer/${i}"
		mkdir -p "${thisrun_net}/collaboration/${i}/author_level_net"
		mkdir -p "${thisrun_net}/transfer/${i}/author_level_net"
		mkdir -p "${thisrun_net}/collaboration/${i}/cluster_level_net"
		mkdir -p "${thisrun_net}/transfer/${i}/cluster_level_net"

		for j in ${net_types[*]}
		do
			mkdir -p "${thisrun_net}/collaboration/${i}/author_level_net/${j}"
			mkdir -p "${thisrun_net}/transfer/${i}/author_level_net/${j}"
			mkdir -p "${thisrun_net}/collaboration/${i}/cluster_level_net/${j}"
			mkdir -p "${thisrun_net}/transfer/${i}/cluster_level_net/${j}"
		done
	done


	for i in ${years[*]}
	do	
		for h in ${subdir[*]}
		do
			mkdir -p ${thisrun_stat}/$h/$i
			for j in ${net_types[*]}
			do
				echo ${thisrun_stat}/$h/$i/$j
				mkdir -p ${thisrun_stat}/$h/$i/$j
				mkdir -p ${thisrun_stat}/$h/$i/$j/images
				mkdir -p ${thisrun_stat}/$h/$i/$j/tables
			done
		done
	done

	
fi
	

cd ${FULL_RUN_PATH}/${RUN}/output/statistics
#tree
