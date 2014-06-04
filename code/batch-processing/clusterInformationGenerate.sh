#clusterInformationGenerate.sh
#Journal Frequency
. ../../parameters/parameters-global.txt
cd ../cluster-analysis/topic-areas/

python JournalFreq.py ${PATHI}
mkdir ${PATHI}keyinfo/
python ExtractKeyInformation.py ${PATHI} ${STYR} ${EDYR}

python clustersize.py ${PATHI} ${STYR} ${EDYR}