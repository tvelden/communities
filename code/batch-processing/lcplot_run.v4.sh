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
echo "ROOT_PATH = " $ROOT_PATH

#array of folders in directory tree
dir[0]="${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/${RUN}/"
dir[1]="${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/${RUN}/output/"
dir[2]="${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/${RUN}/output/networks"
dir[3]="${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/${RUN}/output/statistics"

#array of subdirectories for statistics folders
statsubdir[0]="images/"
statsubdir[1]="csv/"
statsubdir[2]="R/"

#array of subdirectories for network folders
netsubdir[0]="whole_net/"
netsubdir[1]="large_component/"
netsubdir[2]="2ndlargest_component/"

netsubsubdir[0]="net/"
netsubsubdir[1]="vector/"
netsubsubdir[2]="partition/"
netsubsubdir[3]="images/"

# time slice names
time_slice="${TYPE}${START_YEAR}-${END_YEAR}_${SIZE}years"
stat_time_slice="${dir[3]}/${time_slice}/" #statistics time slice path
net_time_slice="${dir[2]}/${time_slice}/" #networks time slice path


#creates appropriate directories
for i in "${dir[@]}"
do
	if [ -d $i ]
	then
		echo "$i already exists"
	else
		mkdir $i
		echo "$i has been created"
	fi
done

#creates appropriate directories
for i in "${dir[@]}"
do
	if [ -d $i ]
	then
		echo "$i already exists"
	else
		mkdir $i
		echo "$i has been created"
	fi
done

#creates statistics time slice
if [ -d $stat_time_slice ]
then
	echo "$stat_time_slice already exists"
else
	mkdir $stat_time_slice
	echo "$stat_time_slice has been created"
fi

#subdirectories for statistics
for i in "${statsubdir[@]}"
do
	statdir="${stat_time_slice}${i}"
	if [ -d $statdir ]
	then
		echo "$statdir already exists"
	else
		mkdir $statdir
		echo "$statdir has been created"
	fi
done

#create statistics CSV for whole network and large component network
stat_csv="${stat_time_slice}/csv/${FIELD}${RUN}${TYPE}${START_YEAR}-${ENDYEAR}_${SIZE}years_component_analysis.csv"
headers="START, END, TOTAL_SIZE_NODES, TOTAL_SIZE_EDGES, LC_SIZE_NODES, LC_SIZE_EDGES, LC_DIAM"
if [ -e $stat_csv ]
then
	echo "component_analysis csv has already been initialized"
else
	echo $headers > ${stat_csv}
fi

#create statistics csv for 2nd largest component network
snd_stat_csv="${stat_time_slice}/csv/${FIELD}${RUN}${TYPE}${START_YEAR}-${ENDYEAR}_${SIZE}years_sndcomponent_analysis.csv"
if [ -e $snd_stat_csv ]
then
	echo "component_analysis csv has already been initialized"
else
	headers2="START, END, SNDLC_SIZE_NODES, SNDLC_SIZE_EDGES, SNDLC_DIAM"	
	echo $headers2 > ${snd_stat_csv}
fi

#creates network time slice
if [ -d $net_time_slice ]
then
	echo "$net_time_slice already exists"
else
	mkdir $net_time_slice
	echo "$net_time_slice has been created"
fi

#subdirectories for networks
for i in "${netsubdir[@]}"
do
	netdir="${dir[2]}/${time_slice}/$i"
	if [ -d $netdir ]
	then
		echo "$netdir already exists"
	else
		mkdir $netdir
		for j in "${netsubsubdir[@]}"
		do
			netsubdir="${netdir}$j"
			mkdir $netsubdir
		done
		echo "$netdir has been created"
	fi
done

#check for network files in whole_net, run networkbuild.py if they don't exist
count=`ls -1 ${net_time_slice}whole_net/net/*.net  | wc -l`
echo "There are $count time slices created for these parameter settings"
if [ $count != 0 ]
then
	echo "The whole network .net files for $time_slice have already been created"
	networkbuildcheck=0
else
	echo "The whole network .net files for $time_slice have not been processed yet"
	echo "Running networkbuild.py now to create $time_slice time slices"
	cd ../build-networks/co-author
	python networkbuild.py 
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


#find network files in network/<time_slice>
fullnet=(${net_time_slice}whole_net/net/*.net)
echo "These are the whole network files that will be used"
for i in ${fullnet[*]}
do
	echo $i
done


#check if there are large component files for this run already, creates files if they don't exist
count=`ls -1 ${net_time_slice}large_component/net/*.net  | wc -l`
echo "There are $count time slices created for these parameter settings"
if [ $count != 0 ]
then
	echo "Largest Component network files have already been generated"
else
	for i in ${fullnet[*]}
	do
		args="--args filepath='$i' outpath='${dir[2]}/${time_slice}/large_component/net/' field='${FIELD}' run='${RUN}' size='${SIZE}' type='${TYPE}' csv='${stat_csv}'"
		echo "Largest Component : $i"
		R --slave "$args" < ../build-networks/co-author/lcbuild.R
		R_Check=$?
		if [ ${R_Check} != 0 ]
		then
			echo "problem running lcbuild.R for $i"
			exit 1
		fi
	done
fi

#check if there are second largest component files for this run already, creates files if they don't exist
count=`ls -1 ${net_time_slice}2ndlargest_component/net/*.net  | wc -l`
echo "There are $count time slices created for these parameter settings"
if [ $count != 0 ]
then
	echo "Second Largest Component network files have already been generated"
else
	for i in ${fullnet[*]}
	do
		args="--args filepath='$i' outpath='${dir[2]}/${time_slice}/2ndlargest_component/net/' field='${FIELD}' run='${RUN}' size='${SIZE}' type='${TYPE}' csv='${snd_stat_csv}'"
		echo "2nd Largest Component : $i"
		R --slave "$args" < ../build-networks/co-author/sndlcbuild.R
		R_Check=$?
		if [ ${R_Check} != 0 ]
		then
			echo "problem running sndlcbuild.R for $i"
			exit 1
		fi
	done
fi

#network visualizations are out until a more memory efficient method is devised

#check if large component visulization files for this run exist already,
# creates files if they don't exist
#if [ -d ${stat_time_slice}/images/visualizations/ ]
#then
#	echo "visualizations folder has already been created"
#else
#	mkdir ${stat_time_slice}/images/visualizations/
#	echo "visualization folder was created"
#fi

#lcnet=(${net_time_slice}large_component/net/*.net)
#count=`ls -1 ${stat_time_slice}images/visualizations/large_component/*.net  | wc -l`
#echo "There are $count visualizations created for these parameter settings"
#if [ $count == 0 ]
#then
#	echo "Largest Component Visualizations have already been made"
#else
#	for i in ${lcnet[*]}
#	do
#		args="--args filepath='$i' outpath='${dir[2]}/${time_slice}/large_component/images/' field='${FIELD}' run='${RUN}' size='${SIZE}' type='${TYPE}' desc='Largest Component'"
#		echo "Largest Component Visualization : $i"
#		R --slave "$args" < ../data-visualization/lcvisualization.R
#		R_Check=$?
#		if [ ${R_Check} != 0 ]
#		then
#			echo "problem running visualizations for netvisualization.R for $i"
#			exit 1
#		fi
#	done
#fi

# Plot Graph of Large Component Size vs. Time
#check if there are second largest component files for this run already, creates files if they don't exist
lcsizevtime="${dir[3]}/${time_slice}/images/lc_size-vs-time"
lcsizevtimeactual="${lcsizevtime}_actual.png"
if [ -e  $lcsizevtimeactual ]
then
	echo "Plot graph of Largest Component Size vs. Time has already been created at :"
	echo $lcsizevtimeactual
else
	args="--args net_type='lc' outpath='${lcsizevtimeactual}' field='${FIELD}' run='${RUN}' size='${SIZE}' type='${TYPE}' csv='${stat_csv}' start_year='${START_YEAR}' end_year='${END_YEAR}'"
	echo "Creating Plot graph of Large Component vs. Time at ${lcsizevtime}"
	R --slave "$args" < ../data-visualization/net_sizevstime.R
	R_Check=$?
	if [ ${R_Check} != 0 ]
	then
		echo "problem creating plot for Large Component Size vs. Time"
		exit 1
	fi
fi
