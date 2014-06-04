#transfer pajek to gephi
import sys
netsource = sys.argv[1]
clusource = sys.argv[2]
target = sys.argv[3]
netinfile = open(netsource,"r")
cluinfile = open(clusource,"r")
outfile = open(target,"w")

clustersize = []
clustersize.append(1)
for line in cluinfile:
    clustersize.append(int(line))

head  = '<?xml version="1.0" encoding="UTF-8"?>\n'
head += '<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd">\n'
head += '  <meta lastmodifieddate="2013-12-11">\n'
head += '    <creator>Gephi 0.8.1</creator>\n'
head += '    <description></description>\n'
head += '  </meta>\n'
head += '  <graph defaultedgetype="directed" mode="static">\n'
head += '    <nodes>\n'
mid   = '    </nodes>\n'
mid  += '    <edges>\n'
end   = '    </edges>\n'
end  += '  </graph>\n'
end  += '</gexf>'

outfile.write(head)
i = -1
vnum = 0
for line in netinfile:
    i += 1
    if (i == 0):
        ss = line.split(" ")
        vnum = int(ss[1])
        continue
    if (i<=vnum):
        ss = line.split(" ")
        s1 =  "      " + '<node id="' + str(i) + '" label="Area' + str(i) + '">\n'
        s1 += '        <viz:size value="' + str(clustersize[i]) + '"></viz:size>\n'
        s1 += '      </node>\n'
        outfile.write(s1)
    if (i==vnum+1):
        outfile.write(mid)
    if (i>vnum+1):
        ss = line.split(" ")
        s1 =  '      <edge source="' + ss[0] + '" target="' + ss[1] + '" weight="' + ss[2][0:len(ss[2])-1] + '">\n'
        s1 += '      </edge>\n'
        outfile.write(s1)
outfile.write(end)        
outfile.close()

