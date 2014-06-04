#Compressed network generate
source = "../../../../../Dropbox/Files/Synthe/"
sourceout = "../../../../../Dropbox/Files/Compact/"

cluInfile = open(source+"Synthe2.clu",'r')
netInfile = open(source+"DirectCitationNetwork_Modified_GC.net",'r')
fileInfile = open("../../../../../Dropbox/Network Build/in-norm-dis-hfree-red.txt",'r')

cluOutfile = open(sourceout+"CompactNet.clu","w")
netOutfile = open(sourceout+"CompactNet.net","w")
fileOutfile = open(sourceout+"CompactNet.txt","w")

lineNumberBoo = {}
idNumberBoo = []
idMaps = {}

i = -1
tot = 0
for line in cluInfile:
    i += 1
    if (i==0):
        cluOutfile.write("Vertices 40491\n") #modify
        continue
    lineNumberBoo[i] = False
    temp = line[0:len(line)-1]
    num = int(temp)
    if (num>=12):
        continue
    tot += 1
    cluOutfile.write(line)
    lineNumberBoo[i] = True

toti = i    

print tot

i = -1 #linenumber
i2 = 0 #newlinenumber
for line in netInfile:
    i += 1
    if (i==0):
        netOutfile.write("Vertices "+str(tot)+"\n") #modify
        continue
    if (i<=toti):
        if (lineNumberBoo[i]!=True):
            continue
    i2 = i2 + 1
    if (i<=toti):
        idMaps[i] = i2
        ss = line.split('"')
        idt = ss[1]
        idNumberBoo.append(idt)
        netOutfile.write(str(i2)+' "'+ss[1]+'"'+ ss[2])
    else:
        if (line=="*Arcs\r\n"):
            netOutfile.write(line)
            continue
        else:
            ss = line.split(" ")
            if (int(ss[0]) in idMaps) and (int(ss[1]) in idMaps):
                new1 = str(idMaps[int(ss[0])])
                new2 = str(idMaps[int(ss[1])])
                netOutfile.write(new1+" "+new2+" "+ss[2])

flag = False
tt = False
for line in fileInfile:
    string = str(line)

    if (string[0] == 'I' and string[1]=='D'):
        idt = string[3:len(string)-1]
        if (idt in idNumberBoo):
            flag = True
        else:
            flag = False
            tt = True

    if flag:
        fileOutfile.write(string)
print tt











    