#clusterInformationGenerate.sh
#Journal Frequency
#Important information extraction
#clustersize extraction

. ../../parameters/parameters-global.txt
cd ../cluster-analysis/topic-areas/
RAWINPUTFILE=${ROOT_PATH}/nwa-${FIELD}/data/data1/raw/
REDUCEDINPUTFILE=${ROOT_PATH}/nwa-${FIELD}/data/data1/reduced/
OUTPATH=${ROOT_PATH}/nwa-${FIELD}/runs/${RUN}/output/

if [ -f ${REDUCEDINPUTFILE}in-norm-dis-hfree-red.txt ]
then
    INPUTFILE=${REDUCEDINPUTFILE}in-norm-dis-hfree-red.txt
    echo "The input file is from the reduced data directory"
elif [ -f ${RAWINPUTFILE}in.txt ]
then
    INPUTFILE=${RAWINPUTFILE}in.txt
    echo "The input file is from the raw data directory"
else
    echo "input file doesn't exists"
    echo "Please copy the input file named 'in-norm-dis-hfree-red.txt' into ${REDUCEDINPUTFILE} or copy the raw input file named "in.txt" into ${RAWINPUTFILE}"
    exit
fi



PATHIN=${INPUTFILE}
STYR=${START_YEAR}
EDYR=${END_YEAR}
PATHDCNOUT=${OUTPATH}statistics/accumulative${STYR}-${EDYR}/citation/
PATHDCNIN=${OUTPATH}network/accumulative${STYR}-${EDYR}/citation/

mkdir -p ${PATHDCNOUT}
mkdir -p ${PATHDCNOUT}JournalFreq
mkdir -p ${PATHDCNOUT}clustersize
mkdir -p ${PATHDCNOUT}keyinfo

echo "The codes will generate the Jounral Frequency information, important information for every cluster and clustersize information for direct citation network"
echo "All the information are stored in $PATHDCNOUT"

echo "------------------------------------------------------------"
echo "Begin to calculate journal frequency for every cluster"
python JournalFreq.py ${PATHIN} ${PATHDCNIN} ${PATHDCNOUT}JournalFreq/
echo "End of calculation"

echo "------------------------------------------------------------"

echo "Begin to extract key information from every cluster"
python ExtractKeyInformation.py ${PATHIN} ${PATHDCNIN} ${PATHDCNOUT}keyinfo/ ${STYR} ${EDYR}
echo "End of extraction"

echo "------------------------------------------------------------"

echo "Begin to calculate cluster size"
python clustersize.py ${PATHIN} ${PATHDCNIN} ${PATHDCNOUT}clustersize/ ${STYR} ${EDYR}
echo "End of Calculation"
