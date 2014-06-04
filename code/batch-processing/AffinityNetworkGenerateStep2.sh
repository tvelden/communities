#AffinityNetworkGenerateStep2
. ../../parameters/parameters-global.txt


grep "<viz:pos" ${PATHI}/affinity/AccumulativeNetworkAuthorChanged.gexf  >${PATHI}/affinity/positionAuthor
grep "<viz:pos" ${PATHI}/affinity/AccumulativeNetworkCitationChanged.gexf  >${PATHI}/affinity/positionCitation

cd ../cluster-analysis/topic-areas/

#python AffinityNetworkGenerate.py ${PATHI}in.txt ${PATHI}affinity2/ ${PATHI}DirectCitationNetworkGiantComponent.net ${PATHI}DirectCitationNetworkGiantComponent_Synthe2.clu 5 ${STYR} ${EDYR}

python Zoomout.py ${PATHI}/affinity/positionAuthor ${PATHI}/affinity2/layoutAuthor
python Zoomout.py ${PATHI}/affinity/positionCitation ${PATHI}/affinity2/layoutCitation

python AffinityNetworkPajektoGephi.py ${PATHI}/affinity2/ ${PATHI}/affinity2/layoutAuthor Authors ${STYR} ${EDYR} 5
python AffinityNetworkPajektoGephi.py ${PATHI}/affinity2/ ${PATHI}/affinity2/layoutCitation Citation ${STYR} ${EDYR} 5

python AffinityNetworkPajektoGephiNotFix.py ${PATHI}/affinity2/ ${PATHI}/affinity2/layoutAuthor Authors ${STYR} ${EDYR} 5
python AffinityNetworkPajektoGephiNotFix.py ${PATHI}/affinity2/ ${PATHI}/affinity2/layoutCitation Citation ${STYR} ${EDYR} 5
