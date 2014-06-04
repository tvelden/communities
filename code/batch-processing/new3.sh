echo "Clustering Begin"
. ../../parameters/parameters-global.txt
PATHT=${PATHI}in.txt
PATHOUT=${PATHI}DirectCitationNetwork.net
# echo "InputPath= $PATH"
echo "Begin Building Citation Network"
cd ../build-networks/document-citation
pwd
python networkbuild.py /Users/shiyansiadmin/Dropbox/Files/OldField2Data2/in.txt /Users/shiyansiadmin/Dropbox/Files/OldField2Data2/DirectCitationNetwork.net


