# this script creates topic concentrated collaboration network
# if there is a collabration link between two groups: look at the 
# each topic and change link weights according to each topic
import re, json

# get a dictionary with cluster and their authors from node labels, takes in net, clu files
def getCluNode(accu_prefix):
    net = open(accu_prefix + '.net', 'rU')
    net_line = net.read().split('\n')
    net.close()
    au_label = []
    for i in range(1, int(net_line[0].split(' ')[1]) + 1):
        line_sp = net_line[i].split(' ')
        if len(line_sp) > 2:
            au_label.append([line_sp[0], (line_sp[1] + ' ' + line_sp[2]).strip('"')])
        else:
            au_label.append([line_sp[0], line_sp[1].strip('"')])

    clu = open(accu_prefix + '.clu', 'rU')
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
def conbTopic(records, artTopicList):
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

# this function is to match all the authors for a publication to their clusters
def conbClu(records, clusters):
    for uid, val in records.iteritems():
        clus = set()
        for au in val[1]:
            for clu, aus in clusters.iteritems():
                if au in aus:
                    clus.add(clu)
        records[uid].append(list(clus))
    with open('records_topic.json', 'wb') as jsonOutput:
        json.dump(records, jsonOutput, indent = 2)
    jsonOutput.close()
    return records

def getSlideTopic(records, disc_collab_prefix, desired_topics = 11):
    disc_collab_net = open(disc_collab_prefix, 'rU')
    disc_collab = disc_collab_net.readlines()
    disc_collab_net.close()

    startYr, lastYr = map(int, re.findall('\d\d\d\d', disc_collab_prefix))
    window = map(str, range(startYr, lastYr + 1))
    topicIDs = map(str, range(desired_topics + 1))
    
    for topic in topicIDs:
        with open(disc_collab_prefix + '_' + topic + '.net', 'wb') as output:
            for line in disc_collab:
                if re.search('^\*.*', line):
                    output.write(line)
                elif re.search('^[0-9]+\s\".*', line):
                    output.write(line)
                elif re.search('^[0-9]+\s[0-9]+\s[0-9]+.*', line):
                    link = line.split(' ')[:2]
                    print link
                    weight_counter = 0
                    # get records dictionary info
                    for uid, val in records.iteritems():
                        if val[2] == topic and val[0] in window:
                            if set(val[3]).intersection(link) == set(link):
                                weight_counter += 1
                    if weight_counter > 0:
                        output.write(' '.join(link) + ' ' + str(weight_counter) + '\n')
        output.close()

if __name__ == '__main__':
    import glob
    accu_prefix = 'field2run1_accumulative1991-2012_22years_wholenet'
    # disc_collab_prefix = 'field2run2_discrete2005-2012_8years_wholenet_collaboration'
    disc_collab_prefix = glob.glob('*5years_wholenet_collaboration.net')
    clusters = getCluNode(accu_prefix)
    artTopicList, maxTopicID = getTopics('ArticleID-ClusterID2005-2012')
    pre_records = conbTopic(getRecs('field2.txt'), artTopicList)
    records = conbClu(pre_records, clusters)
    # records = json.loads(open('records_topic.json', 'rU').read())
    for discNet in disc_collab_prefix:
        getSlideTopic(records, disc_collab_prefix, 11)
    