#temp3 generate .vec file
source = "/Users/shiyansiadmin/Dropbox/Files/Field3Data1/affinity/"
infile = open(source + "NumberOfPapers1991-2012", 'r')
outfile = open(source + "NumberOfPapers1991-2012.vec", 'w')
top = 11
outfile.write("Vertices "+ str(top) +"\n")
i = 0
for line in infile:
    i += 1
    if i>top:
        break
    outfile.write(line)

outfile.close()