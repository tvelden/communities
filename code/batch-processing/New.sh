#!/usr/bin/python

#Shell script for the Clustering process for Direct Citation Network
echo "Clustering Begin"
. ../../parameters/parameters-global.txt
PATH=${PATHI}in.txt
PATHOUT=${PATHI}DirectCitationNetwork.net
echo "InputPath= $PATH"
echo "Begin Building Citation Network"
cd ../build-networks/document-citation
python networkbuild.py $PATH $PATHOUT
echo "Building Citation Network Complete"