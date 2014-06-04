#temp5 Merge
source = "/Users/shiyansiadmin/Dropbox/Files/NewField2Data2/affinity2/ResidualMatrixCitation"
startyear = 1991
endyear = 2012
outfile = open(source + "All", "w")
for year in range(startyear,endyear-3):
    st = year
    ed = year + 4
    infile = open(source + str(st) + "-" + str(ed),"r")
    for line in infile:
        outfile.write(line)

outfile.close()
