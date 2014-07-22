#AffinityNetworkGenerateStep2 (dynamic affinity network)
. ../../parameters/parameters-global.txt

STYR=${START_YEAR}
EDYR=${END_YEAR}
WINDOW=${SIZE}

REDUCEDINPUTFILE=${ROOT_PATH}${FIELD}/data/data1/reduced/
OUTPATH=${ROOT_PATH}${FIELD}/runs/${RUN}/output/
NETIN=${OUTPATH}network/accumulative${STYR}-${EDYR}/affinity/
PATHDCNIN=${OUTPATH}network/accumulative${STYR}-${EDYR}/citation/

DYNETOUT=${OUTPATH}network/dynamic${STYR}-${EDYR}_${WINDOW}years/affinity/
DYSTATSOUT=${OUTPATH}statistics/dynamic${STYR}-${EDYR}_${WINDOW}years/affinity/

mkdir -p $DYNETOUT
mkdir -p $DYSTATSOUT

echo "In order to generate the dynamic affinity network, you should first run the AffinityNetworkGenerateStep1 successfully."
echo "Then you have to open the AccumulativeNetworkAuthor.gexf and AccumulativeNetworkCitation in $NETIN,"
echo "change the layouts in the gephi files and saved them named AccumulativeNetworkAuthorChanged and AccumulativeNetworkCitationChanged in the same directory"

echo "------------------------------------------------------------"

if [ -f ${NETIN}AccumulativeNetworkAuthorChanged.gexf ] && [ -f ${NETIN}AccumulativeNetworkCitationChanged.gexf ]
then 
    echo "Generation begin"
else
    echo "Please change the layouts of the accumulative network"
    read -p "If the layout files are generated, Press [Enter] key to continue"
fi

grep "<viz:pos" ${NETIN}AccumulativeNetworkAuthorChanged.gexf  >${NETIN}positionAuthor
grep "<viz:pos" ${NETIN}AccumulativeNetworkCitationChanged.gexf  >${NETIN}positionCitation

cd ../cluster-analysis/topic-areas/

python Zoomout.py ${NETIN}positionAuthor ${DYNETOUT}layoutAuthor
python Zoomout.py ${NETIN}positionCitation ${DYNETOUT}layoutCitation
echo "The layouts are stored in $DYNETOUT"




echo "Begin to generate the affinity network for each time slices between $STYR and $EDYR with the window $WINDOW years"
python AffinityNetworkGenerate.py ${REDUCEDINPUTFILE}in-norm-dis-hfree-red.txt ${DYNETOUT} ${DYSTATSOUT} ${PATHDCNIN}DirectCitationNetworkGiantComponent.net ${PATHDCNIN}DirectCitationNetworkGiantComponent_Synthe2.clu ${WINDOW} ${STYR} ${EDYR}

python AffinityNetworkPajektoGephi.py $DYNETOUT $DYSTATSOUT $DYNETOUT ${DYNETOUT}layoutAuthor Authors ${STYR} ${EDYR} ${SIZE}
python AffinityNetworkPajektoGephi.py $DYNETOUT $DYSTATSOUT $DYNETOUT ${DYNETOUT}layoutCitation Citation ${STYR} ${EDYR} ${SIZE}

python AffinityNetworkPajektoGephiNotFix.py $DYNETOUT $DYSTATSOUT $DYNETOUT ${DYNETOUT}layoutAuthor Authors ${STYR} ${EDYR} ${SIZE}
python AffinityNetworkPajektoGephiNotFix.py $DYNETOUT $DYSTATSOUT $DYNETOUT ${DYNETOUT}layoutCitation Citation ${STYR} ${EDYR} ${SIZE}

echo "The dynamic affinty network is generated"
echo "All the pajek .net files for every time slice can be found in $DYNETOUT, the statistics information about them are in $DYSTATSOUT."
echo "The dynamic gephi files ( fixed version and nofixed version) are stored in $DYNETOUT."





