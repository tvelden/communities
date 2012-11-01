"""
This script reads a given hub node list and marks each of these corresponding nodes
in the given graph as hub nodes or nonhub nodes... maintains a csv of number of new nodes connected to
hub nodes
"""

import networkx as nx
import sys
import csv

accnew_loc = sys.argv[1]
csv_loc = sys.argv[2]
hublist_loc = sys.argv[3]
year = sys.argv[4]
hubtonew_count = 0

#open graph
try:
	acc_graph = nx.read_gexf(accnew_loc)
except IOError as ioe:
	print `ioe`
	print "Problem reading accumulative graph for " + `year`
	sys.exit(1)

#open csv file
try:
	in_csv = open(csv_loc, "a")
except IOError as ioe:
	print `ioe`
	print "Problem reading csv file for " + `year`
	sys.exit(1)

in_csvwriter = csv.writer(in_csv)

#open hublist
try:
	inhublist = open(hublist_loc, "r")
except IOError as ioe:
	print `ioe`
	print "Problem reading hub list for " + `year`
	sys.exit(1)



for line in inhublist.readlines():
	#length = len(line) - 3
	hub = line.strip('\n').replace('\"', '')
	#print "hub : " + line 
	if acc_graph.has_node(hub):
		acc_graph.node[hub]['HUB'] = 'hub'
		#print "hub found in graph"
		for nbr in acc_graph[hub]:
			OLDNEW = acc_graph.node[nbr]['OLDNEW']
			if OLDNEW == 'NEW':
				#print "hubtonew found"
				hubtonew_count = hubtonew_count + 1
				acc_graph.edge[nbr][hub]['hubtonew'] = 'yes'
				#print hubtonew_count

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

# add functionality to create a group that discerns intersection between values in hub attribute
# new/old attribute

#print hubtonew_count
inhublist.close()
try:
	nx.write_gexf(acc_graph, accnew_loc)
except IOError as ioe:
	print `ioe`
	print "Problem writing out acc_graph"
	sys.exit(1)

in_csvwriter.writerow([str(year) , `hubtonew_count`])
in_csv.close()




