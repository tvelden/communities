# this script rematch topic concentrated collaboration network to giant component 


# this function slipts a file into list of lines
def fileTolist(fileName):
    f = open(fileName, 'rU')
    lines = f.read().split('\n')
    f.close()
    return lines

# this function takes in the Giant Component of the accumulated network
# and produces list of tuples (node-index, node-label)
def labGC(accuNet):
    aGClab = [] # this list is to store GC labs
    for i in range(1, int(accuNet[0].split(' ')[1]) + 1):
        index, lab, coordi = [ls.strip() for ls in accuNet[i].split('"')]
        aGClab.append((index, lab))
    return aGClab

# this function takes in list of tuples of accumulative network GC's 
# (node-index, node-label), and list of lines of discrete collaboration network
def remap(disNet, aGClab):
    mapLab = [] # to store the index remap
    for i in range(1, int(disNet[0].split(' ')[1]) + 1):
        index = disNet[i].split('"')[0].rstrip()
        lab = disNet[i].split('"')[1]
        for accuInx, accuLab in aGClab:
            if lab == accuLab:
                mapLab.append((index, accuInx))
    return mapLab

# this function produces the remaped edges according to the remap list
def mapEdge(disNet, mapLab):
    newEdge = []
    for i in range(int(disNet[0].split(' ')[1]) + 2, len(disNet) - 1):
        lab1, lab2, weight = disNet[i].split(' ')
        edge = []
        disLab = [labs[0] for labs in mapLab]
        if lab1 in disLab and lab2 in disLab:
            for dis, accu in mapLab:
                if lab1 == dis:
                    edge.append(accu)
                if lab2 == dis:
                    edge.append(accu)
            edge.append(weight)
            newEdge.append(tuple(edge))
    return newEdge

if __name__ == '__main__':
    import glob
    accuGCnet = 'field2run1_accumulative1991-2012_22years_wholenet_collaboration_giant_layout.net'
    disc_prefix = glob.glob('*5years_wholenet_collaboration_*.net')
    for i in range(len(disc_prefix)):
        accuNet = fileTolist(accuGCnet)
        aGClab = labGC(accuNet)
        disNet = fileTolist(disc_prefix[i])
        
        mapLab = remap(disNet, aGClab)
        newEdge = mapEdge(disNet, mapLab)
        
        netOutput = open(disc_prefix[i][:-4] + '_GC.net', 'wb')
        for node in range(int(accuNet[0].split(' ')[1]) + 2):
            netOutput.write(accuNet[node] + '\n')
        for lab1, lab2, weight in newEdge:
            netOutput.write(lab1 + ' ' + lab2 + ' ' + weight + '\n')
        netOutput.close()