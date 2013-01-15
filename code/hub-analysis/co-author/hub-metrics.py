# read in parameter variables
import sys
import os
import csv
import networkx as nx
#import net_lib as nl

_convertOnly = False # if True, script will only convert pajek files directly into gephi files without new attributes
_FIELD = '' 
_RUN = ''
_STARTYEAR = ''
_ENDYEAR = ''
_TYPE = '' # Type of run : discrete, sliding, accumulative
_SIZE = '' # size of slicing window
_NETPATH = '' # path to network output
_DATAPATH = '' # path to data

parameterLoc = "../../../parameters/parameters-global.txt"
linebreak1 = "<><><><><><><><><><><><><><><><><><><><><>"
linebreak2 = "_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-"
params = [] # list of parameter values
accumGephNetLocs = [] # list of all accumulative slice .gexf locations, for output
discGephNetLocs = [] # list of all discrete slice .gexf locations, for output
accumNets = [] # list of accumulative networkx objects 
discNets = [] # list of discrete networkx objects
discGephNetAttLocs = [] # list of discrete gexf network locations with attributes, for output
netMetrics = dict() # 2D dictionary with first key as year of network, and 2nd key as type of metric for network
years = [] # years of network, just for indexing
nodeSizeByPub = dict() # keeps track of a node's most recent number of publications
nodeSizeByActiveYears = dict() # keeps track of a node's most recent number of active years
nodeGroup = dict() # keeps track of a node's group

hubsLoc = [] # list of the location of the hub lists for each year starting with the start_year
hubLists = [] # list of hub lists
accKnownHubs = dict() # accumulative list of hubs, number of active years when entering the network, number of years since first published, number of publications
csv1Loc = sys.argv[1] + _FIELD + _RUN + "Active_Years_Data.csv" # keeps track of csv for number of active years and number of years since first published
differentiationListLoc = sys.argv[1] + _FIELD + _RUN + "_Unrecognized_Hublist.csv"# keeps track of csv for number of publications per person
diffList = []
csvHeaders = ["hubName", "YEAR", "firstYearPub", "yearsSinceFirstPub", "activeYears", "numPublished"]
hubDict = dict() # key is the year of the hub list, value is list of hubs for that year
#create searchable list from hubFile
#for hub in hubFile:
#	hublist.append(hub.strip('\n').replace('\"', ''))



try:
	param = open(parameterLoc)
except:
	print "Problem opening parameter file at " + parameterLoc
	sys.exit(1)

print linebreak1
print "Parameter File Opened Successfully"
print linebreak1

for line in param:
	index = line.index('=') + 1
	params.append(line[index:].rstrip())
param.close()

_FIELD = params[0]
_RUN = params[1]
_STARTYEAR = params[2]
_ENDYEAR = params[3]
_TYPE = params[4]
_SIZE = params[5]
_NETPATH = params[6]
_DATAPATH = params[7]

_accRunType = "accumulative" + _STARTYEAR + "-" + _ENDYEAR + "_" + _SIZE + "years"
_discRunType = "discrete" + _STARTYEAR + "-" + _ENDYEAR + "_" + _SIZE + "years"

print linebreak2
print "PARAMETERS : \n"
print "Field = " + `_FIELD`
print "Run = " + `_RUN`
print "Start Year = " + `_STARTYEAR`
print "End Year = " + `_ENDYEAR`
print "Type = " + `_TYPE`
print "Size = " + `_SIZE`
print "Net Path = " + `_NETPATH`
print "Data Path = " + `_DATAPATH`
print linebreak2
print linebreak1
print "Initializing..."
# create list of pajek file locations in accumulative slicing
for year in range(int(_STARTYEAR), int(_ENDYEAR) + 1):
	years.append(year)
	netMetrics[year] = dict()
	sliceName = "accumulative" + _STARTYEAR + "-" + str(year) + "_" + _SIZE + "years"
	gephFileName = _FIELD + _RUN + "_" + sliceName + "_wholenet.gexf"
	hubFileName = _FIELD + _RUN + "_" + sliceName + "_wholenet.hub"


	#Hub Files
	hubLoc = "../../../" + _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/" + "networks/" + _accRunType + "/generic/" + _STARTYEAR + "-" + str(year) + "/whole_net/hubs/" + hubFileName
	hubsLoc.append(hubLoc)

	#Gephi files
	gephLoc = "../../../" + _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/" + "networks/" + _accRunType + "/generic/" + _STARTYEAR + "-" + str(year) + "/whole_net/gephi/" + gephFileName
	accumGephNetLocs.append(gephLoc)
print linebreak1

# create list of pajek file locations in discrete slicing
for year in range(int(_STARTYEAR), int(_ENDYEAR) + 1):
	sliceName = "discrete" + str(year) + "-" + str(year) + "_" + _SIZE + "years"
	gephFileName = _FIELD + _RUN + "_" + sliceName + "_wholenet.gexf"
	gephFileNameAtts = _FIELD + _RUN + "_" + sliceName + "_wholenet_Attributes.gexf"

	#Gephi Files
	gephLoc = "../../../" + _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/" + "networks/" + _discRunType + "/generic/" + str(year) + "-" + str(year) + "/whole_net/gephi/" + gephFileName
	gephAttLoc = "../../../" + _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/" + "networks/" + _discRunType + "/generic/" + str(year) + "-" + str(year) + "/whole_net/gephi/" + gephFileNameAtts
	discGephNetLocs.append(gephLoc)
	discGephNetAttLocs.append(gephAttLoc)

# import gephi .gexf files
for loc in discGephNetAttLocs:
	discNets.append(nx.read_gexf(loc))

# track hub lists in a list
print "Hub Locations : "
for hList in hubsLoc:
	print "\t" + hList
	#create searchable list from hubFile
	print 
	hublist = []
	hubFile = open(hList, "r").readlines()
	for hub in hubFile:
		hublist.append(hub.strip('\n').replace('\"', ''))
	hubLists.append(hublist)

print "Initializing Finished"
print linebreak1



print linebreak1
print "Calculating Hub Origins"
# determine whether nodes differentiated as hubs ever become non-hubs again
numYears = int(_ENDYEAR) - int(_STARTYEAR)
for i in range(0, numYears):
	print i
	print "year: " + str(years[i])
	for hub in hubLists[i]:
		if hub not in hubLists[i+1]:
			diffList.append(hub)
			#print "Hub : " + hub + " is added to diffList"
		if hub not in accKnownHubs.keys():
			if hub in discNets[i].nodes():
				fYear = discNets[i].node[hub]['FirstYearPub']
				yearsSince = discNets[i].node[hub]['YearsSinceFirstPub']
				aYears = discNets[i].node[hub]['SIZEBYACTIVEYEARS']
				numPub = discNets[i].node[hub]['SIZEBYPUB']
				accKnownHubs[hub] = dict(YEAR=years[i], firstYearPub=fYear, yearsSinceFirstPub=yearsSince, activeYears=aYears, numPublished=numPub)
				#print "Hub : " + hub + " has been added to the list in " + str(accKnownHubs[hub]['YEAR'])
		#	else:
				#print "Hub : " + hub + " was not in network for this year"
		#else:
			#print "Hub : " + hub + " is already in the list"
#write out csv
if(os.path.exists(csv1Loc)):
	os.remove(csv1Loc)
if(os.path.exists(differentiationListLoc)):
	os.remove(differentiationListLoc)

csvOut=csv.writer(open(csv1Loc, "a"))
diffListOut=open(differentiationListLoc, "a")
print "csv location : "
print "\t" + csv1Loc
print "Differentiation List : "
print "\t" + differentiationListLoc
csvOut.writerow(csvHeaders)

for hub in accKnownHubs:
	#print "Hub : " + hub
	#print "Year : " + str(accKnownHubs[hub]['YEAR'])
	csvOut.writerow([hub, accKnownHubs[hub]['YEAR'], accKnownHubs[hub]['firstYearPub'], accKnownHubs[hub]['yearsSinceFirstPub'], accKnownHubs[hub]['activeYears'], accKnownHubs[hub]['numPublished']])

for hub in diffList:
	diffListOut.write(hub)
print "PROGRAM FINISHED"


