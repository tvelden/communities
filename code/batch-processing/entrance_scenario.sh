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
csvLoc="${FULL_RUN_PATH}${RUN}/output/statistics/${discrete_slice}/generic/allyears/whole_net/tables/${FIELD}${RUN}"


linebreak1="/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/"

echo $linebreak1
echo "Running entrance_scenario.py"
cd ../community-analysis
python ./entrance_scenario.py
pyCheck=$?
cd -
if [ ${pyCheck} != 0 ]
then
	echo $linebreak1
	echo "problem running /community-analysis/entrance_scenario.py"
	echo $linebreak1
	exit 1
fi

echo $linebreak1

echo "Making plots..."
args="--args outpath='${png_path}' field='${FIELD}' run='${RUN}' type='${TYPE}' catCsv='${csvLoc}_Category.csv' scenCsv='${csvLoc}_Scenario.csv' catPercCsv='${csvLoc}_CategoryPercent.csv' scenPercCsv='${csvLoc}_ScenarioPercent.csv' start_year='${START_YEAR}' end_year='${END_YEAR}'"
echo "Args for plotting : " ${args}
R --slave "$args" < ../data-visualization/Category_And_Scenario_Vis.R
R_Check=$?
if [ ${R_Check} != 0 ]
then
	echo "problem creating plot of Category and Scenario Metrics"
	exit 1
fi