import sys, json, codata

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

# since the new output file is generated after name ambiguation
# we need to re-generated records dictionary again and replace recodes' names
# with the name after name ambiguation
def getRecs(fieldText = 'field2.txt', allRecords = 'all_records.json'):
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
        records[uid] = [au]

    f = open(allRecords, 'rU')
    allrecords = json.loads(f.read())
    f.close()
    for key in records.keys():
        records[key].append(allrecords['WOS:' + key][6])
        records[key].insert(0, allrecords['WOS:' + key][0])
    return records

# this function provides a dictionary of years with clusters and its continents
# the dictionary has three levels: {yr: {clu: {co: []}}}
def getEveryYearCo(years, records, clusters):
    continents = ['No Country', 'AF', 'AS', 'EU', 'NA', 'SA', 'OC', 'AN']
    # build a dictionary container
    yearClu = {str(yr): {clu: {c: 0 for c in continents} for clu in clusters.keys()} for yr in years}
    for uid, val in records.iteritems():
        print val
        if len(val[2]) == 0:
            cons = ['No Country']
        else:
            cons = []
            for country in val[2]:
                cons.append(codata.ccn_to_ctca2[codata.cn_to_ccn[country.title()]])

        # go through all the authors and decide with clusters it belongs to
        clus = []
        for au in val[1]:
            for clu, aus in clusters.iteritems():
                if au in aus:
                    clus.append(clu)
        clus = set(clus)

        # finally add the infomation into the dictionary container
        for cluster in clus:
            for con in cons:
                yearClu[val[0]][cluster][con] += 1
    with open('yearClu_Geo.json', 'wb') as jsonOutput:
        json.dump(yearClu, jsonOutput, indent = 2)
    jsonOutput.close()
    return yearClu

def getSlide(years, yrRange, yearClu, disc_prefix, disc_postfix):
    lastYr = years[-1] - yrRange + 1
    startYrs = range(years[0], lastYr + 1)
    continents = [(0, 'No Country'), (1, 'AF'), (2, 'AS'), (3, 'EU'), (4, 'NA'), (5, 'SA'), (6, 'OC'), (7, 'AN'), 
        (8, 'AF-AS'), (9, 'AF-EU'), (10, 'AF-NA'), (11, 'AF-SA'), (12, 'AF-OC'), (13, 'AF-AN'), (14, 'AS-EU'), 
        (15, 'AS-NA'), (16, 'AS-SA'), (17, 'AS-OC'), (18, 'AS-AN'), (19, 'EU-NA'), (20, 'EU-SA'), (21, 'EU-OC'), 
        (22, 'EU-AN'), (23, 'NA-SA'), (24, 'NA-OC'), (25, 'NA-AN'), (26, 'SA-OC'), (27, 'SA-AN'), (28, 'OC-AN')]
    for year in startYrs:
        window = range(year, year + yrRange)
        slide = dict()
        for clu in yearClu[str(year)].keys():
            slide[clu] = {'No Country': 0, 'AF': 0, 'AS': 0, 'EU': 0, 'NA': 0, 'SA': 0, 'OC': 0, 'AN': 0}
        for yr in window:
            for clu in yearClu[str(yr)].keys():
                for continent in yearClu[str(yr)][clu]:
                    slide[clu][continent] += yearClu[str(yr)][clu][continent]

        cluContinent = {clu: 0 for clu in slide}
        for clu in slide.keys():
            sortClu = sorted(slide[clu].iteritems(), key = lambda x: x[1], reverse = True)
            if sortClu[0][0] == 'No Country' and sortClu[0][1] / float(sum(zip(*sortClu)[1])) > 0.8:
                cluContinent[clu] = 0
            else:
                if sortClu[0][0] == 'No Country':
                    if sortClu[2][1] * 2 >= sortClu[1][1]:
                        for ele in continents:
                            if set([sortClu[1][0], sortClu[2][0]]) == set(ele[1].split('-')):
                                cluContinent[clu] = ele[0]
                    else:
                        for ele in continents:
                            if ele[1] == sortClu[1][0]:
                                cluContinent[clu] = ele[0]
                else:
                    if sortClu[1][1] * 2 >= sortClu[0][1]:
                        for ele in continents:
                            if set([sortClu[0][0], sortClu[1][0]]) == set(ele[1].split('-')):
                                cluContinent[clu] = ele[0]
                    else:
                        for ele in continents:
                            if ele[1] == sortClu[0][0]:
                                cluContinent[clu] = ele[0]

        sortCluCon = sorted(cluContinent.iteritems(), key = lambda x: int(x[0]))
        aggregate = [0, 2, 3, 4]
        with open(disc_prefix + str(year)+ '-' + str(year + yrRange - 1) + '_' + str(yrRange) + disc_postfix, 'wb') as output:
            output.write('*Vertices ' + str(len(sortCluCon)) + '\n')
            for clu, con in sortCluCon:
                if con in aggregate:
                    output.write(str(con) + '\n')
                elif con == 14:
                    output.write('5' + '\n')
                elif con == 15:
                    output.write('6' + '\n')
                elif con == 19:
                    output.write('7' + '\n')
                else:
                    output.write('1' + '\n')
        output.close()

if __name__ == '__main__':
    import glob
    # accu_prefix = sys.argv[1] # accumulative network
    accu_prefix = 'field2run1_accumulative1991-2012_22years_wholenet'
    years = range(1991, 2013)
    disc_prefix =  accu_prefix.split('_')[0] + '_discrete' # prefix of discrete collaboration network
    disc_postfix = 'years_wholenet_collaboration.clu'
    
    # below three lines can be commented out after you get yearClu_Geo.json when you do editing.
    clusters = getCluNode(accu_prefix)
    records = getRecs('field2.txt', 'all_records.json')
    yearClu = getEveryYearCo(years, records, clusters)

    # uncomment following line for editing
    # yearClu = json.loads(open('yearClu_Geo.json', 'rU').read())
    getSlide(years, yrRange = 5, yearClu, disc_prefix, disc_postfix)
    