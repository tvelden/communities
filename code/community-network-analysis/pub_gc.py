# this script checks all the publications in the GC

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


if __name__ == '__main__':
    import glob, json
    import matplotlib.pyplot as plt
    accuGCnet = 'field2run1_accumulative1991-2012_22years_wholenet_collaboration_giant_layout.net'
    accu_collab_prefix = 'field2run1_accumulative1991-2012_22years_wholenet_collaboration.net'
    records = json.loads(open('records_topic.json', 'rU').read())
    GCNet = fileTolist(accuGCnet)
    aGClab = labGC(GCNet)
    accuCollabNet = fileTolist(accu_collab_prefix)
    mapLab = remap(accuCollabNet, aGClab)
    clus = zip(*mapLab)[0]
    for uid in records.keys():
        if all(clu not in clus for clu in records[uid][3]):
            records.pop(uid)
    years = range(1991, 2013)
    topics = range(12)
    topic_year_counts = {str(t): {str(yr): 0 for yr in years} for t in topics}
    for uid, val in records.iteritems():
        if val[2] in map(str, topics):
            topic_year_counts[val[2]][val[0]] += 1
    for t in map(str, topics):
        yr_counts = []
        for yr in map(str, years):
            yr_counts.append(topic_year_counts[t][yr])
        plt.plot(years, yr_counts)
    plt.legend(['topic ' + t for t in map(str, topics)], loc = 'upper left')
    plt.show()
    