#clusterInformationGenerate.sh
#Journal Frequency
#Important information extraction
#clustersize extraction

. ../../parameters/parameters-global.txt
cd ../cluster-analysis/topic-areas/

REDUCEDINPUTFILE=${ROOT_PATH}${FIELD}/data/data1/reduced/
OUTPATH=${ROOT_PATH}${FIELD}/runs/${RUN}/output/

PATHIN=${REDUCEDINPUTFILE}in-norm-dis-hfree-red.txt
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
