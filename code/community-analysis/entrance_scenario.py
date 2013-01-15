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

parameterLoc = "../../parameters/parameters-global.txt"
linebreak1 = "<><><><><><><><><><><><><><><><><><><><><>"
linebreak2 = "_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-"
params = [] # list of parameter values
discNets = [] # list of discrete networkx objects
discGephNetAttLocs = [] # list of discrete gexf network locations with attributes, for output
years = [] # years of network, just for indexing
newNodes = [] # amount of new authors in a given year, first index correspondes with first index of year list
totals = [] # total nodes in a given year
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
_Catcsv = "../../" + _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/statistics/" + _discRunType + "/generic/" + "allyears/whole_net/tables/" + _FIELD + _RUN + "_Category.csv"
_Scencsv = "../../" + _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/statistics/" + _discRunType + "/generic/" + "allyears/whole_net/tables/" + _FIELD + _RUN + "_Scenario.csv"
_CatPerCsv = "../../" + _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/statistics/" + _discRunType + "/generic/" + "allyears/whole_net/tables/" + _FIELD + _RUN + "_CategoryPercent.csv"
_ScenPerCsv = "../../" + _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/statistics/" + _discRunType + "/generic/" + "allyears/whole_net/tables/" + _FIELD + _RUN + "_ScenarioPercent.csv"
csvHeaders = ["YEAR", "A", "B", "C", "D", "E", "F", "G", "H", "0", "1", "2", "3", "4"]
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

def catA(net, comp): # Pure New
	""" This method maps the nodes of a component determined to be in Category A to it's
		appropriate scenario.

		Pre-conditions:
			net : the networkx network object containing the component
			comp : the list of nodes in the component
	"""
	catAmount = 0
	scenAmount = 0
	for n in comp:
		net.node[n]['category'] = 'A'
		net.node[n]['scenario'] = '2'
		catAmount +=1
		scenAmount +=1
	return catAmount, scenAmount

def catB(net, comp): # Pure Old
	""" This method maps the nodes of a component determined to be in Category B to it's
		appropriate scenario.

		Pre-conditions:
			net : the networkx network object containing the component
			comp : the list of nodes in the component
	"""
	cat = 0
	scen0 = 0
	for n in comp:
		net.node[n]['category'] = 'B'
		net.node[n]['scenario'] = '0'
		cat += 1
		scen0 += 1

	return cat, scen0

def catC(net, comp): # Mixed with no hub
	""" This method maps the nodes of a component determined to be in Category C to it's
		appropriate scenario.
	"""
	cat = 0
	scen4 = 0
	scen0 = 0
	for n in comp:
		net.node[n]['category'] = 'C'
		cat += 1
		if net.node[n]['OLDNEW'] == 'NEW':
			net.node[n]['scenario'] = '4'
			scen4 += 1
		else:
			net.node[n]['scenario'] = '0'
			scen0 += 1
	return cat, scen4, scen0
def catD(net, comp): # Mixed with no new nodes connecting to a hub
	cat = 0
	scen4 = 0
	scen0 = 0

	for n in comp:
		net.node[n]['category'] = 'D'
		cat += 1
		if net.node[n]['OLDNEW'] == 'NEW':
			net.node[n]['scenario'] = '4'
			scen4 += 1
		else:
			net.node[n]['scenario'] = '0'
			scen0 += 1
	return cat, scen4, scen0

def catE(net, comp): # Mixed with only new hubs
	cat = 0
	scen4 = 0
	scen0 = 0
	for n in comp:
		net.node[n]['category'] = 'E'
		cat += 1
		if net.node[n]['OLDNEW'] == 'NEW':
			net.node[n]['scenario'] = '4'
			scen4 += 1
		else:
			net.node[n]['scenario'] = '0'
			scen0 += 1
	return cat, scen4, scen0

def catF(net, comp, oHubs): # Mixed with new hub and old hub, but no new hub directly connects to old hub
		cat = len(comp)
		scen1 = 0
		scen0 = 0
		scen4 = 0

		nodes = comp #make new list of nodes that are in the component
		#print "new component list is " + str(len(nodes)) + " long"
		#for node in comp:
		#	print "node : " + `node`
		for hub in oHubs: # find new author to old hub connections and map to scenario 1
			net.node[hub]['category'] = 'F'
			#print 'Hub : ' + hub
			for nbr in net.neighbors(hub):
				#print "\t" + `nbr`
				if net.node[nbr]['OLDNEW'] == 'NEW':
					try:
						comp.remove(nbr)
					except ValueError:
						pass
					else:
						scen1 += 1
						net.node[nbr]['category'] = 'F'
						net.node[nbr]['scenario'] = '1'
		for n in comp:
			net.node[n]['category'] = 'F'
			if net.node[n]['OLDNEW'] == 'NEW': # new node not connected to old hub
				scen4 += 1
				net.node[n]['scenario'] = '4'
			else:
				scen0 += 1
				net.node[n]['scenario'] = '0' # old node
		return cat, scen1, scen0, scen4

def catG(net, comp, newHubToOldHub, newHubs, oldHubs): # Mixed Component with new hub connecting to an old hub
	print "Category G appears"
	#for auth in comp:
	#	print "\tAuthor: " + auth
	cat = len(comp)
	scen1 = 0
	scen3 = 0
	scen4 = 0
	scen0 = 0
	nodes = comp # make new component node list
	for n in comp: #set Category to 'G'
		net.node[n]['category'] = 'G'
	for nHub, oHub in newHubToOldHub:
		nHubIsScen3 = False
		newAuthorNbrlst = [] # new author neighbor list for this new hub
		for nbr in net.neighbors(nHub):
			if net.node[nbr]['OLDNEW'] == 'NEW':
				newAuthorNbrlst.append(nbr)
		for naNbr in newAuthorNbrlst: # refine new author neighbor list
			oHubConnection = False
			shouldRemove = False
			for naNbrNbr in net.neighbors(naNbr):
				if net.node[naNbrNbr]['HUB'] == 'Hub' and net.node[naNbrNbr]['OLDNEW'] == 'OLD':
					oHubConnection=True
				if naNbrNbr not in net.neighbors(nHub) and (naNbrNbr != nHub):
					shouldRemove=True
			if shouldRemove:
				#print "New Author Neighbor, " + naNbr + ", has been removed"
				#print "\tneighbor is " + naNbrNbr
				newAuthorNbrlst.remove(naNbr)
				nodes.remove(naNbr)
				if oHubConnection:
				#	print "\tCounted as Scenario 1"
					net.node[naNbr]['scenario'] = '1'
					scen1 += 1
				else:
				#	print "\tCounted as Scenario 4"
					net.node[naNbr]['scenario'] = '4'
					scen4 +=1
		if len(newAuthorNbrlst) > 0:
			#print ("potential scenario 3s")
			for naNbr in newAuthorNbrlst:  # evaluate which group node is likely more a part of
				nHubEdgeStrength = net[naNbr][nHub]['publications']
				oHubEdgeStrength = 0
				for nbr2 in net.neighbors(naNbr):
					if net.node[nbr2]['HUB'] == 'Hub' and net.node[nbr2]['OLDNEW'] == 'OLD':
						oHubEdgeStrength = net[naNbr][nbr2]['publications']
			#	print "For new hub, " + nHub + ",  old hub, " + oHub + ", and new author, " + naNbr + " :"
			#	print "\t New Hub Edge Strength = " + str(nHubEdgeStrength)
			#	print "\t Old Hub Edge Strength = " + str(oHubEdgeStrength)
				if nHubEdgeStrength > oHubEdgeStrength:
					net.node[naNbr]['scenario'] = '3'
					nodes.remove(naNbr)
					scen3 += 1
					nHubIsScen3 = True
				elif nHubEdgeStrength < oHubEdgeStrength:
					net.node[naNbr]['scenario'] = '1'
					scen1 += 1
					nodes.remove(naNbr)
				else:  # TIE BREAKER
					net.node[naNbr]['scenario'] = '1'
					scen1 += 1
					nodes.remove(naNbr)
					nHubIsScen3 = True
			if nHubIsScen3:
				net.node[nHub]['scenario'] = '3'
			#	print "Research Group Found with " + nHub
				scen3 += 1
				nodes.remove(nHub)
		for n in nodes:
			if net.node[n]['OLDNEW'] == 'OLD':
				net.node[n]['scenario'] = '0'
				scen0 += 1
			else: # find if connected to old hub or neither hub
				oldHubFound = False
				newHubFound = False
				for nbr in net.neighbors(n):
					if net.node[nbr]['HUB'] == 'Hub':
						if net.node[nbr]['OLDNEW'] == 'NEW':
							newHubFound = True
						else:
							oldHubFound = True
				if not oldHubFound and not newHubFound:
					net.node[n]['scenario'] = '4'
					scen4 += 1
				elif newHubFound and not oldHubFound:
					net.node[n]['scenario'] = '4'
				elif oldHubFound and not newHubFound:
					net.node[n]['scenario'] = '1'
				else:
					print "New Node Connected to both new hub and old hub, should have been handled earlier"
					print "\t Node is " + n

		return cat, scen1, scen3, scen4, scen0


def catH(net, comp, oHubs): # Mixed Component with only Old Hubs
	""" This method is used to simplify the procedure for components that fall into Category H.
		A category H component has only old hubs and no new hubs.  All old nodes in the components
		should be mapped to scenario 0, new nodes connecting to the old hubs should be mapped to
		scenario 1, and new nodes not connected to an old hub should be mapped to scenario 4.

		Pre-conditions:
			net : the networkx network object containing the component
			comp : the list of nodes in the component
			oHubs : the list of old hub nodes in the component
	"""
	cat = len(comp)
	scen1 = 0
	scen4 = 0
	scen0 = 0
	nodes = comp #make new list of nodes that are in the component
	for hub in oHubs: # find new author to old hub connections and map to scenario 1
		net.node[hub]['category'] = 'H'
		for nbr in net.neighbors(hub):
			if net.node[nbr]['OLDNEW'] == 'NEW':
				try:
					nodes.remove(nbr)
				except ValueError:
					pass
				else:
					net.node[nbr]['category'] = 'H'
					net.node[nbr]['scenario'] = '1'
					scen1 += 1
	for n in nodes:
		net.node[n]['category'] = 'H'
		if net.node[n]['OLDNEW'] == 'NEW': # new node not connected to old hub
			net.node[n]['scenario'] = '4'
			scen4 += 1
		else:
			net.node[n]['scenario'] = '0' # old node
			scen0 += 1
	return cat, scen1, scen4, scen0


# create list of pajek file locations in discrete slicing
for year in range(int(_STARTYEAR), int(_ENDYEAR) + 1):
	years.append(year)
	sliceName = "discrete" + str(year) + "-" + str(year) + "_" + _SIZE + "years"
	gephFileNameAtts = _FIELD + _RUN + "_" + sliceName + "_wholenet_Attributes.gexf"

	#Gephi Files
	gephAttLoc = "../../" + _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/networks/" + _discRunType + "/generic/" + str(year) + "-" + str(year) + "/whole_net/gephi/" + gephFileNameAtts
	discGephNetAttLocs.append(gephAttLoc)

# import gephi .gexf files
for loc in discGephNetAttLocs:
	print 'loc : ' + "\n\t" + loc
	discNets.append(nx.read_gexf(loc))
sliceName = "accumulative" + _STARTYEAR + "-" + _ENDYEAR + "_" + _SIZE + "years"
gephAccFileName = _FIELD + _RUN + "_" + sliceName + "_wholenet.gexf"
gephAccumFinalNetLoc = "../../" + _NETPATH + "/nwa-" + _FIELD + "/runs/" + _RUN + "/output/networks/" + _accRunType + "/generic/" + _STARTYEAR + "-" + _ENDYEAR + "/whole_net/gephi/" + gephAccFileName
_gephAccNet = nx.read_gexf(gephAccumFinalNetLoc)
print linebreak1
print "Initialization Finished"
print linebreak1

_metrics = dict() # dictionary for keeping track of category and scenario numbers for each year
for year in years:
	_metrics[year] = dict(A=0, B=0, C=0, D=0, E=0, F=0, G=0, H=0, zero=0, one=0, two=0, three=0, four=0)

# 1. Set edge final publications attribute
#for i in range(0, len(discNets)):
#	for e in discNets[i].edges():
#		pubs = _gephAccNet[e[0]][e[1]]['publications']
#		discNets[i][e[0]][e[1]]['publications'] = pubs
#	nx.write_gexf(discNets[i], discGephNetAttLocs[i])

# 2. find all pure new components and label all nodes
for i in range(0, len(discNets)):
	# Tally New Authors
	news = 0
	totals.append(len(discNets[i].nodes()))
	for n in discNets[i]:
		if discNets[i].node[n]['OLDNEW'] == 'NEW':
			news += 1
	newNodes.append(news)

	print "Year : " + str(years[i])
	comps = nx.connected_components(discNets[i]) # list of node lists for each component
	for comp in comps: # cycle through each comp
		numNews = 0
		numOlds = 0
		hubsInComp = []
		for n in comp:
			if discNets[i].node[n]['OLDNEW'] == 'NEW':
				numNews += 1
			else:
				numOlds += 1
			if discNets[i].node[n]['HUB'] == 'Hub':
				hubsInComp.append(n)
		#print 'Number of Hubs : ' + str(len(hubsInComp))
		if numNews == len(comp): # A Pure New Component is Found
			cat, scen2 = catA(discNets[i], comp)
			_metrics[years[i]]['A'] += cat
			_metrics[years[i]]['two'] += scen2
		elif numOlds == len(comp): # A Pure Old Component is Found
			cat, scen0 = catB(discNets[i], comp)
			_metrics[years[i]]['B'] += cat
			_metrics[years[i]]['zero'] += scen0
		else: # A Mixed Component is Found
			if len(hubsInComp) == 0: # Mixed Component & no hubs present
				cat, scen4, scen0 = catC(discNets[i], comp)
				_metrics[years[i]]['C'] += cat
				_metrics[years[i]]['four'] += scen4
				_metrics[years[i]]['zero'] += scen0
			else: #Mixed Component & Hubs present
				newHubToOldHub = [] # tuple with new hub first, old hub second
				newHubs = []
				oldHubs = []
				newAuthToHub = 0
				for hub in hubsInComp: # find hubs in component
					for nbr in discNets[i].neighbors(hub): # check for new nodes connecting to hubs
						if discNets[i].node[nbr]['OLDNEW'] == 'NEW':
							newAuthToHub += 1

					if discNets[i].node[hub]['OLDNEW'] == 'NEW':
						print 'NEW HUB FOUND : ' + hub
						newHubs.append(hub)
						for nbr in discNets[i].neighbors(hub): # look for new hub to old hub connection
							if discNets[i].node[nbr]['HUB'] == 'Hub':        # This is where we might deal with
								print 'HUB CONNECTED TO HUB : ' + nbr
								if discNets[i].node[nbr]['OLDNEW'] == 'OLD': #  New hub to New hub connections
									print "NEW HUB TO OLD HUB CONNECTION FOUND"
									newHubToOldHub.append((hub, nbr))
					else:
						oldHubs.append(hub)

				#print 'NewHubToOldHub : ' + str(len(newHubToOldHub))
				if newAuthToHub == 0:
					cat, scen4, scen0 = catD(discNets[i], comp)
					_metrics[years[i]]['D'] += cat
					_metrics[years[i]]['four'] += scen4
					_metrics[years[i]]['zero'] += scen0
				elif len(newHubToOldHub) == 0: # No new hub to old hub connections
					if (len(newHubs) > 0) and (len(oldHubs) == 0):  # Only New Hubs exist in the component
						cat, scen4, scen0 = catE(discNets[i], comp)
						_metrics[years[i]]['E'] += cat
						_metrics[years[i]]['four'] += scen4
						_metrics[years[i]]['zero'] += scen0
					elif (len(newHubs) == 0) and (len(oldHubs) > 0): # Only Old Hubs exist in the component
						cat, scen1, scen4, scen0 = catH(discNets[i], comp, oldHubs)
						_metrics[years[i]]['H'] += cat
						_metrics[years[i]]['one'] += scen1
						_metrics[years[i]]['four'] += scen4
						_metrics[years[i]]['zero'] += scen0
					else:
						cat, scen1, scen0, scen4 = catF(discNets[i], comp, oldHubs)
						_metrics[years[i]]['F'] += cat
						_metrics[years[i]]['one'] += scen1
						_metrics[years[i]]['zero'] += scen0
						_metrics[years[i]]['four'] += scen4
				else: # Mixed component with new hub to old hub connection
					cat, scen1, scen3, scen4, scen0 = catG(discNets[i], comp, newHubToOldHub, newHubs, oldHubs)
					_metrics[years[i]]['G'] += cat
					_metrics[years[i]]['one'] += scen1
					_metrics[years[i]]['three'] += scen3
					_metrics[years[i]]['four'] += scen4
					_metrics[years[i]]['zero'] += scen0


# Write out Gephi .gexf files
print linebreak1
print "Writing out Gexf files..."
for i in range(0, len(discNets)):
	print "\tYear: " + str(years[i])
	nx.write_gexf(discNets[i], discGephNetAttLocs[i])

if os.path.exists(_Catcsv):
	os.remove(_Catcsv)

if os.path.exists(_Scencsv):
	os.remove(_Scencsv)

if os.path.exists(_CatPerCsv):
	os.remove(_CatPerCsv)

if os.path.exists(_ScenPerCsv):
	os.remove(_ScenPerCsv)

catcsvOut = csv.writer(open(_Catcsv, "a"))
scencsvOut = csv.writer(open(_Scencsv, "a"))
otherHeaders = ["YEAR", "Category", "NUMBER"]
catcsvOut.writerow(otherHeaders)
scencsvOut.writerow(["YEAR", "Scenario", "NUMBER"])

print linebreak1
print 'Writing out to :'
print "\t" + _Catcsv
print linebreak2

for year in years:
	A = _metrics[year]['A']
	catcsvOut.writerow([year, "A", A])

for year in years:
	B = _metrics[year]['B']
	catcsvOut.writerow([year, "B", B])

for year in years:
	C = _metrics[year]['C']
	catcsvOut.writerow([year, "C", C])

for year in years:
	D = _metrics[year]['D']
	catcsvOut.writerow([year, "D", D])

for year in years:
	E = _metrics[year]['E']
	catcsvOut.writerow([year, "E", E])

for year in years:
	F = _metrics[year]['F']
	catcsvOut.writerow([year, "F", F])

for year in years:
	G = _metrics[year]['G']
	catcsvOut.writerow([year, "G", G])

for year in years:
	H = _metrics[year]['H']
	catcsvOut.writerow([year, "H", H])

print 'Writing out to :'
print "\t" + _Scencsv
print linebreak2

for year in years:
	zero = _metrics[year]['zero']
	scencsvOut.writerow([year, "0", zero])

for year in years:
	one = _metrics[year]['one']
	scencsvOut.writerow([year, "One", one])

for year in years:
	two = _metrics[year]['two']
	scencsvOut.writerow([year, "Two", two])

for year in years:
	three = _metrics[year]['three']
	scencsvOut.writerow([year, "Three", three])

for year in years:
	four = _metrics[year]['four']
	scencsvOut.writerow([year, "Four", four])

catPerCsvOut = csv.writer(open(_CatPerCsv, "a"))
scenPerCsvOut = csv.writer(open(_ScenPerCsv, "a"))
percHeaders = ["YEAR", "TYPE", "NUMBER", "TOTALNEW", "TOTAL"]
catPerCsvOut.writerow(["YEAR", "Category", "NUMBER", "TOTALNEW", "TOTAL"])
scenPerCsvOut.writerow(["YEAR", "Scenario", "NUMBER", "TOTALNEW", "TOTAL"])

print "Writing out to : "
print "\t" + _CatPerCsv
print linebreak2

for i in range(0, len(years)):
	A = _metrics[years[i]]['A']
	catPerCsvOut.writerow([years[i], "A", A, newNodes[i], totals[i]])

for i in range(0, len(years)):
	B = _metrics[years[i]]['B']
	catPerCsvOut.writerow([years[i], "B", B, newNodes[i], totals[i]])

for i in range(0, len(years)):
	C = _metrics[years[i]]['C']
	catPerCsvOut.writerow([years[i], "C", C, newNodes[i], totals[i]])

for i in range(0, len(years)):
	D = _metrics[years[i]]['D']
	catPerCsvOut.writerow([years[i], "D", D, newNodes[i], totals[i]])

for i in range(0, len(years)):
	E = _metrics[years[i]]['E']
	catPerCsvOut.writerow([years[i], "E", E, newNodes[i], totals[i]])

for i in range(0, len(years)):
	F = _metrics[years[i]]['F']
	catPerCsvOut.writerow([years[i], "F", F, newNodes[i], totals[i]])

for i in range(0, len(years)):
	G = _metrics[years[i]]['G']
	catPerCsvOut.writerow([years[i], "G", G, newNodes[i], totals[i]])

for i in range(0, len(years)):
	H = _metrics[years[i]]['H']
	catPerCsvOut.writerow([years[i], "H", H, newNodes[i], totals[i]])

print 'Writing out to :'
print "\t" + _ScenPerCsv
print linebreak2

for i in range(0, len(years)):
	one = _metrics[years[i]]['one']
	scenPerCsvOut.writerow([years[i], "One", one, newNodes[i], totals[i]])

for i in range(0, len(years)):
	two = _metrics[years[i]]['two']
	scenPerCsvOut.writerow([years[i], "Two", two, newNodes[i], totals[i]])

for i in range(0, len(years)):
	three = _metrics[years[i]]['three']
	scenPerCsvOut.writerow([years[i], "Three", three, newNodes[i], totals[i]])

for i in range(0, len(years)):
	four = _metrics[years[i]]['four']
	scenPerCsvOut.writerow([years[i], "Four", four, newNodes[i], totals[i]])

#for year in years:
#	print "Year : " + str(year)
#	A = _metrics[year]['A']
#	B = _metrics[year]['B']
#	C = _metrics[year]['C']
#	D = _metrics[year]['D']
#	E = _metrics[year]['E']
#	F = _metrics[year]['F']
#	G = _metrics[year]['G']
#	H = _metrics[year]['H']
#	zero = _metrics[year]['zero']
#	one = _metrics[year]['one']
#	two = _metrics[year]['two']
#	three = _metrics[year]['three']
#	four = _metrics[year]['four']
#	print "\tA: " + str(A)
#	print "\tB: " + str(B)
#	print "\tC: " + str(C)
#	print "\tD: " + str(D)
#	print "\tE: " + str(E)
#	print "\tF: " + str(F)
#	print "\tG: " + str(G)
#	print "\tH: " + str(H)
#	print "\t0: " + str(zero)
#	print "\t1: " + str(one)
#	print "\t2: " + str(two)
#	print "\t3: " + str(three)
#	print "\t4: " + str(four)
#
#	csvOut.writerow([year,A,B,C,D,E,F,G,H,zero,one,two,three,four])


