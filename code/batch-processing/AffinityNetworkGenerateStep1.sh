# #AffinityNetworkGenerateStep1
. ../../parameters/parameters-global.txt
#PATHI=/Users/shiyansiadmin/Dropbox/Files/Field2DataSS1/
mkdir ${PATHI}affinity
mkdir ${PATHI}affinity2
cd ../cluster-analysis/topic-areas/
STYR=${STYR}
EDYR=${EDYR}
let "window=${EDYR}-${STYR}+1"
python AffinityNetworkGenerate.py ${PATHI}in.txt ${PATHI}affinity/ ${PATHI}DirectCitationNetworkGiantComponent.net ${PATHI}DirectCitationNetworkGiantComponent_Synthe2.clu ${window} ${STYR} ${EDYR}
python transferPajektoGephi.py ${PATHI}affinity/Authors\ ${STYR}-${EDYR}.net ${PATHI}affinity/NumberOfPapers${STYR}-${EDYR} ${PATHI}affinity/AccumulativeNetworkAuthor.gexf
python transferPajektoGephi.py ${PATHI}affinity/Citation\ ${STYR}-${EDYR}.net ${PATHI}affinity/NumberOfPapers${STYR}-${EDYR} ${PATHI}affinity/AccumulativeNetworkCitation.gexf





# PATHI1=/Users/shiyansiadmin/Dropbox/Files/Field2DataSS1/
# mkdir ${PATHI1}affinity
# mkdir ${PATHI1}affinity2
# cd ../cluster-analysis/topic-areas/
# python AffinityNetworkGenerate.py ${PATHI1}in.txt ${PATHI1}affinity/ ${PATHI1}DirectCitationNetworkGiantComponent.net ${PATHI1}DirectCitationNetworkGiantComponent_Synthe2.clu 8 1991 1998
# python transferPajektoGephi.py ${PATHI1}affinity/Authors\ 1991-1998.net ${PATHI1}affinity/NumberOfPapers1991-1998 ${PATHI1}affinity/AccumulativeNetworkAuthor.gexf
# python transferPajektoGephi.py ${PATHI1}affinity/Citation\ 1991-1998.net ${PATHI1}affinity/NumberOfPapers1991-1998 ${PATHI1}affinity/AccumulativeNetworkCitation.gexf

# PATHI2=/Users/shiyansiadmin/Dropbox/Files/Field2DataSS2/
# mkdir ${PATHI2}affinity
# mkdir ${PATHI2}affinity2
# cd ../cluster-analysis/topic-areas/
# python AffinityNetworkGenerate.py ${PATHI2}in.txt ${PATHI2}affinity/ ${PATHI2}DirectCitationNetworkGiantComponent.net ${PATHI2}DirectCitationNetworkGiantComponent_Synthe2.clu 8 1998 2005
# python transferPajektoGephi.py ${PATHI2}affinity/Authors\ 1998-2005.net ${PATHI2}affinity/NumberOfPapers1998-2005 ${PATHI2}affinity/AccumulativeNetworkAuthor.gexf
# python transferPajektoGephi.py ${PATHI2}affinity/Citation\ 1998-2005.net ${PATHI2}affinity/NumberOfPapers1998-2005 ${PATHI2}affinity/AccumulativeNetworkCitation.gexf

# PATHI3=/Users/shiyansiadmin/Dropbox/Files/Field2DataSS3/
# mkdir ${PATHI3}affinity
# mkdir ${PATHI3}affinity2
# cd ../cluster-analysis/topic-areas/
# python AffinityNetworkGenerate.py ${PATHI3}in.txt ${PATHI3}affinity/ ${PATHI3}DirectCitationNetworkGiantComponent.net ${PATHI3}DirectCitationNetworkGiantComponent_Synthe2.clu 8 2005 2012
# python transferPajektoGephi.py ${PATHI3}affinity/Authors\ 2005-2012.net ${PATHI3}affinity/NumberOfPapers2005-2012 ${PATHI3}affinity/AccumulativeNetworkAuthor.gexf
# python transferPajektoGephi.py ${PATHI3}affinity/Citation\ 2005-2012.net ${PATHI3}affinity/NumberOfPapers2005-2012 ${PATHI3}affinity/AccumulativeNetworkCitation.gexf






# # python AffinityNetworkGenerate.py ${PATHI}in.txt ${PATHI}affinity/ ${PATHI}DirectCitationNetworkGiantComponent.net ${PATHI}DirectCitationNetworkGiantComponent_Synthe2.clu 22
# # python AffinityNetworkGenerate.py ${PATHI}in.txt ${PATHI}affinity2/ ${PATHI}DirectCitationNetworkGiantComponent.net ${PATHI}DirectCitationNetworkGiantComponent_Synthe2.clu 5

# python AffinityNetworkGenerate.py ${PATHI}in.txt ${PATHI}affinity3/ ${PATHI}DirectCitationNetworkGiantComponent.net ${PATHI}DirectCitationNetworkGiantComponent_Synthe2.clu 22 1991 2012
# python AffinityNetworkGenerate.py ${PATHI}in.txt ${PATHI}affinity4/ ${PATHI}DirectCitationNetworkGiantComponent.net ${PATHI}DirectCitationNetworkGiantComponent_Synthe2.clu 5 1991 2012
# python transferPajektoGephi.py ${PATHI}affinity3/Authors\ 1991-2012.net ${PATHI}affinity/NumberOfPapers1991-2012 ${PATHI}affinity3/AccumulativeNetworkAuthor.gexf
# python transferPajektoGephi.py ${PATHI}affinity3/Citation\ 1991-2012.net ${PATHI}affinity/NumberOfPapers1991-2012 ${PATHI}affinity3/AccumulativeNetworkCitation.gexf
