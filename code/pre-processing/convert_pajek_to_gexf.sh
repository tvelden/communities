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
linebreak="---------------------------------------------------------"

#initialize time slice structure
cd ../pre-processing
./make_dirs_for_timeslice.sh
cd -

#figure out time slices
if [ "${TYPE}" == "accumulative" ]
then
	#initialize array to accumulative
	echo "Setting up slicing for accumulative"
	let "window=${END_YEAR}-${START_YEAR}"
	#echo "window is $window"
	let "numslices=$window/$SIZE"
	let "firstendyear=$START_YEAR+$SIZE-1"
	for ((i=${firstendyear}; i <=${END_YEAR}; i+=${SIZE}))
	do
		#echo $i
		years[${#years[*]}]="${START_YEAR}-${i}"
	done
	echo $linebreak

elif [ "${TYPE}" == "discrete" ]
then
	#initialize array to discrete
	echo "Setting up slicing for discrete"
	let "window=${END_YEAR}-${START_YEAR}"
	#echo "window is $window"
	let "numslices=$window/$SIZE"
	let "firstendyear=$START_YEAR+$SIZE-1"
	firststartyear=${START_YEAR}
	for ((i=${firststartyear}, k=${firstendyear}; k <=${END_YEAR}; i+=${SIZE}, k+=${SIZE}))
	do
		#echo "$i - $k"
		years[${#years[*]}]="${i}-${k}"
	done
	echo $linebreak
elif [ "${TYPE}" == "sliding" ]
then
	#initialize array to discrete
	echo "Setting up slicing for discrete"
	let "window=${END_YEAR}-${START_YEAR}"
	#echo "window is $window"
	let "numslices=$window/$SIZE"
	let "firstendyear=$START_YEAR+$SIZE-1"
	firststartyear=${START_YEAR}
	for ((i=${firststartyear}, k=${firstendyear}; k <=${END_YEAR}; i+=${SIZE}, k+=${SIZE}))
	do
		#echo "$i - $k"
		years[${#years[*]}]="${i}-${k}"
	done
	echo $linebreak
else
	echo "The parameter file is using an invalid type, $TYPE"
	exit 1
fi

#count the number of slices which have a network slice
count=0
for i in ${years[*]}
do
	if [ `ls -1 ${FULL_RUN_PATH}${RUN}/output/networks/${slicing}/generic/${i}/whole_net/pajek/*.net | wc -l` -ne 0 ]
	then
		count=$[count+1]
	fi
done

echo $linebreak

#check for network files in whole_net, run networkbuild.py if they don't exist
echo "There are $count time slices created for these parameter settings"
if [ $count != 0 ]
then
	echo "The whole network .net files for $time_slice have already been created"
	networkbuildcheck=0
else
	echo "The whole network .net files for $time_slice have not been processed yet"
	echo "Running networkbuild.py now to create $time_slice time slices"
	cd ../build-networks/co-author
	pwd
	python netbuild-pajek.py 
	networkbuildcheck=$? #grab exit code from running python script
	if [[ $networkbuildcheck != 0 ]] #check exit code
	then
		echo "networkbuild.py did not finish correctly"
		exit 1 # END SHELL SCRIPT WITH EXIT STATUS CODE 1
	else
		echo "networkbuild.py has finished making time sliced .net files for ${time_slice}"
	fi
	cd -
	pwd
fi

echo $linebreak

#create statistics CSV for whole network and large component network
stat_csv="${FULL_RUN_PATH}${RUN}/output/statistics/${slicing}/generic/allyears/whole_net/tables/whole_lc_stats"
headers="START, END, TOTAL_SIZE_NODES, TOTAL_SIZE_EDGES, LC_SIZE_NODES, LC_SIZE_EDGES, LC_DIAM"
if [ -e $stat_csv ]
then
	echo "component_analysis csv has already been initialized"
else
	echo "initializing analysis csv"
	echo $headers > ${stat_csv}
fi

#create statistics csv for 2nd largest component network
snd_stat_csv="${FULL_RUN_PATH}${RUN}/output/statistics/${slicing}/generic/allyears/whole_net/tables/sndlc_stats"
if [ -e $snd_stat_csv ]
then
	echo "component_analysis csv has already been initialized"
else
	headers2="START, END, SNDLC_SIZE_NODES, SNDLC_SIZE_EDGES, SNDLC_DIAM"	
	echo $headers2 > ${snd_stat_csv}
fi

#get filenames for each .net file
for i in ${years[*]}
do
	fullnet[${#fullnet[*]}]=${FULL_RUN_PATH}${RUN}/output/networks/${slicing}/generic/${i}/whole_net/pajek/${FIELD}${RUN}_${TYPE}${i}_${SIZE}years_wholenet.net
	lc_pajek[${#lc_pajek[*]}]=${FULL_RUN_PATH}${RUN}/output/networks/${slicing}/generic/${i}/large_component/pajek/
	sndlc_pajek[${#sndlc_pajek[*]}]=${FULL_RUN_PATH}${RUN}/output/networks/${slicing}/generic/${i}/2ndlargest_component/pajek/
	pajekpath[${#pajekpath[*]}]=${FULL_RUN_PATH}${RUN}/output/networks/${slicing}/generic/${i}/whole_net/pajek/
	basenames[${#basenames[*]}]=${FIELD}${RUN}_${TYPE}${i}_${SIZE}years
done

echo $linebreak

###################################################################################################

#check if there are large component files for this run already, creates files if they don't exist
#count the number of slices which have a large component network slice
lc_count=0
i=0
while [ $i -lt ${#years[@]} ]
do
	if [ -e ${lc_pajek[$i]}/${basenames[$i]}_lc.net ]
	then
		lc_count=$[lc_count + 1]
	fi
	i=$[i+1]
done

echo "There are ${lc_count} large component time slices created for these parameter settings"
if [ ${lc_count} != 0 ]
then
	echo "Largest Component network files have already been generated"
else
	i=0
	while [ $i -lt ${#years[@]} ]
	do
		args="--args filepath='${fullnet[$i]}' outpath='${lc_pajek[$i]}/${basenames[$i]}_lc.net' csv='${stat_csv}' years='${years[$i]}'"
		echo "Largest Component : ${years[$i]}"
		R --slave "$args" < ../build-networks/co-author/lcbuild.R
		R_Check=$?
		if [ ${R_Check} != 0 ]
		then
			echo "problem running lcbuild.R for $i"
			exit 1
		fi
	i=$[i+1]
	done
fi

echo $linebreak
echo "Computing statistics for the Second Largest Component and processing subnetwork"
#check if there are second largest component files for this run already, creates files if they don't exist
sndlc_count=0
i=0
while [ $i -lt ${#years[@]} ]
do
	if [ -e ${sndlc_pajek[$i]}/${basenames[$i]}_sndlc.net ]
	then
		sndlc_count=$[sndlc_count + 1]
	fi
	i=$[i+1]
done

echo "There are ${sndlc_count} second large component time slices created for these parameter settings"
if [ ${sndlc_count} != 0 ]
then
	echo "Second Largest Component network files have already been generated"
else
	i=0
	while [ $i -lt ${#years[@]} ]
	do
		args="--args filepath='${fullnet[$i]}' outpath='${sndlc_pajek[$i]}/${basenames[$i]}_sndlc.net' csv='${snd_stat_csv}' years='${years[$i]}'"
		echo "Second Largest Component : ${years[$i]}"
		R --slave "$args" < ../build-networks/co-author/sndlcbuild.R
		R_Check=$?
		if [ ${R_Check} != 0 ]
		then
			echo "problem running lcbuild.R for $i"
			exit 1
		fi
	i=$[i+1]
	done
fi

echo $linebreak


# Plot Graph of Large Component Size vs. Time
#check if there are second largest component files for this run already, creates files if they don't exist
lcsizevtime="${FULL_RUN_PATH}${RUN}/output/statistics/${slicing}/generic/allyears/large_component/images/${slicing}_lc_size-vs-time"
if [ -e  ${lcsizevtime}_actual_nodes.png ] && [ -e ${lcsizevtime}_actual_edges.png ] && [ -e ${lcsizevtime}_percent_edges.png ] && [ -e ${lcsizevtime}_percent_nodes.png ]
then
	echo "Plot graph of Largest Component Size vs. Time has already been created at :"
	echo $lcsizevtime
	echo $linebreak
else
	args="--args net_type='lc' outpath='${lcsizevtime}' field='${FIELD}' run='${RUN}' #size='${SIZE}' type='${TYPE}' csv='${stat_csv}' start_year='${START_YEAR}' end_year='${END_YEAR}'"
	#echo $linebreak
	#echo $args
	#echo $linebreak
	echo "Creating Plot graph of Large Component vs. Time at ${lcsizevtime}"
	echo $linebreak
	R --slave "$args" < ../data-visualization/net_sizevstime.R
	R_Check=$?
	if [ ${R_Check} != 0 ]
	then
		echo "problem creating plot for Large Component Size vs. Time"
		exit 1
	fi
fi

# Plot Graph of  Second Largest COmponent vs. Time
#check if there are second largest component files for this run already, creates files if they don't exist
sndlcsizevtime="${FULL_RUN_PATH}${RUN}/output/statistics/${slicing}/generic/allyears/2ndlargest_component/images/${slicing}_sndlc_size-vs-time"
if [ -e  ${sndlcsizevtime}_actual_nodes.png ] && [ -e ${sndlcsizevtime}_actual_edges.png ] && [ -e ${sndlcsizevtime}_percent_edges.png ] && [ -e ${sndlcsizevtime}_percent_nodes.png ]
then
	echo "Plot graph of Second Largest Component Size vs. Time has already been created at :"
	echo $sndlcsizevtime
	echo $linebreak
else
	args="--args net_type='sndlc' outpath='${sndlcsizevtime}' field='${FIELD}' run='${RUN}' size='${SIZE}' type='${TYPE}' csv='${snd_stat_csv}' start_year='${START_YEAR}' end_year='${END_YEAR}' csv2='${stat_csv}'"
	#echo $linebreak
	#echo $args
	#echo $linebreak
	echo "Creating Plot graph of Second Largest Component vs. Time at ${lcsizevtime}"
	echo $linebreak
	R --slave "$args" < ../data-visualization/net_sizevstime.R
	R_Check=$?
	if [ ${R_Check} != 0 ]
	then
		echo "problem creating plot for Second Largest Component Size vs. Time"
		exit 1
	fi
fi

# Plot Graph of Largest Component Diameter vs. Time
lcdiamvtime="${FULL_RUN_PATH}${RUN}/output/statistics/${slicing}/generic/allyears/large_component/images/${slicing}_lc_diam-vs-time"

if [ -e ${lcdiamvtime}_diam.png ]
then
	echo "Plot graph of Largest Component Diamater vs. Time has already been created at :"
	echo $lcdiamvtime
	echo $linebreak
else
	args="--args net_type='lc' outpath='${lcdiamvtime}' field='${FIELD}' run='${RUN}' type='${TYPE}' csv='${stat_csv}' start_year='${START_YEAR}' end_year='${END_YEAR}'"

	echo "Creating Plot graph of Largest Component Diameter vs. Time"
	echo $linebreak
	R --slave "$args" < ../data-visualization/net_diamvstime.R
	R_Check=$?
	if [ ${R_Check} != 0 ]
	then
		echo "problem creating plot for Largest Component Diameter vs. Time"
		exit 1
	fi
fi

#plot graph of Largest Component Diameter vs. Size
lcdiamvsize="${FULL_RUN_PATH}${RUN}/output/statistics/${slicing}/generic/allyears/large_component/images/lc_diam-vs-size"

if [ -e  ${lcdiamvsize}_actual_nodes.png ] && [ -e ${lcdiamvsize}_actual_edges.png ] && [ -e ${lcdiamvsize}_percent_edges.png ] && [ -e ${lcdiamvsize}_percent_nodes.png ]
then
	echo "Plot graph of Largest Component Diameter vs. Size has already been created at :"
	echo $lcdiamvsize
	echo $linebreak
else
	args="--args net_type='lc' outpath='${lcdiamvsize}' field='${FIELD}' run='${RUN}' type='${TYPE}' csv='${stat_csv}' start_year='${START_YEAR}' end_year='${END_YEAR}'"
	
	echo "Creating Plot graph of Largest Component Diameter vs. Size"
	echo $linebreak
	R --slave "$args" < ../data-visualization/net_diamvssize.R
		R_Check=$?
	if [ ${R_Check} != 0 ]
	then
		echo "problem creating plot for Largest Component Diameter vs. Size"
		exit 1
	fi
fi


echo $linebreak
echo "PROGRAM FINISHED"
echo $linebreak
