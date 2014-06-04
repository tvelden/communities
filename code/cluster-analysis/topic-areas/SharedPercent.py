#shared Percent
source1="/Users/shiyansiadmin/Dropbox/Files/Field3Data1/affinity/NumberOfAuthorsDisJoin1991-2012" #number of authors
source2="/Users/shiyansiadmin/Dropbox/Files/Field3Data1/affinity/NumberOfSharedAuthorsDisJoin1991-2012" #matrix
target="/Users/shiyansiadmin/Dropbox/Files/Field3Data1/affinity/NumberOfSharedAuthorsDisJoin1991-2012(percent)"

infile1 = open(source1,"r")
infile2 = open(source2,"r")
outfile = open(target,"w")

NumberOfAuthor = []
NumberOfAuthor.append(0)
for line in infile1:
    NumberOfAuthor.append(int(line))

top = 11
i = 0
for line in infile2:
    ss = line.split("	")
    print ss
    i += 1
    j = 0
    for item in ss:
    	j += 1
    	if j>top:
    	    break
        number = float(int(item))/float(NumberOfAuthor[i])
        outfile.write(str(number) + "	")
    outfile.write("\n")

outfile.close()