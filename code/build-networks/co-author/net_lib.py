""" This library includes some functions written to handle the tasks in defining the values of
attributes of nodes in a network by comparing them to the nodes in other graphs. """

import networkx as nx
import collections

def intersection(Anet, Bnet, attType, attVal1, attVal2):
	"""defines the attribute, attType, of node a in Anet to be of attVal1
	if this same node is found in Bnet, else attType is set to attVal2"""
	totalcount = 0.0
	val1count = 0.0
	val2count = 0.0
	for a in Anet:
		Anet.node[a][attType] = attVal2
		totalcount= totalcount + 1
		for b in Bnet:
			if (a == b):
				Anet.node[a][attType] = attVal1
	#			print `a` + "has been set to " + `attVal1`
				val1count = val1count + 1
				break
		if(Anet.node[a][attType] == attVal2):
	#		print `a` + "has been set to " + `attVal2`
			val2count = val2count + 1
	print "Total Count is " + `totalcount` + "\n"
	print "# of " + `attVal1` + " is " + `val1count`
	print "# of " + `attVal2` + " is " + `val2count`
	val1perc = (val1count/totalcount) * 100.0
	val2perc = (val2count/totalcount) * 100.0
	print "percent of " + `attVal1` + " is " + `val1perc`
	print "percent of " + `attVal2` + " is " + `val2perc`
	counts = collections.namedtuple('count', ['val1count', 'val2count'])
	return counts(val1count, val2count)

def interinter(Anet, attType1, attVal11, attVal12, attType2, attVal21, attVal22, attTypeNew):
	"""takes the combinations of the values of attributes, attType1 and attType2
	and combines them to make new groupings by attribute attTypeNew"""
	OLDIN = 0
	NEWIN = 0
	OLDOUT = 0
	NEWOUT = 0
	for a in Anet:
		Anet.node[a][attTypeNew] = Anet.node[a][attType1] + "," + `Anet.node[a][attType2]`
		if (Anet.node[a][attType1] == attVal11):
			if (Anet.node[a][attType2] == attVal21):
				OLDIN = OLDIN + 1 
#				print "OLDIN is now " + `OLDIN`
			else :
				OLDOUT = OLDOUT + 1
#				print "OLDOUT is now " + `OLDOUT`
		else:
			if (Anet.node[a][attType2] == attVal21):
				NEWIN = NEWIN + 1
#				print "NEWIN is now " + `NEWIN`
			else :
				NEWOUT = NEWOUT + 1
#				print "NEWOUT is now " + `NEWOUT`
	return OLDIN, NEWIN, OLDOUT, NEWOUT

def cleanPaj(paj):
	""" The networkx module is not great at converting pajek files directly into gephi files.
	I have found that it works best to first convert the pajek network into a dictionary and
	then back into networkx's network data object before further modification. This method
	returns a usable network with all the same nodes and edges as pajek network passed into it.
	"""
	dict = nx.to_dict_of_dicts(paj)
	newNet = nx.from_dict_of_dicts(dict)
	return newNet

def puremixcomps(net):
	"""returns a 11 tuple containing the total number of components, the number of mixed components,
	the number of pure new components, and the number of pure old components"""

	complist = nx.connected_component_subgraphs(net)
	purenew = 0
	pureold = 0
	mixed = 0
	total = len(complist)
	news_from_pure = 0
	olds_from_pure = 0
	news_from_mix = 0
	olds_from_mix = 0
	net_total = 0
	numnews = 0
	numolds = 0
	for comp in complist:
		comptotal = 0
		new = 0
		old = 0
		for n in comp:
			oldnew = comp.node[n]['OLDNEW']
			if oldnew == 'OLD':
				old = old + 1
				numolds += 1
			elif oldnew == 'NEW':
				new += 1
				numnews += 1
			else:
				print "!!!!!!   THIS SHOULD NOT HAPPEN -> !!!!!!!!" + `oldnew`
			comptotal = comptotal + 1

		if new == comptotal :
			purenew = purenew + 1
			news_from_pure += comptotal

		elif old == comptotal :
			pureold = pureold + 1
			olds_from_pure += comptotal

		else:
			mixed += 1
			olds_from_mix += old
			news_from_mix += new
		net_total += comptotal

	#print "Numnews : " + str(numnews)
	#print "Numolds : " + str(numolds)

	return total, mixed, purenew, pureold, news_from_mix, olds_from_mix, news_from_pure, olds_from_pure, numnews, numolds, net_total




def groupatts(net):
	""" returns a network in which each node in the network has a new attribute, 'group', designating which of
	of the following groups that node should be categorized as :
	1. non-hub joined network connected to a hub
	2. non-hub joined network not connected to a hub
	3. hub joined network connected to a hub
	4. hub joined network not connected to a hub
	"""

	for n in net:
		HUB = net.node[n]['HUB']
		toHUB = net.node[n]['toHub']
		if HUB == 'hub':
			if toHUB == 'yes':
				net.node[n]['group']= 'hub_to_hub'
			else:
				net.node[n]['group']= 'hub_not_to_hub'
		else:
			if toHUB == 'yes':
				net.node[n]['group']= 'nonhub_to_hub'
			else:
				net.node[n]['group']= 'nonhub_not_to_hub'

	return net

def conv_paj_to_gephi(pajLoc, gephiLoc):
	""" takes in the relative location of a pajek .net file and outputs a gephi .gexf file
		in the location designated by the gephi attribute
	"""

	pajNet = nx.read_pajek(pajLoc)
	pajNet = cleanPaj(pajNet)
	nx.write_gexf(gephiLoc)

def open_paj_as_nx(pajLoc):
	""" takes in the relative location of a pajek .net file and returns a networkx object
	"""

	pajNet = nx.read_pajek(pajLoc)
	pajNet = cleanPaj(pajNet)
	return pajNet

def fix_nx_edge_weight_bug(accumNet, attName):
	""" takes in an accumulative networkx network file and fixes a bug that occurs when networkx
		imports pajek networks with edge weights.  The bug parses the weight attribute data to
		a key in the edge attribute dictionary labeled as '0'.  The data is held as another dictionary.
		This method parses the data from this place to the correct part of the dictionary with the
		correct name.
	"""
	for e in accumNet.edges():
		attVal = float(accumNet.get_edge_data(e[0],e[1])[0]['weight'])
		accumNet[e[0]][e[1]][attName] = attVal
		
def attOldNew(discNet, accNet):
	""" Takes in a discrete network slice for a year n, and an accumulative network slice
	for a year n - 1 to determine which nodes were formerly in the network (Old) and which nodes
	have never been in the network (New).  The 'OLDNEW' attribute is set accordingly for each node.

	Returns : two tuple (# of new nodes, # of old nodes)

	Precondition : discNet and accNet are both networkx network objects 
	"""
	newNodes = 0
	oldNodes = 0

	for n in discNet:
		if n in accNet:
			discNet.node[n]['OLDNEW'] = 'OLD'
			oldNodes += 1
		else:
			discNet.node[n]['OLDNEW'] = 'NEW'
			newNodes += 1

	return (oldNodes, newNodes)