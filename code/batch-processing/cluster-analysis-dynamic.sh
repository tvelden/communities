#Shell script for the Clustering process for Direct Citation Network
. ../../parameters/parameters-global.txt

PATHIN=${PATHI}in.txt
STYR=${STYR}
EDYR=${EDYR}
PATHDCN=${PATHI}DirectCitationNetwork.net
echo "Begin Building Citation Network"
echo "InputPath = $PATHIN"
echo "OutputPath = $PATHDCN"
cd ../build-networks/document-citation
python networkbuild.py $PATHIN $PATHDCN $STYR $EDYR
echo "Building Citation Network Complete"

PATHGC=${PATHI}DirectCitationNetworkGiantComponent.net   #giant component
echo "Begin Finding Giant Component"
echo "InputPath = $PATHDCN"
echo "OutputPath = $PATHGC"
python FindGiantComponent.py $PATHDCN $PATHGC
echo "Finding Giant Component Complete"

PATHFRPF=${PATHI}DirectCitationNetworkGiantComponent.clu #partition file for the first round
echo "Begin First Round Clustering"
echo "InputPath = $PATHGC"
echo "OutputPath = $PATHFRPF"
cd ../../cluster-analysis/co-authors/infomap_undir
./infomap 345234 $PATHGC 10
echo "First Round Clustering Complete"

PATHSHRUNK=${PATHI}DirectCitationNetworkGiantComponent_Shrunk.net #shrunk network file
echo "Begin Shrinking"
echo "InputPath1 = $PATHGC"
echo "InputPath2 = $PATHFRPF"
echo "OutputPath = $PATHSHRUNK"
cd ../../Two\ Round\ Clustering
python NetworkShrink.py $PATHGC $PATHFRPF $PATHSHRUNK
echo "Shrinking Complete"

PATHSRPF=${PATHI}DirectCitationNetworkGiantComponent_Shrunk.clu #partition file for the second round
echo "Begin Second Round Clustering"
echo "InputPath= $PATHSHRUNK"
echo "OutputPath= $PATHSRPF"
cd ../../cluster-analysis/co-authors/infomap_undir
./infomap 345234 $PATHSHRUNK 10
echo "Second Round Clustering Complete"

PATHPF=${PATHI}DirectCitationNetworkGiantComponent_Synthe.clu #synthesized partition file
echo "Begin Two Round Partition File Mapping"
echo "InputPath1= $PATHFRPF"
echo "InputPath2= $PATHSRPF"
echo "OutputPath= $PATHPF"
cd ../../Two\ Round\ Clustering
python TwoRoundClusterMapping.py $PATHFRPF $PATHSRPF $PATHPF
echo "Two Round Cluster Mapping Complete" 

PATHFPF=${PATHI}DirectCitationNetworkGiantComponent_Synthe2.clu #final synthesized partition file
echo "Begin Partition File Mapping according to sizes"
echo "InputPath= $PATHPF"
echo "OutputPath= $PATHFPF"
python ClusterLabelTransfer.py $PATHPF $PATHFPF
echo "Partition File Mapping according to sizes Complete"