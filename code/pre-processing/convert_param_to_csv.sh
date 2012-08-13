#!/bin/bash

#refers to communities/parameters/parameters-global.txt to .csv

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

csv="../../parameters/parameters-global.csv"

if [ -e $csv ]
then
	echo "${csv} already exists"
else
	touch ${csv}
	echo "FIELD; RUN; START_YEAR; END_YEAR; TYPE; SIZE; NET_PATH; DATA_PATH" > ${csv}
	echo "${FIELD}; ${RUN}; ${START_YEAR}; ${END_YEAR}; ${TYPE}; ${SIZE}; ${NET_PATH}; ${DATA_PATH}" >> ${csv}
	echo "${csv} has been created"
fi

