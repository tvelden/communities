#!/bin/bash

# This script creates the appropriate folders for running the network analysis scripts.
# The data will need to be added to <field>/data/<data<raw,reduced,etc>/

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
DATA_DIRS=$(dirname $DATA_PATH)

#check that network path is valid
if [ -d ${ROOT_PATH}${NET_PATH} ]
then
	if [ -d ${ROOT_PATH}${NET_PATH}/nwa-${FIELD} ]
	then
		#if network path is valid begin creating the necessary directories
		echo "setting up ${ROOT_PATH}${NET_PATH}nwa-${FIELD} for network analysis"

		if [ -d ${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/data/ ]
		then
			echo "The Specified data directory is valid"
		else
			mkdir -p ${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/data/
			echo "The data path has been initialized"
			echo "The parameter file currently says that your data is ${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/data/${DATA_PATH}"
			if [ -e ${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/data/$DATA_PATH ]
			then
				echo "This data appears to exist"
			else
				echo "This data does not appear to exist.  Either change the DATA_PATH value of the parameter-global.txt file"
				echo "or place the specified data in ${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/data/${DATA_DIRS}"
			fi
		fi
	
		if [ -d ${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/ ]
		then
			echo "${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/ is a valid directory, your program runs will appear inside here"
		else 
			mkdir -p ${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/
			echo "${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/ has been created"
			echo "Your program runs will appear here"
		fi
	else
		echo "$FIELD does not appear to exist within $NET_PATH"
		mkdir -p ${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/data/
		mkdir -p ${ROOT_PATH}${NET_PATH}/nwa-${FIELD}/runs/
		echo "$FIELD has now been created for $NET_PATH"
	fi
else
	echo "The specified folder for the network path, $NET_PATH , does not exist"
fi
