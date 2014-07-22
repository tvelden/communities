#Shell scripts to generate the directories which are need for my analysis (citation network, affinity network and so on)
. ../../parameters/parameters-global.txt
echo "These codes are used to generated the directory for the citation network and affinity network"
echo
echo "These are the parameters designated by ../../parameters/parameters-global.txt"
echo "FIELD = " $FIELD
echo "RUN = " $RUN
echo "START YEAR = " $START_YEAR
echo "END YEAR = "$END_YEAR
echo "ROOT PATH = "$ROOT_PATH
echo "-------------------------"
RAWINPUTFILE=${ROOT_PATH}/${FIELD}/data/data1/raw/
REDUCEDINPUTFILE=${ROOT_PATH}/${FIELD}/data/data1/reduced/
mkdir -p ${RAWINPUTFILE}
mkdir -p ${REDUCEDINPUTFILE}

echo "Please copy the raw inputfile into ${RAWINPUTFILE} or copy the reduced inputfile named 'in-norm-dis-hfree-red.txt' into ${REDUCEDINPUTFILE}"

echo 
echo "------------------------"
OUTPUTDIR=${ROOT_PATH}/${FIELD}/runs/${RUN}/output/

mkdir -p ${OUTPUTDIR}


echo "The output files are in ${OUTPUTDIR}"

mkdir ${OUTPUTDIR}network
mkdir ${OUTPUTDIR}statistics