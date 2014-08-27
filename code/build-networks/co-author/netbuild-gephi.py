# read in parameter variables
import sys
import os
import csv
import networkx as nx
import net_lib as nl

parameterLoc = "../../../parameters/parameters-global.txt"
linebreak1 = "<><><><><><><><><><><><><><><><><><><><><>"
linebreak2 = "_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-"
params = [] # list of parameter values
accumPajNetLocs = [] # list of all accumulative slice .net locations
accumPajVecLocs = [] # list of all accumulative slice .vec locations
discPajNetLocs = [] # list of all discrete slice .net locations
discVecNetLocs = [] # list of all discrete slice .vec locations
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
nodeFirstYear = dict() #keeps track of a node's first year in the network

#hubLoc = "../../../../TEST_dirs/nwa-field1/runs/run1norm-dis-hfree-red/output/networks/accumulative1991-2010_1years/generic/1991-2010/whole_net/hubs/field1run1norm-dis-hfree-red_accumulative1991-2010_1years_wholenet.hub"
# Only temporary until batch script is created
hubLoc = sys.argv[1]
csvLoc = sys.argv[2]
csvHeaders = ["YEAR", "totalNodes", "totalNew", "totalOld", "totalFromMixed", "newFromMixed", "oldFromMixed", "totalFromPure", "newFromPure", "oldFromPure", "totalComps", "mixedComps", "pureComps", "pureNewComps", "pureOldComps", "nodesToNewHubs", "nodesToOldHubs", "nodesNotConnectedToHub"]
hubFile = open(hubLoc, "r").readlines()
hublist = []

#create searchable list from hubFile
for hub in hubFile:
	hublist.append(hub.strip('\n').replace('\"', ''))

print "Hub List : "
j = 0
for hub in hublist:
	print "\t" + str(j) + " : "  + hub
	j += 1


_convertOnly = False # if True, script will only convert pajek files directly into gephi files without new attributes
_FIELD = '' 
_RUN = ''
_STARTYEAR = ''
_ENDYEAR = ''
_TYPE = '' # Type of run : discrete, sliding, accumulative
_SIZE = '' # size of slicing window
_NETPATH = '' # path to network output
_DATAPATH = '' # path to data

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
	pajFileName = _FIELD + _RUN + "_" + sliceName + "_wholenet.net"
	vecFileName = _FIELD + _RUN + "_" + sliceName + "_wholenet.vec"
	gephFileName = _FIELD + _RUN + "_" + sliceName + "_wholenet.gexf"
	
	#Pajek files
	pajLoc = _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/" + "networks/" + _accRunType + "/generic/" + _STARTYEAR + "-" + str(year) + "/whole_net/pajek/" + pajFileName
	vecLoc = _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/" + "networks/" + _accRunType + "/generic/" + str(year) + "-" + str(year) + "/whole_net/pajek/" + vecFileName
	accumPajNetLocs.append(pajLoc)
	accumPajVecLocs.append(vecLoc)

	#Gephi files
	gephLoc = _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/" + "networks/" + _accRunType + "/generic/" + _STARTYEAR + "-" + str(year) + "/whole_net/gephi/" + gephFileName
	accumGephNetLocs.append(gephLoc)
print linebreak1

# create list of pajek file locations in discrete slicing
for year in range(int(_STARTYEAR), int(_ENDYEAR) + 1):
	sliceName = "discrete" + str(year) + "-" + str(year) + "_" + _SIZE + "years"
	pajFileName = _FIELD + _RUN + "_" + sliceName + "_wholenet.net"
	vecFileName =_FIELD + _RUN + "_" + sliceName + "_wholenet.vec"
	gephFileName = _FIELD + _RUN + "_" + sliceName + "_wholenet.gexf"
	gephFileNameAtts = _FIELD + _RUN + "_" + sliceName + "_wholenet_Attributes.gexf"

	
	#Pajek Files
	pajLoc = _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/" + "networks/" + _discRunType + "/generic/" + str(year) + "-" + str(year) + "/whole_net/pajek/" + pajFileName
	vecLoc = _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/" + "networks/" + _discRunType + "/generic/" + str(year) + "-" + str(year) + "/whole_net/pajek/" + vecFileName
	discPajNetLocs.append(pajLoc)
	discVecNetLocs.append(vecLoc)

	#Gephi Files
	gephLoc = _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/" + "networks/" + _discRunType + "/generic/" + str(year) + "-" + str(year) + "/whole_net/gephi/" + gephFileName
	gephAttLoc = _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/" + "networks/" + _discRunType + "/generic/" + str(year) + "-" + str(year) + "/whole_net/gephi/" + gephFileNameAtts
	discGephNetLocs.append(gephLoc)
	discGephNetAttLocs.append(gephAttLoc)

# create list of networkx network objects for the accumulative slicing
print "Adding Accumulative Networks from : "
for loc in accumPajNetLocs:
	print "\t " + `loc` + "\n"
	net = nl.open_paj_as_nx(loc)
	accumNets.append(net)

# create list of networkx network objects for the discrete slicing
print "Adding Discrete Networks from : "
for loc in discPajNetLocs:
	print "\t " + `loc` + "\n"
	net = nl.open_paj_as_nx(loc)
	discNets.append(net)

print "Initializing Finished"
print linebreak1

# This block only runs if _convertOnly is set to True in the field at the top of the page.
# If this block runs, the program will exit and the rest of the code will NOT run.
# This is intended to make a quick processes when an exact copy of the pajek file is needed
# and nothing else.
if _convertOnly:
	print " CONVERTING ONLY : Writing out accumulative sliced Gephi Files"
	print linebreak2
	# Write out accumulative gephi networks
	for i in range(0, len(accumNets)):
		print "Writing out to :"
		print `accumGephNetLocs[i]`
		nl.fix_nx_edge_weight_bug(accumNets[i], 'publications')
		nx.write_gexf(accumNets[i], accumGephNetLocs[i])
		print linebreak2
	# Write out discrete gephi networks
	for i in range(0, len(discNets)-1):
		print "Writing out to :"
		print `discGephNetLocs[i]`
		nx.write_gexf(discNets[i], discGephNetLocs[i])
	sys.exit(2)

# add attributes
# 1. add OLDNEW attributes

# initalize first year
print "Setting OLDNEW attributes for..."
for n in discNets[0]:
	discNets[0].node[n]['OLDNEW'] = 'NEW'
	discNets[0].node[n]['toHub'] = 'no'
	discNets[0].node[n]['SIZEBYACTIVEYEARS'] = 1
	discNets[0].node[n]['FirstYearPub'] = _STARTYEAR
	discNets[0].node[n]['YearsSinceFirstPub'] = 0
	nodeFirstYear[n] = _STARTYEAR
	print `n`
	nodeSizeByActiveYears[n] = 1
netMetrics[years[0]]['totalNew'] = len(discNets[0])
netMetrics[years[0]]['totalNodes'] = len(discNets[0])
netMetrics[years[0]]['totalOld'] = 0
netMetrics[years[0]]['toNewHubs'] = 0 # initializing toNewHubs key and value
netMetrics[years[0]]['toOldHubs'] = 0 # initializing toOldHubs key and value
netMetrics[years[0]]['toNoHubs'] = 0 # initializing toNoHubs key and value
print "\t" + str(years[0])

# initialize rest of years
for i in range(1, len(discNets)):
	for n in discNets[i]:
		discNets[i].node[n]['toHub'] = 'no'
	for e,f in discNets[i].edges_iter():
		discNets[i].edge[e][f]['hubEdge'] = 'no'

# set OLDNEW attribute
for i in range(1, len(discNets)):
	nodes = nl.attOldNew(discNets[i], accumNets[i - 1])
	#print "New nodes = " + str(nodes[1])
	#print "Old nodes = " + str(nodes[0])
	netMetrics[years[i]]['totalNew'] = nodes[1]
	netMetrics[years[i]]['totalOld'] = nodes[0]
	netMetrics[years[i]]['totalNodes'] = nodes[0] + nodes[1]
	netMetrics[years[i]]['toNewHubs'] = 0 # initializing toNewHubs key and value
	netMetrics[years[i]]['toOldHubs'] = 0 # initializing toOldHubs key and value
	netMetrics[years[i]]['toNoHubs'] = 0
	print "\t" + str(years[i])
	for n in discNets[i]:
		if discNets[i].node[n]['OLDNEW'] == 'NEW':
			discNets[i].node[n]['FirstYearPub'] = years[i]
			nodeFirstYear[n] = years[i]
			discNets[i].node[n]['YearsSinceFirstPub'] = 0
		else:
			print `n`
			print `discNets[i].node[n]`
			discNets[i].node[n]['FirstYearPub'] = nodeFirstYear[n]
			yearsSinceFirstPub = years[i] - int(discNets[i].node[n]['FirstYearPub'])
			discNets[i].node[n]['YearsSinceFirstPub'] = yearsSinceFirstPub
print linebreak1

# 2. size nodes according to publication
print "Setting Size attributes for..."
for i in range(0, len(discPajNetLocs)):
	print "\t" + str(years[i])
	pajNet = open(discPajNetLocs[i], "r").readlines()
	pajVec = open(discVecNetLocs[i], "r").readlines()

	for j in range(0, len(pajNet)):
		lIndex = pajNet[j].find("\"") + 1
		if lIndex > 0 :
			label = pajNet[j][lIndex : len(pajNet[j])].strip('\n').replace('\"', '')
			if label in nodeSizeByPub:
				nodeSizeByPub[label] += int(pajVec[j])
				nodeSizeByActiveYears[label] += 1
			else:
				nodeSizeByPub[label] = int(pajVec[j])
				nodeSizeByActiveYears[label] = 1
			discNets[i].node[label]['SIZEBYPUB'] = nodeSizeByPub[label]
			discNets[i].node[label]['SIZEBYACTIVEYEARS'] = nodeSizeByActiveYears[label]

# 3. add Hub attributes
# NOTE : Will require passing in hubFile location as argument when script is called
# 4. add toHub attributes

print linebreak1
print "Setting Hub and toHub attributes for..."

# NOTE : TRY ITERATING THROUGH EDGES INSTEAD OF NODES
for i in range(0, len(discNets)):
	print "\t" + str(years[i])
	hubsThisYear = 0
	for n in discNets[i]:
		if n in hublist:
			discNets[i].node[n]['HUB'] = "Hub"
			hubsThisYear += 1
			for nbr in discNets[i].neighbors(n):
				discNets[i].node[nbr]['toHub'] = 'yes'
		else:
			discNets[i].node[n]['HUB'] = "nonHub"

	#print "\t" + "Hubs : " + str(hubsThisYear)
	#print "\t" + "total active nodes : " + str(len(discNets[i]))

	# loop through all nodes again to determine type of hub connections if any
	for n in discNets[i]:
		newHubConnections = 0
		oldHubConnections = 0
		if discNets[i].node[n]['OLDNEW'] == 'NEW':
			for nbr in discNets[i].neighbors(n):
				if discNets[i].node[nbr]['HUB'] == "Hub":
					if discNets[i].node[nbr]['OLDNEW'] == 'NEW':
						newHubConnections += 1
					elif discNets[i].node[nbr]['OLDNEW'] == 'OLD':
						if i == 0:
							print "THIS SHOULD NOT HAPPEN"
							print "Author is " + `discNets[i].node[nbr]`
						oldHubConnections += 1
					else:
						print "Should Not Be Here Either : " + `discNets[i].node[nbr]['OLDNEW']`
						print "Author is " + `discNets[i].node[nbr]`

			if (oldHubConnections > 0) or (newHubConnections > 0):
				if oldHubConnections > 0 :
					netMetrics[years[i]]['toOldHubs'] += 1
				else:
					netMetrics[years[i]]['toNewHubs'] += 1
			else:
				netMetrics[years[i]]['toNoHubs'] += 1
		
		
	# 5. Component Analysis
	componentMetrics = nl.puremixcomps(discNets[i])
	netMetrics[years[i]]['totalComps'] = componentMetrics[0]
	netMetrics[years[i]]['mixedComps'] = componentMetrics[1]
	netMetrics[years[i]]['pureNew'] = componentMetrics[2]
	netMetrics[years[i]]['pureOld'] = componentMetrics[3]
	netMetrics[years[i]]['newFromMixed'] = componentMetrics[4]
	netMetrics[years[i]]['oldFromMixed'] = componentMetrics[5]
	netMetrics[years[i]]['newFromPure'] = componentMetrics[6]
	netMetrics[years[i]]['oldFromPure'] = componentMetrics[7]

# 6. Group attributes by the following groups
#		- hub joined network connected to hub
#		- hub joined network connected to nonhub
#		- nonhub joined network connected to hub
#		- nonhub joined network connected to nonhub
for i in range(0, len(discNets)):
	for n in discNets[i]:
		if n not in nodeGroup:
			if discNets[i].node[n]['HUB'] == 'Hub':
				if discNets[i].node[n]['toHub'] == 'yes':
					discNets[i].node[n]['Group'] = 'hubConnectedToHub'
					nodeGroup[n] = 'hubConnectedToHub'
				elif discNets[i].node[n]['toHub'] == 'no':
					discNets[i].node[n]['Group'] = 'hubConnectedToNonHub'
					nodeGroup[n] = 'hubConnectedToNonHub'
				else:
					print "PROBLEM WITH toHub NODE ATTRIBUTE"
					sys.exit(1)
			elif discNets[i].node[n]['HUB'] == 'nonHub':
				if discNets[i].node[n]['toHub'] == 'yes':
					discNets[i].node[n]['Group'] = 'nonhubConnectedToHub'
					nodeGroup[n] = 'nonhubConnectedToHub'
				elif discNets[i].node[n]['toHub'] == 'no':
					discNets[i].node[n]['Group'] = 'nonhubConnectedToNonHub'
					nodeGroup[n] = 'nonhubConnectedToNonHub'
				else:
					print "PROBLEM WITH toHub NODE ATTRIBUTE"
					sys.exit(1)
			else:
				print "PROBLEM WITH HUB NODE ATTRIBUTE"
				sys.exit(1)
		else:
			discNets[i].node[n]['Group'] = nodeGroup[n]



# 7. Write out gexf Files and CSV files
print linebreak2
print "Writing out Gephi Files to..."
for i in range(0, len(discGephNetAttLocs)):
	print "\t" + discGephNetAttLocs[i]
	nx.write_gexf(discNets[i], discGephNetAttLocs[i])

print linebreak2
print "Writing out csv File to ..."
print "\t" + csvLoc

if os.path.exists(csvLoc):
	os.remove(csvLoc)

csvOut = csv.writer(open(csvLoc, "a"))
csvOut.writerow(csvHeaders)
for year in netMetrics:
	totalNodes = netMetrics[year]['totalNodes']
	totalNew = netMetrics[year]['totalNew']
	totalOld = netMetrics[year]['totalOld']
	totalFromMixed = netMetrics[year]['newFromMixed'] + netMetrics[year]['oldFromMixed']
	newFromMixed = netMetrics[year]['newFromMixed']
	oldFromMixed = netMetrics[year]['oldFromMixed']
	totalFromPure = netMetrics[year]['newFromPure'] + netMetrics[year]['oldFromPure']
	newFromPure = netMetrics[year]['newFromPure']
	oldFromPure = netMetrics[year]['oldFromPure']
	totalComps = netMetrics[year]['totalComps']
	mixedComps = netMetrics[year]['mixedComps']
	pureComps = netMetrics[year]['pureNew'] + netMetrics[year]['pureOld']
	pureNewComps = netMetrics[year]['pureNew']
	pureOldComps = netMetrics[year]['pureOld']
	nodesToNewHubs = netMetrics[year]['toNewHubs']
	nodesToOldHubs = netMetrics[year]['toOldHubs']
	nodesNotConnectedToHub = netMetrics[year]['toNoHubs']
	csvOut.writerow([year, totalNodes, totalNew, totalOld, totalFromMixed, newFromMixed, oldFromMixed, totalFromPure, newFromPure, oldFromPure, totalComps, mixedComps, pureComps, pureNewComps, pureOldComps, nodesToNewHubs, nodesToOldHubs, nodesNotConnectedToHub])
print linebreak2
print linebreak1
print "PROGRAM FINISHED WITHOUT ERROR"
print linebreak1

