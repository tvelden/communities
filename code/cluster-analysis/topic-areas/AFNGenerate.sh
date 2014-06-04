# shell script to generate different affinity network
echo "Generate the first one"

inputfile=/Users/shiyansiadmin/Dropbox/Files/Field3Data1/in.txt
outputdir=/Users/shiyansiadmin/Dropbox/Files/Field3Data1/affinity/
giantcomponent=/Users/shiyansiadmin/Dropbox/Files/Field3Data1/DirectCitationNetworkGiantComponent.net
partitionfile=/Users/shiyansiadmin/Dropbox/Files/Field3Data1/DirectCitationNetworkGiantComponent_Synthe2.clu

python AffinityNetworkGenerate.py $inputfile $outputdir $giantcomponent $partitionfile

# echo "Generate the second one"

# nputfile=/Users/shiyansiadmin/Dropbox/Files/OldField2Data2/in.txt
# outputdir=/Users/shiyansiadmin/Dropbox/Files/OldField2Data2/affinity2/
# giantcomponent=/Users/shiyansiadmin/Dropbox/Files/OldField2Data2/DirectCitationNetworkGiantComponent.net
# partitionfile=/Users/shiyansiadmin/Dropbox/Files/article-cluster-area-Synthe.clu

# python AffinityNetworkGenerate.py $inputfile $outputdir $giantcomponent $partitionfile