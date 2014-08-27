# this script is built based on the net window script. it intents 
# to do the trantitative study on the discrete collaborate network.
# since we already know the group size, we are now curious about the links
# How about the collaboration links? Are they based on more papers or more people contributing or both?
# Determine temporal evolution (assume 5 year window and 2 year steps) of:
# 1. average number of papers underlying a link
# 2. average number of people from a pair of clusters contributing to the link 
# 3. average 'dispersion': = sum over author pairs {number of papers both authors are contributing to / total number of papers}
# 4. A series of scatter plots depicting for each inter-group link:
#     x: # of papers that the link is based on
#     y: # of authors from both clusters included in the links

def main():
    # re-implement classifier for links between clusters
    summary = open(accu_prefix + '.snet', 'rU')
    lines = summary.read().split('\n')
    summary.close()

    nodes = dict()
    # a dict for individual node information
    for i in range(len(lines) / 3):
        node_id = lines[i*3].split(' ')[0]
        clu_id = lines[i*3].split(' ')[2]
        adja_nodes = lines[i*3 + 1].split(' ')
        weights = lines[i*3 + 2].split(' ')
        nodes[node_id] = [clu_id, adja_nodes, weights]

    clusters = dict()
    # a dict for individual cluster information
    for key, val in nodes.iteritems():
        if val[0] not in clusters:
            clusters[val[0]] = [key]
        else:
            clusters[val[0]].append(key)

    # read original network file to get author name as node labels
    net = open(accu_prefix + '.net', 'rU')
    net_line = net.read().split('\n')
    net.close()
    au_label = []
    for i in range(1, int(net_line[0].split(' ')[1]) + 1):
        au_label.append([net_line[i].split(' ')[0], (net_line[i].split(r' ')[1] + ' ' + net_line[i].split(r' ')[2]).strip('"')])

    # read vex file to get the weights for each authors, and loads au pubductitvity into the au_label list
    # will use the most productive author as the label for the cluster
    # if the cluster doesn't have a hub node
    vec = open(accu_prefix + '.vec', 'rU')
    vec_line = vec.read().split('\n')
    vec.close()
    for i in range(1, int(vec_line[0].split(' ')[1]) + 1):
        au_label[i - 1].append(vec_line[i])

    # read hub file to get node role information, only extract hub nodes into a list
    hub = open(accu_prefix + '.all.txt', 'rU')
    hub_line = hub.read().split('\n')
    hub.close()
    hub_nodes = []
    for line in hub_line:
        if line.split(' ')[-1] in ['R5', 'R6', 'R7']:
            hub_nodes.append(line.split(' ')[0])

    # set cluster names as hub nodes of the cluster if exist, otherwise make the most
    # productive author to be the label for the cluster
    clu_lab = dict()
    for clu, ns in clusters.iteritems():
        productivity = 0
        for n in ns:
            if int(au_label[int(n)-1][2]) > productivity:
                productivity = int(au_label[int(n)-1][2])
                most_prod = au_label[int(n)-1][1]

            if n in hub_nodes:
                if clu not in clu_lab:
                    clu_lab[clu] = [au_label[int(n)-1][1] + '*']
                else:
                    clu_lab[clu].append(au_label[int(n)-1][1] + '*')

        if clu not in clu_lab:
            clu_lab[clu] = [most_prod]

    # load discrete network with its author names and match back to get a new dictionary with clusters
    discre_net = open(discre_prefix + '.net', 'rU')
    discre_net_lines = discre_net.read().split('\n')
    discre_net.close()
    # match back to the original node labels
    ori_lab = []
    for i in range(1, int(discre_net_lines[0].split(' ')[1]) + 1):
        for au in au_label:
            lab = (discre_net_lines[i].split(' ')[1] + ' ' + discre_net_lines[i].split(' ')[2]).strip('"')
            if lab == au[1]:
                ori_lab.append([str(i), au[0]]) # second element is the original label

    # get all the edge info from discrete network and match back to base network
    discre_edges = []
    for i in range(int(discre_net_lines[0].split(' ')[1]) + 2, len(discre_net_lines) - 1):
        pair = set()
        for new, ori in ori_lab:
            if discre_net_lines[i].split(' ')[0] == new or discre_net_lines[i].split(' ')[1] == new:
                pair.add(ori)   
        # each element contains a set of pair of nodes and edge weight
        discre_edges.append([pair, discre_net_lines[i].split(' ')[2]])


    # create a new dict to match discrete net work nodes based on the original clusters dict
    discre_clu = dict()
    for clu, ns in clusters.iteritems():
        discre_clu[clu] = []
        for lab in ori_lab:
            if lab[1] in ns:
                discre_clu[clu].append(lab[1])

    # function to produce interaction information between two clusters
    # both clusters are only the values (node_id list in a cluster) from clusters above
    def get_interact(clu1, clu2):
        pairs = []          # a list contains all the pairs of nodes between two clusters
        for i in clu1:
            for j in nodes[i][1]:       #look through its adjacent nodes
                if j in clu2:
                    pairs.append((i, j))
        return pairs      #return a tuple with total weights and pairs

    # function to classify transfer and collaberation links based on a list of pairs 
    # of nodes between two clusters
    def classifier(ls):
        a = set()
        b = set()
        for pair in ls:
            a.add(pair[0])
            b.add(pair[1])
        if len(a) > 2 and len(b) > 2:
            link_type = 'collaberate'
        else:
            link_type = 'transfer'
        return link_type


    # get all the collaberate link pairs from the base network
    collab_pairs = dict()
    # transfer_pairs = dict()
    for pair in itertools.combinations(range(1, len(clusters) + 1), 2):
        interaction = get_interact(clusters[str(pair[0])], clusters[str(pair[1])])
        if classifier(interaction) == 'collaberate':
            collab_pairs[pair] = interaction
        
    # now we can get edges for the new collab network
    new_collab = dict()
    for edge in discre_edges:
        for pair, links in collab_pairs.iteritems():
            if edge[0] in [set(x) for x in links]:
                if pair not in new_collab:
                    new_collab[pair] = [edge]
                else:
                    new_collab[pair].append(edge)

    def paperSum(ls):
        s = sum(int(x[1]) for x in ls)
        return s

    def auSum(ls):
        s = sum(len(x[0]) for x in ls)
        return s

    paperls = map(paperSum, new_collab.values())
    peoplels = map(auSum, new_collab.values())

    avgPaper = sum(paperls) / float(len(new_collab))
    avgAu = sum(peoplels) / float(len(new_collab))

    def dispersion(ls):
        dispersion = []
        pairs = [list(x[0]) for x in ls]
        for pair in pairs:
            pubCounter = 0
            au1, au2 = pair
            for edge in discre_edges:
                if au1 in edge[0] or au2 in edge[0]:
                    pubCounter += int(edge[1])
            dispersion.append(pubCounter)
        return dispersion
    dispersionLs = map(sum, map(dispersion, new_collab.values()))
    avgDispersion = sum([x/y for x, y in zip(dispersionLs, paperls)]) / float(len(new_collab))

    write nodes into cluster network files
    output = open(discre_prefix + '_summary.txt', 'wb')
    output.write('*summary for discrete window collaboration network \n')
    output.write('Average number of papers underlying a link: ' + str(avgPaper) + '\n')
    output.write('Average number of people from a pair of clusters contributing to the link: ' + str(avgAu) + '\n')
    output.write('Average dispersion: ' + str(avgDispersion))
    output.close()
    return (paperls, peoplels)

def scatterPlot(x, y, t):
    plt.scatter(np.array(x), np.array(y))
    plt.title(t, fontsize = 18)
    plt.xlim(-1, 25)
    plt.ylim(0, 35)

if __name__ == '__main__':
    import sys, itertools, glob
    import numpy as np
    import matplotlib.pyplot as plt
    accu_prefix = 'sigmod1run3_accumulative1991-2010_20years_wholenet'
    discre_prefixs = [dis[:-4] for dis in glob.glob('*5years_wholenet.net')]
    i = 1
    fig = plt.figure(figsize=(20, 20), dpi=800)
    # ax = fig.add_subplot(111)
    for discre_prefix in discre_prefixs:
        x, y = main()
        plt.subplot(4, 4, i)
        scatterPlot(x, y, str(1990 + i) + '-' + str(1994 + i))
        i += 1
    plt.suptitle(r'Scatter Plot for Each Inter-group Link', fontsize = 30)
    # ax.set_xlabel(r'# of Papers that the Link Is Based on', fontsize = 25)
    # ax.set_ylabel(r'# of Authors from Both Clusters Included in the Links', fontsize = 25)
    plt.savefig('Scatter.png')