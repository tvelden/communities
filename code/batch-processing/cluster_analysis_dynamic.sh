#Shell script for the Clustering process for Direct Citation Network
. ../../parameters/parameters-global.txt
RAWINPUTFILE=${ROOT_PATH}/nwa-${FIELD}/data/data1/raw/
REDUCEDINPUTFILE=${ROOT_PATH}/nwa-${FIELD}/data/data1/reduced/

echo "The process for generation of direct citation network needs the input file named 'in-norm-dis-hfree-red.txt' in ${REDUCEDINPUTFILE} or the input file named 'in.txt' in ${RAWINPUTFILE}"
echo "START YEAR =  $START_YEAR"
echo "END YEAR = $END_YEAR"

OUTPATH=${ROOT_PATH}/nwa-${FIELD}/runs/${RUN}/output/

INPUTFILE=${REDUCEDINPUTFILE}

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
    echo "Please copy the input file named 'in-norm-dis-hfree-red.txt' into ${REDUCEDINPUTFILE}"
    exit
fi
PATHIN=${INPUTFILE}
STYR=${START_YEAR}
EDYR=${END_YEAR}

PATHDCNOUT=${OUTPATH}network/accumulative${STYR}-${EDYR}/citation/
mkdir -p $PATHDCNOUT


PATHDCN=${PATHDCNOUT}DirectCitationNetwork.net

echo "------------------------------------------------------------"

echo "Begin Building Citation Network"
echo "InputFile = $PATHIN"
echo "OutputFile = $PATHDCN"
cd ../build-networks/document-citation
python networkbuild.py $PATHIN $PATHDCN $STYR $EDYR
echo "Building Citation Network Complete"

echo "------------------------------------------------------------"

PATHGC=${PATHDCNOUT}DirectCitationNetworkGiantComponent.net   #giant component
echo "Begin Finding Giant Component"
echo "InputPath = $PATHDCN"
echo "OutputPath = $PATHGC"
python FindGiantComponent.py $PATHDCN $PATHGC
echo "Finding Giant Component Complete"

echo "------------------------------------------------------------"

PATHFRPF=${PATHDCNOUT}DirectCitationNetworkGiantComponent.clu #partition file for the first round
echo "Begin First Round Clustering"
echo "InputPath = $PATHGC"
echo "OutputPath = $PATHFRPF"
cd ../../cluster-analysis/co-authors/infomap_undir
./infomap 345234 $PATHGC 10
echo "First Round Clustering Complete"

echo "------------------------------------------------------------"

PATHSHRUNK=${PATHDCNOUT}DirectCitationNetworkGiantComponent_Shrunk.net #shrunk network file
echo "Begin Shrinking"
echo "InputPath1 = $PATHGC"
echo "InputPath2 = $PATHFRPF"
echo "OutputPath = $PATHSHRUNK"
cd ../../Two\ Round\ Clustering
python NetworkShrink.py $PATHGC $PATHFRPF $PATHSHRUNK
echo "Shrinking Complete"

echo "------------------------------------------------------------"

PATHSRPF=${PATHDCNOUT}DirectCitationNetworkGiantComponent_Shrunk.clu #partition file for the second round
echo "Begin Second Round Clustering"
echo "InputPath= $PATHSHRUNK"
echo "OutputPath= $PATHSRPF"
cd ../../cluster-analysis/co-authors/infomap_undir
./infomap 345234 $PATHSHRUNK 10
echo "Second Round Clustering Complete"

echo "------------------------------------------------------------"

PATHPF=${PATHDCNOUT}DirectCitationNetworkGiantComponent_Synthe.clu #synthesized partition file
echo "Begin Two Round Partition File Mapping"
echo "InputPath1= $PATHFRPF"
echo "InputPath2= $PATHSRPF"
echo "OutputPath= $PATHPF"
cd ../../Two\ Round\ Clustering
python TwoRoundClusterMapping.py $PATHFRPF $PATHSRPF $PATHPF
echo "Two Round Cluster Mapping Complete" 

echo "------------------------------------------------------------"

PATHFPF=${PATHDCNOUT}DirectCitationNetworkGiantComponent_Synthe2.clu #final synthesized partition file
echo "Begin Partition File Mapping according to sizes"
echo "InputPath= $PATHPF"
echo "OutputPath= $PATHFPF"
python ClusterLabelTransfer.py $PATHPF $PATHFPF
echo "Partition File Mapping according to sizes Complete"

echo "------------------------------------------------------------"

echo "The two round clustering have finished. All the files can be found in ${PATHDCNOUT}"