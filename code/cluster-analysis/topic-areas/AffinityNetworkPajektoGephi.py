#pajek to gephi
import sys
netin = sys.argv[1]
statsin = sys.argv[2]
netout = sys.argv[3]

position = sys.argv[4]
startyear = int(sys.argv[6])
endyear = int(sys.argv[7])
window = int(sys.argv[8])
head  = '<?xml version="1.0" encoding="UTF-8"?>\n'
head += '<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd">\n'
head += '  <meta lastmodifieddate="2013-12-11">\n'
head += '    <creator>Gephi 0.8.1</creator>\n'
head += '    <description></description>\n'
head += '  </meta>\n'
head += '  <graph defaultedgetype="directed" mode="dynamic">\n'
head += '    <nodes>\n'
mid   = '      <node id="00" start="' + str(startyear-1) + '">\n'
mid  += '        <viz:size value="10"></viz:size>\n'
mid  += '        <viz:position x="0.0" y="0.0" z="0.0"></viz:position>\n'
mid  += '      </node>\n'
mid  += '      <node id="11" start="' + str(startyear-1) + '">\n'
mid  += '        <viz:size value="10"></viz:size>\n'
mid  += '        <viz:position x="0.0" y="0.1" z="0.0"></viz:position>\n'
mid  += '      </node>\n'
mid  += '    </nodes>\n'
mid  += '    <edges>\n'
mid  += '      <edge id="ex" source="00" target="11" weight="0.100" start="' + str(startyear-1) + '"></edge>\n'
end   = '    </edges>\n'
end  += '  </graph>\n'
end  += '</gexf>'



def transfer(type):
    # read the list of position
    listOfPosition = []    
    infilePosition = open(position,'r')
    for line in infilePosition:
        listOfPosition.append(line)
    writelistNode = []
    writelistEdge = []
    edgetot = 0
    top = 11
    for year in range(startyear,endyear-3):
        if (type=="Authors"):
            infileNode = open(statsin+'NumberOfPapers'+str(year)+"-"+str(year+window-1),'r')
        else:
            infileNode = open(statsin+'NumberOfPapers'+str(year)+"-"+str(year+window-1),'r')
        infileEdge = open(netin+type+' '+str(year)+"-"+str(year+window-1)+".net")
        tot = 0
        for line in infileNode:
            tot +=1
            if (tot>top): break
            addstring = "      " + '<node id="' + str(year) +'-' + str(tot) + '" label="Area' + str(tot) + '" start="' + str(year-0.25) + '" end="' + str(year+0.25) + '"' +  '>\n'
            addstring += '        <viz:size value="'+ line[0:len(line)-1] +'"></viz:size>\n'
            addstring +="        " + listOfPosition[tot-1]
            addstring += '      </node>\n'
            writelistNode.append(addstring)
        flag = 0
        for line in infileEdge:
            if (line=="*Arcs\n"): 
            	flag =1
            	continue
            if (flag==0): continue
            edgetot+=1
            k = line.split(" ")
            sou = k[0]
            tar = k[1]
            if (int(sou)>top):
                continue
            if (int(tar)>top):
                continue
            eweight = k[2]
            addstring = '        <edge id="' +  str(edgetot) + '" source="' + str(year)+ "-" + sou + '" target="' + str(year) + "-" + tar + '" weight="' + eweight[0:len(eweight)-1] + '" start="' + str(year-0.25) + '" end="' + str(year+0.25) + '"' +  '></edge>\n'
            writelistEdge += addstring
    outFile = open(netout + type +"DynamicAffinityNetwork.gexf",'w')
    outFile.write(head)
    for line in writelistNode:
        outFile.write(line)
    outFile.write(mid)
    for line in writelistEdge:
        outFile.write(line)
    outFile.write(end)

transfer(sys.argv[5])
#transfer("Citation")


