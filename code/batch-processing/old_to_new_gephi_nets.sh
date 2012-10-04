#!/bin/bash

#----NOTE-----
# This program assumes that the accumulative 1 year slicing for START_YEAR to END_YEAR have
# already been processed and output to their appropriate folders.  If this has not been done,
# this program will exit with an error

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

NETEND_YEAR = "2010"
NETSTART_YEAR = "1991"

ROOT_PATH="../../"
FULL_DATA_PATH=${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/data/$DATA_PATH
FULL_RUN_PATH=${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/
slicing=${TYPE}${NETSTART_YEAR}-${NETEND_YEAR}_${SIZE}years
discrete_slice=discrete${NETSTART_YEAR}-${NETEND_YEAR}_${SIZE}years
accumul_slice=accumulative${NETSTART_YEAR}-${NETEND_YEAR}_${SIZE}years
linebreak="---------------------------------------------------------"

# figure out time slices
# Anets -> The discrete slice of the network that is of interest at time, t
# Bnets -> The accumulative slice of the network up until time, t - 1
# Cnets -> The accumulative large component slice of the network up until time, t

echo "Initializing Slicing Scheme"
let "window=${END_YEAR}-${START_YEAR}"
let "numslices=$window/$SIZE"
let "firstendyear=$START_YEAR+$SIZE-1"
firststartyear=${NETSTART_YEAR}
for ((k=${firstendyear}; k <=${END_YEAR}; k+=${SIZE}))
do
	let "prevyear=$k-1"
	currSlice = "${k}-${k}"
	prevSlice = "${START_YEAR}-${prevyear}"
	currPaj="${FULL_RUN_PATH}${RUN}/output/networks/${discrete_slice}/generic/${currSlice}/whole_net/pajek/${FIELD}${RUN}_discrete${i}_${SIZE}years_wholenet.net"
	prevPaj="${FULL_RUN_PATH}${RUN}/output/networks/${accumulative_slice}/generic/${prevSlice}/whole_net/pajek/${FIELD}${RUN}_${TYPE}${i}_${SIZE}years_wholenet.net"
	lcPaj="${FULL_RUN_PATH}${RUN}/output/networks/${accumulative_slice}/generic/${currSlice}/large_component/pajek/${FIELD}${RUN}_${TYPE}${i}_${SIZE}years_lc.net"
	outGexf="${FULL_RUN_PATH}${RUN}/output/networks/${discrete_slice}/generic/${currSlice}/whole_net/gephi/${FIELD}${RUN}_discrete${i}_${SIZE}years_wholenet.gexf"

	#check for files
	if [ -e ${currPaj} ] && [ -e ${prevPaj} ] && [ -e ${lcPaj} ]
	then
		$linebreak
		echo "Creating NEW to OLD gexf file for ${currPaj}"
		cd ../clustering
		python new_to_old_authors_clustering.py ${currPaj} ${prevPaj} ${lcPaj} ${outGexf}
		Py_Check=$?
		cd - 

		#check for python problems 
		if [ ${Py_Check} != 0 ]
		then
			$linebreak
			echo "problem creating gexf file for ${currPaj}"
			exit 1
			$linebreak
		fi
		else
		$linebreak
		echo "You must first create all the pajek files for $NETSTART_YEAR to $NETEND_YEAR"
		echo "in order to run this program."
		$linebreak
		exit 1
	fi
done
echo "PROGRAM FINISHED"
echo $linebreak

