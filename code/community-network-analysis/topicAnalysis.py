import sys, json

# get a dictionary with cluster and their authors from node labels, takes in net files
def getCluNode(prefix):
    net = open(prefix + '.net', 'rU')
    net_line = net.read().split('\n')
    net.close()
    au_label = []
    for i in range(1, int(net_line[0].split(' ')[1]) + 1):
        line_sp = net_line[i].split(' ')
        if len(line_sp) > 2:
            au_label.append([line_sp[0], (line_sp[1] + ' ' + line_sp[2]).strip('"')])
        else:
            au_label.append([line_sp[0], line_sp[1].strip('"')])

    clu = open(prefix + '.clu', 'rU')
    clu_line = clu.read().split('\n')
    clu.close()
    clusters = dict()
    for i in range(1, int(clu_line[0].split(' ')[1]) + 1):
        if clu_line[i] not in clusters:
            clusters[clu_line[i]] = [au_label[i - 1][1]]
        else:
            clusters[clu_line[i]].append(au_label[i - 1][1])
    return clusters

# this function takes in article-topic and get total number of topics
def getTopics(recordTopic = 'ArticleID-TopicID'):
    f = open(recordTopic, 'rU')
    artTopic = f.readlines()
    f.close()

    artTopicList = []
    for line in artTopic:
        uid, topicID = line.strip('\n').split('\t')
        artTopicList.append((uid, topicID))

    topicIDs = zip(*artTopicList)[1]
    maxTopicID = max(map(int, topicIDs))
    if len(sorted(set(topicIDs))) == len(range(min(map(int, topicIDs)), maxTopicID+1)):
        return artTopicList, maxTopicID
    else:
        print 'some topic id has no article assigned to!'

# this function is to get records information, uid and authors for matching topics
def getRecs(fieldText = 'field2.txt'):
    f = open(fieldText, 'rU')
    text = f.read()
    f.close()

    recs = text.split('\n\n')
    recs = [r.split('\n') for r in recs]
    records = dict()
    for rec in recs:
        au = []
        for line in rec:
            if line[0:2] == 'ID':
                uid = line[3:]
            elif line[0:2] == 'AU':
                au.append(line[3:])
            elif line[0:1] == ' ':
                au.append(line[1:])
            elif line[0:2] == 'BI':
                yr = line[-4:]
        records[uid] = [yr, au]
    return records

# this function is to combine info of topics and records
def conb(records, artTopicList):
    for tup in artTopicList:
        if tup[0] in records:
            records[tup[0]].append(tup[1])
        else:
            print tup[0], 'is not showing up in records.'
    for uid in records.keys():
        if len(records[uid]) != 3:
            print uid
            records.pop(uid)
    return records

# this function gets every year info with articles and on all topics
def getYearTopic(years, records, clusters, maxTopicID):
    topics = map(str, range(maxTopicID + 1))
    yearClu = {str(yr): {clu: {t: 0 for t in topics} for clu in clusters.keys()} for yr in years}
    for uid, val in records.iteritems():
        print val
        # go through all the authors and decide with clusters it belongs to
        clus = []
        for au in val[1]:
            for clu, aus in clusters.iteritems():
                if au in aus:
                    clus.append(clu)
        clus = set(clus)
        recTocpic = val[2]
        # finally add the infomation into the dictionary container
        for cluster in clus:
            yearClu[val[0]][cluster][recTocpic] += 1
    with open('yearClu_Topic.json', 'wb') as jsonOutput:
        json.dump(yearClu, jsonOutput, indent = 2)
    jsonOutput.close()
    return yearClu

# finally, this function accumulates cluster topics for a time window
def getSlide(years, yrRange, yearClu, maxTopicID, disc_prefix, disc_postfix):
    lastYr = years[-1] - yrRange + 1
    startYrs = range(years[0], lastYr + 1)
    topicIDs = map(str, range(maxTopicID + 1))
    for year in startYrs:
        window = range(year, year + yrRange)
        slide = dict()
        for clu in yearClu[str(year)].keys():
            slide[clu] = {t: 0 for t in topicIDs}
        for yr in window:
            for clu in yearClu[str(yr)].keys():
                for topic in yearClu[str(yr)][clu]:
                    slide[clu][topic] += yearClu[str(yr)][clu][topic]
        
        # then need to get topics concentrations for each slide
        for topic in topicIDs[:12]:
            with open(disc_prefix + str(year)+ '-' + str(year + yrRange - 1) + '_' + str(yrRange) + disc_postfix + '_' + topic + '.clu', 'wb') as output:
                output.write('*Vertices ' + str(len(slide)) + '\n')
                for clu in sorted(map(int, slide.keys())):
                    totalPaper = sum(slide[str(clu)].values())
                    topicPaper = slide[str(clu)][topic]
                    if topicPaper == 0 or totalPaper == 0:
                        output.write('0' + '\n')
                    elif topicPaper / float(totalPaper) <= 0.1:
                        output.write('1' + '\n')
                    elif  0.1 < topicPaper / float(totalPaper) <= 0.5:
                        output.write('2' + '\n')
                    elif topicPaper / float(totalPaper) > 0.5:
                        output.write('3' + '\n')
            output.close()

if __name__ == '__main__':
    # accu_prefix = sys.argv[1] # accumulative network
    accu_prefix1 = 'field2run1_accumulative1991-2012_22years_wholenet'
    disc_prefix =  accu_prefix1.split('_')[0] + '_discrete' # prefix of discrete collaboration network
    disc_postfix = 'years_wholenet_collaboration'
    
    years = range(1991, 2013)
    # clusters = getCluNode(accu_prefix)
    # artTopicList, maxTopicID = getTopics('ArticleID-ClusterID2005-2012')
    # records = conb(getRecs('field2.txt'), artTopicList)
    # yearClu = getYearTopic(years, records, clusters, maxTopicID)
    yearClu = json.loads(open('22yearClu_Topic.json', 'rU').read())
    getSlide(years, 22, yearClu, 49, disc_prefix, disc_postfix)
