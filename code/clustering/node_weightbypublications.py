""" 
This script will take in a given graph and for each node it will
increment the corresponding node's weight in the node weight csv file and
accumulative graph
"""

import sys
import csv
import networkx as nx

#csv = sys.argv[1]
disc_loc = sys.argv[1]
accprev_loc = sys.argv[2]
accnew_loc = sys.argv[3]
acc_graph = nx.Graph()
disc_graph = nx.Graph()
lineBreak = "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>"

# take in argument for current year discrete slice, accumulative weighted graph location, 
# check that csv file exists
#try:
#   open(csv)
#except IOError as e:
#   print `csv` + " is not a valid csv location"

def cleanPaj(paj):
	""" The networkx module is not great at converting pajek files directly into gephi files.
	I have found that it works best to first convert the pajek network into a dictionary and
	then back into networkx's network data object before further modification. This method
	returns a usable network with all the same nodes and edges as pajek network passed into it.
	"""
	dict = nx.to_dict_of_dicts(paj)
	newNet = nx.from_dict_of_dicts(dict)
	return newNet

try:
	disc_graph = nx.read_pajek(disc_loc)
except IOError as e:
	print `disc_loc` + " is not a valid discrete graph slice location.  This program can not continue. Exiting now"
	sys.exit(1)

disc_graph = cleanPaj(disc_graph)

if accprev_loc == "firstyear":
	acc_graph = disc_graph.copy()
	for n in acc_graph:
		acc_graph.node[n]['weight'] = 1
		acc_graph.node[n]['OLDNEW'] = 'NEW'
		#print `acc_graph[n]`
		
	print "Writing file out to : " + `accnew_loc`
	try:
		nx.write_gexf(acc_graph, accnew_loc)
	except AttributeError as ae:
		print `ae`
		print "There was a problem writing out the first graph at " + `accnew_loc`
		sys.exit(1)
	sys.exit(0)

try:
	acc_graph = nx.read_gexf(accprev_loc)
except IOError as e:
		print "ERROR: " + `accprev_loc` + " is not the location of the previous accumulative slice."
		sys.exit(1)


#if it is already in the network, +1 to weight
# else add node to the network with weight of 1
print "creating graph at " + `accnew_loc`
acc_graph = nx.read_gexf(accprev_loc)
rem_edges = nx.to_edgelist(acc_graph)
acc_graph.remove_edges_from(rem_edges)
for d in disc_graph:
	if acc_graph.has_node(d):
		acc_graph.node[d]['weight'] = acc_graph.node[d]['weight'] + 1
		acc_graph.node[d]['OLDNEW'] = 'OLD'
	else:
		#print "The node : " + `d`
		#node=disc_graph.node[d]
		acc_graph.add_node(d)
		acc_graph.node[d]['weight'] = 1
		acc_graph.node[d]['OLDNEW'] = 'NEW'

numedges = 0
not_edges = 0
for n in acc_graph:
	acc_graph.node[n]['HUB']='nonhub'
edges = nx.to_edgelist(disc_graph)
acc_graph.add_edges_from(rem_edges, hubtonew="no")
for e in edges:
	if not (acc_graph.has_edge(e[0], e[1]) or acc_graph.has_edge(e[1], e[0])):
		numedges = numedges + 1
		acc_graph.add_edge(e[0], e[1], hubtonew="no")
	else:
		not_edges = not_edges + 1

#print "new edges : " + str(numedges)
#print "not edges : " + str(not_edges)
#print "total : " + str(acc_graph.number_of_edges())
nx.write_gexf(acc_graph, accnew_loc)


