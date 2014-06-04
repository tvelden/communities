#Zoomout
import sys
infile = open(sys.argv[1],'r')
outfile = open(sys.argv[2],'w')

for line in infile:
    ss = line.split('"')
    out = ""
    out += ss[0] + '"'
    nu = float(ss[1]) * 50
    out += str(nu) + '"'
    out += ss[2] + '"'
    nu = float(ss[3]) * 50
    out += str(nu) + '"'
    out += ss[4] + '"'
    out += ss[5] + '"'
    out += ss[6]
    outfile.write(out)
outfile.close()
