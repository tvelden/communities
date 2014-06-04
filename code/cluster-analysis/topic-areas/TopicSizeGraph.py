#topic size graph
source = "/Users/shiyansiadmin/Dropbox/Files/NewField2Data2"
outfile = open(source + "/clustersize","w")
top = 11
startyear = 1991
endyear = 2012
window = 5
outfile.write("year	")
for i in range(1,top+1):
    outfile.write("Cluster" + str(i) + "	")
outfile.write("\n")
for i in range(startyear,endyear-window+2):
    st = i
    outfile.write(str(st) + "	")
    ed = i + window -1
    infile = open(source + "/affinity2/NumberOfPapers" + str(st) + "-" + str(ed) , "r")
    co = 0
    for line in infile:
        co += 1
        if (co>top):
            break
        outfile.write(line[0:len(line)-1]+"	")
    outfile.write("\n")

outfile.close()
