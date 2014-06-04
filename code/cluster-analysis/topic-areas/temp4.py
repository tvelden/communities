#temp4 acount the matrix for the number of papers
source = "/Users/shiyansiadmin/Dropbox/Files/NewField2Data2/affinity2/"
top = 11
clusters = {}
for i in range(1,top+1):
    clusters[i] = []

startyeart = 1991
endyeart = 2012
window = 5
for startyear in range(startyeart,endyeart-window+2):
    infile = open(source + "NumberOfPapers" + str(startyear) + "-" + str(startyear+window-1),'r')
    i = 0
    for line in infile:
        i += 1
        if (i>top): 
            break
        clusters[i].append(line[0:len(line)-1])
    infile.close()

outfile = open(source + "NumberOfPapersMatrix",'w')
outfile.write("	")
for startyear in range(startyeart,endyeart-window+2):
    outfile.write(str(startyear) + "-" + str(startyear+window-1) + "	")
outfile.write("\n")

for i in range(1,top+1):
    outfile.write("Area"+str(i)+"	")
    for it in clusters[i]:
        outfile.write(it+"	")
    outfile.write("\n")