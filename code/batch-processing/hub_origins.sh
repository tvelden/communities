#!/bin/bash

# NOTE : This program assumes that .net files exist in the appropriate directories.
#  For more information about where these files should be and how to create them refere to the
#  README file in this directory

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
discrete_slice=discrete${START_YEAR}-${END_YEAR}_${SIZE}years
accumul_slice=accumulative${START_YEAR}-${END_YEAR}_${SIZE}years
png_path="${FULL_RUN_PATH}${RUN}/output/statistics/${discrete_slice}/generic/allyears/whole_net/images/"


linebreak1="/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/"
csvLoc="${FULL_RUN_PATH}${RUN}/output/statistics/${discrete_slice}/generic/allyears/whole_net/tables/"
#hubFileLoc="../${FULL_RUN_PATH}${RUN}/output/networks/${accumul_slice}/generic/${START_YEAR}-${END_YEAR}/whole_net/hubs/${FIELD}${RUN}_accumulative${START_YEAR}-${END_YEAR}_${SIZE}years_wholenet.hub"

echo "Hub File Location : " ${hubFileLoc}
echo $linebreak1
echo "Running netbuild-gephi.py to create .gexf files..."
cd ../hub-analysis/co-author
python ./hub-metrics.py "../${csvLoc}"
pyCheck=$?
cd -
if [ ${pyCheck} != 0 ]
then
	echo $linebreak1
	echo "problem with /hub-analysis/co-author/hub-metrics.py file"
	echo $linebreak1
	exit 1
fi

echo linebreak1

echo "Making plots..."
args="--args outpath='${png_path}' field='${FIELD}' run='${RUN}' type='${TYPE}' csv='${csvLoc}Active_Years_Data.csv' start_year='${START_YEAR}' end_year='${END_YEAR}'"
echo "Args for plotting : " ${args}
R --slave "$args" < ../data-visualization/hub_origins_vis.R
R_Check=$?
if [ ${R_Check} != 0 ]
then
	echo "problem creating plot for new nodes from Mixed Components vs. Pure Components"
	exit 1
fi

