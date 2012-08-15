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

#find network files in network/<time_slice>
cd ../cluster-analysis/co-authors/infomap_undir

#get filenames for each .net file
for i in ${years[*]}
do
	fullnet[${#fullnet[*]}]=${FULL_RUN_PATH}${RUN}/output/networks/${slicing}/generic/${i}/whole_net/pajek/${FIELD}${RUN}_${TYPE}${i}_${SIZE}years_wholenet.net
	pajekpath[${#pajekpath[*]}]=${FULL_RUN_PATH}${RUN}/output/networks/${slicing}/generic/${i}/whole_net/pajek/
	basenames[${#basenames[*]}]=${FIELD}${RUN}_${TYPE}${i}_${SIZE}years_wholenet
done

#create clustering files and move them to a different folder
echo "Clustering with Rosvall algorithm"
for i in ${fullnet[*]}
do
	make
	./infomap 345234 ../../$i 10
	if [ $? != 0 ]
	then
		echo "//////////////////------WARNING-------///////////////////"
		echo "problem with clustering $i"
		exit 1
	fi
done

cd -

echo $linebreak

echo "Running Asif's Legacy Code"
cd ../cluster-analysis/co-authors/Asif_code/
pwd

echo $linebreak
echo " "

i=0
j=0
while [ $i -lt ${#pajekpath[@]} ]
do
	echo "processing slice ${years[$i]} with networksummarize.pl"
	./networksummarize.pl ../../${pajekpath[$i]} ${basenames[$i]}
	if [ $? != 0 ]
	then
		echo "//////////////////------WARNING-------///////////////////"
		echo "There was a problem running Asif Legacy Code - networksummarize.pl"
		exit 1
	fi
	echo $linebreak
	echo "processing slice ${years[$i]} with zP.pl"
	dirname="../../${pajekpath[$i]}/${basenames[$i]}"
	outdirname="../../${FULL_RUN_PATH}${RUN}/output/networks/${slicing}/generic/${years[$i]}/whole_net/hubs/${basenames[$i]}"

	echo "dirname used is $dirname"
	echo "outdirname used is $outdirname"

	./zP.pl ${dirname} ${outdirname}

	if [ $? != 0 ]
	then
		echo "//////////////////------WARNING-------///////////////////"
		echo "There was a problem running Asif Legacy Code - zP.pl"
		exit 1
	fi
	
	echo $linebreak
	echo "processing slice ${years[$i]} hubs with hub.py"
	cd ../../../hub-analysis/co-author
	
	hubnet="../${FULL_RUN_PATH}${RUN}/output/networks/${slicing}/generic/${years[$i]}/whole_net/pajek/${basenames[$i]}.net"
	huball="../${FULL_RUN_PATH}${RUN}/output/networks/${slicing}/generic/${years[$i]}/whole_net/hubs/${basenames[$i]}.all.txt"
	hubout="../${FULL_RUN_PATH}${RUN}/output/networks/${slicing}/generic/${years[$i]}/whole_net/hubs/${basenames[$i]}.hub"

	echo "hubnet used is $hubnet"
	echo "huball used is $huball"
	echo "hubout should be $hubout"

	python hub.py $hubnet $huball $hubout
	
	if [ $? != 0 ]
	then
		echo "//////////////////------WARNING-------///////////////////"
		echo "There was a problem running hub.py for ${years[$i]}"
		exit 1
	fi

	cd -
	i=$[i+1]
	echo $linebreak
done

