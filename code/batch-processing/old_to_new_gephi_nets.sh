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

NETEND_YEAR="2010"
NETSTART_YEAR="1991"

ROOT_PATH="../../"
FULL_DATA_PATH=${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/data/$DATA_PATH
FULL_RUN_PATH=${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/
slicing=${TYPE}${NETSTART_YEAR}-${NETEND_YEAR}_${SIZE}years
discrete_slice=discrete${NETSTART_YEAR}-${NETEND_YEAR}_${SIZE}years
accumul_slice=accumulative${NETSTART_YEAR}-${NETEND_YEAR}_${SIZE}years
cluster_csv="${FULL_RUN_PATH}${RUN}/output/statistics/${discrete_slice}/generic/allyears/whole_net/tables/old_new_authors.csv"
oldnew_png="${FULL_RUN_PATH}${RUN}/output/statistics/${discrete_slice}/generic/allyears/whole_net/images/"
echo "cluster_csv = ${cluster_csv}"
linebreak="---------------------------------------------------------"

# figure out time slices
# Anets -> The discrete slice of the network that is of interest at time, t
# Bnets -> The accumulative slice of the network up until time, t - 1
# Cnets -> The accumulative large component slice of the network up until time, t

#initialize CSV to keep track of new author, old author, large component, non-large component cluster sizes
echo "YEAR, SIZE, OLD, NEW, inLC, outLC, OLDIN, OLDOUT, NEWIN, NEWOUT" > ${cluster_csv}

#initialize slicing scheme
echo "Initializing Slicing Scheme"
let "window=${END_YEAR}-${START_YEAR}"
let "numslices=$window/$SIZE"
let "firstendyear=$START_YEAR+$SIZE"
firststartyear=${NETSTART_YEAR}
for ((k=${firstendyear}; k <=${END_YEAR}; k+=${SIZE}))
do
	let "prevyear=$k-1"
	currSlice="${k}-${k}"
	prevSlice="${START_YEAR}-${prevyear}"
	accSlice="${START_YEAR}-${k}"
	currPaj="${FULL_RUN_PATH}${RUN}/output/networks/${discrete_slice}/generic/${currSlice}/whole_net/pajek/${FIELD}${RUN}_discrete${currSlice}_${SIZE}years_wholenet.net"
	echo "currPaj = ${currPaj}"
	prevPaj="${FULL_RUN_PATH}${RUN}/output/networks/${accumul_slice}/generic/${prevSlice}/whole_net/pajek/${FIELD}${RUN}_accumulative${prevSlice}_${SIZE}years_wholenet.net"
	echo "prevPaj = ${prevPaj}"
	lcPaj="${FULL_RUN_PATH}${RUN}/output/networks/${accumul_slice}/generic/${accSlice}/large_component/pajek/${FIELD}${RUN}_accumulative${accSlice}_${SIZE}years_lc.net"
	echo "lcPaj = ${lcPaj}"
	outGexf="${FULL_RUN_PATH}${RUN}/output/networks/${discrete_slice}/generic/${currSlice}/whole_net/gephi/${FIELD}${RUN}_discrete${currSlice}_${SIZE}years_wholenet.gexf"
	echo "outGexf = ${outGexf}"
	#check for files
	if [ -e ${currPaj} ] && [ -e ${prevPaj} ] && [ -e ${lcPaj} ]
	then
		echo $linebreak
		echo "Creating NEW to OLD gexf file for ${currPaj}"
		cd ../clustering
		python new_to_old_authors_clustering.py "${currPaj}" "${prevPaj}" "${lcPaj}" "${outGexf}" "${cluster_csv}" "${k}"
		Py_Check=$?
		cd - 

		#check for python problems 
		if [ ${Py_Check} != 0 ]
		then
			echo $linebreak
			echo "problem creating gexf file for ${currPaj}"
			exit 1
			echo $linebreak
		fi
		else
		echo $linebreak
		echo "You must first create all the pajek files for $NETSTART_YEAR to $NETEND_YEAR"
		echo "in order to run this program."
		echo $linebreak
		exit 1
	fi
done
echo "processing of gexf files has finished"
echo $linebreak

echo "Plotting stats graphs"
args="--args outpath='${oldnew_png}' field='${FIELD}' run='${RUN}' type='${TYPE}' csv='${cluster_csv}' start_year='${START_YEAR}' end_year='${END_YEAR}'"

R --slave "$args" < ../data-visualization/old_new_stat_vis.R
R_Check=$?
if [ ${R_Check} != 0 ]
then
	echo "problem creating plot for Largest Component Diameter vs. Size"
	exit 1
fi

echo $linebreak
echo "PROGRAM FINISHED"
echo $linebreak

