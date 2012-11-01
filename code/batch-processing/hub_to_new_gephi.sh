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
stat_csv="${FULL_RUN_PATH}${RUN}/output/statistics/${accumul_slice}/generic/allyears/whole_net/tables/hub_to_new_stats.csv"
headers="YEAR, HUBTONEW"
hublist="${FULL_RUN_PATH}${RUN}/output/networks/${accumul_slice}/generic/${NETSTART_YEAR}-${NETEND_YEAR}/whole_net/hubs/${FIELD}${RUN}_accumulative${NETSTART_YEAR}-${NETEND_YEAR}_${SIZE}years_wholenet.hub"
echo $headers > ${stat_csv}
hubnew_png="${FULL_RUN_PATH}${RUN}/output/statistics/${accumul_slice}/generic/allyears/whole_net/images/"
linebreak="---------------------------------------------------------"

#initialize slicing scheme
echo "Initializing Slicing Scheme"
let "window=${END_YEAR}-${START_YEAR}"
let "numslices=$window/$SIZE"
let "firstendyear=$START_YEAR+$SIZE"
firststartyear=${NETSTART_YEAR}

disc_loc[${#disc_loc[*]}]="${FULL_RUN_PATH}${RUN}/output/networks/${discrete_slice}/generic/${START_YEAR}-${START_YEAR}/whole_net/pajek/${FIELD}${RUN}_discrete${START_YEAR}-${START_YEAR}_${SIZE}years_wholenet.net"
k=0
echo ${disc_loc[$k]}
accprev_loc[${#accprev_loc[*]}]="firstyear"
echo ${accprev_loc[$k]}
accnew_loc[${#accnew_loc[*]}]="${FULL_RUN_PATH}${RUN}/output/networks/${accumul_slice}/generic/${START_YEAR}-${START_YEAR}/whole_net/gephi/${FIELD}${RUN}_accumulative${START_YEAR}-${START_YEAR}_${SIZE}years_weighted_hubtonew.gexf"

for ((k=${firstendyear}; k <=${END_YEAR}; k+=${SIZE}))
do
	let "prevyear=$k-1"
	currSlice="${k}-${k}"
	prevSlice="${START_YEAR}-${prevyear}"
	accSlice="${START_YEAR}-${k}"
	disc_loc[${#disc_loc[*]}]="${FULL_RUN_PATH}${RUN}/output/networks/${discrete_slice}/generic/${currSlice}/whole_net/pajek/${FIELD}${RUN}_discrete${currSlice}_${SIZE}years_wholenet.net"
	#echo "disc_loc = ${disc_loc[${#disc_loc[]} - 1]"
	accprev_loc[${#accprev_loc[*]}]="${FULL_RUN_PATH}${RUN}/output/networks/${accumul_slice}/generic/${prevSlice}/whole_net/gephi/${FIELD}${RUN}_accumulative${prevSlice}_${SIZE}years_weighted_hubtonew.gexf"
	#echo "accprev_loc = ${accprev_loc[${#accprev_loc[*]} - 1]}"
	accnew_loc[${#accnew_loc[*]}]="${FULL_RUN_PATH}${RUN}/output/networks/${accumul_slice}/generic/${accSlice}/whole_net/gephi/${FIELD}${RUN}_accumulative${accSlice}_${SIZE}years_weighted_hubtonew.gexf"
	#echo "accnew_loc = ${accnew_loc[${#accnew_loc[*]} -1]}"
done

i=0
while [ $i -lt ${#disc_loc[@]} ]
do 

	echo $linebreak
	echo "Creating HUB to NEW Author gexf file"
	cd ../clustering
	python node_weightbypublications.py "${disc_loc[$i]}" "${accprev_loc[$i]}" "${accnew_loc[$i]}"
	Py_Check=$?
	cd - 

	#check for python problems 
	if [ ${Py_Check} != 0 ]
	then
		echo $linebreak
		echo "problem creating gexf file"
		exit 1
		echo $linebreak
	fi
	i=$[i+1]

done

i=1
for ((k=${firstendyear}; k <=${END_YEAR}; k+=${SIZE}))
do

	echo $linebreak
	echo "Adding Hub Attributes filling out HUB CSV"
	cd ../clustering
	echo "accumulative graph for ${k}"
	echo "accnew_loc : "${accnew_loc[$i]}
	echo "${hublist}"

	python hubtonew.py "${accnew_loc[$i]}" "${stat_csv}" "${hublist}" "${k}"
	Py_Check=$?
	cat ${stat_csv}
	cd - 

	#check for python problems 
	if [ ${Py_Check} != 0 ]
	then
		echo $linebreak
		echo "problem creating with hubtonew.py for ${k}"
		exit 1
		echo $linebreak
	fi
	i=$[i+1]
done

echo "Plotting stats graphs"
args="--args outpath='${hubnew_png}' field='${FIELD}' run='${RUN}' type='${TYPE}' csv='${stat_csv}' start_year='${START_YEAR}' end_year='${END_YEAR}'"

R --slave "$args" < ../data-visualization/hub_to_new_plot.R
R_Check=$?
if [ ${R_Check} != 0 ]
then
	echo "problem creating plot for Largest Component Diameter vs. Size"
	exit 1
fi
#echo "processing of gexf files has finished"
#echo $linebreak

#echo "Plotting stats graphs"
#args="--args outpath='${oldnew_png}' field='${FIELD}' run='${RUN}' type='${TYPE}' csv='${cluster_csv}' start_year='${START_YEAR}' end_year='${END_YEAR}'"

#R --slave "$args" < ../data-visualization/old_new_stat_vis.R
#R_Check=$?
#if [ ${R_Check} != 0 ]
#then
#	echo "problem creating plot for Largest Component Diameter vs. Size"
#	exit 1
#fi

#echo $linebreak
#echo "PROGRAM FINISHED"
#echo $linebreak

