#temp
top = 11
infile =open("/Users/shiyansiadmin/Dropbox/Files/Field3Data1/affinity/ResidualMatrixCitation1991-2012","r")
outfile = open("/Users/shiyansiadmin/Dropbox/Files/Field3Data1/affinity/ResidualMatrixCitation1991-2012(cc)","w")
i = 0
outfile.write("source	target	value\n")
for line in infile:
    i += 1
    a = line.split("	")
    for j in range(1,top+1):
        outfile.write(str(i) + "	" + str(j) + "	" + a[j-1] + "\n")

outfile.close()
