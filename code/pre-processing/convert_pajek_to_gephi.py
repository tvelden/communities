import sys
import networkx as nx

inFile = sys.argv[1]
outFile = sys.argv[2]
lineBreak = "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>"

print lineBreak
print "inFile is " + inFile
print "outFile is " + outFile
print lineBreak

G = nx.read_pajek(inFile)
dict = nx.to_dict_of_dicts(G)
F = nx.from_dict_of_dicts(dict)
nx.write_gexf(F, outFile)

