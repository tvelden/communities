"""
Takes a particular year as an argument and computes a network representing the new authors who have
attached to old authors in this year, the old authors who have attached to old authors, and the new authors
who have attached to new authors as separate clusters.
"""

import networkx as nx
import sys

# Arguments
# 1. FileA -> Discrete 1 year slice of entire network of current year
# 2. FileB -> Accumulative 1 year slice of entire network up to the current year, but not including current year
# 3. FileC -> Accumulative 1 year slice of large_component up to and including the current year.
# 4. outFile -> Output .gexf file name 

FileA = sys.argv[1]
FileB = sys.argv[2]
FileC = sys.argv[3]

outFile = sys.argv[4]
lineBreak = "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>"

print lineBreak
print "FileA= " + FileA
print "FileB= " + FileB
print "FileC= " + FileC
print "outFile= " + outFile
print lineBreak

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
				print `a` + "has been set to " + `attVal1`
				val1count = val1count + 1
				break
		if(Anet.node[a][attType] == attVal2):
			print `a` + "has been set to " + `attVal2`
			val2count = val2count + 1
	print "Total Count is " + `totalcount` + "\n"
	print "# of " + `attVal1` + " is " + `val1count`
	print "# of " + `attVal2` + " is " + `val2count`
	val1perc = (val1count/totalcount) * 100.0
	val2perc = (val2count/totalcount) * 100.0
	print "percent of " + `attVal1` + " is " + `val1perc`
	print "percent of " + `attVal2` + " is " + `val2perc`

def interinter(Anet, attType1, attType2, attTypeNew):
	"""takes the combinations of the values of attributes, attType1 and attType2
	and combines them to make new groupings by attribute attTypeNew"""
	for a in Anet:
		Anet.node[a][attTypeNew] = `Anet.node[a][attType1]` + "," + `Anet.node[a][attType2]`

def cleanPaj(paj):
	""" The networkx module is not great at converting pajek files directly into gephi files.
	I have found that it works best to first convert the pajek network into a dictionary and
	then back into networkx's network data object before further modification. This method
	returns a usable network with all the same nodes and edges as pajek network passed into it.
	"""
	dict = nx.to_dict_of_dicts(paj)
	newNet = nx.from_dict_of_dicts(dict)
	return newNet

#take file input
Apaj = nx.read_pajek(FileA)
Bpaj = nx.read_pajek(FileB)
Cpaj = nx.read_pajek(FileC)

#clean the pajek files
netA = cleanPaj(Apaj)
netB = cleanPaj(Bpaj)
netC = cleanPaj(Cpaj)

#get intersection between A and B
intersection(netA, netB, 'OLDNEW', 'OLD', 'NEW')
intersection(netA, netC, 'inLC', True, False)
interinter(netA, 'OLDNEW', 'inLC', 'OLDNEWinLC')
nx.write_gexf(netA, outFile)



#G = nx.read_pajek(inFile)
#dict = nx.to_dict_of_dicts(G)
#F = nx.from_dict_of_dicts(dict)
#nx.write_gexf(F, outFile)

