# create collaboration and transer network window based on the accumulative network
# use accumulative network clusters to form fixed cluster nodes for these network windows
# approach 2 for the discrete network cluster analysis
import sys, itertools, glob

# get a dictionary with cluster and their authors from node labels, takes in net files
# and it also returns a list with authors' info: index, name, number of paper
# both information are from accumulative network
def getCluNode(accu_prefix):
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
        sp = net_line[i].split(' ')
        if len(sp) == 3:
            au_label.append([sp[0], (sp[1] + ' ' + sp[2]).strip('"')])
        elif len(sp) == 2:
            au_label.append([sp[0], sp[1].strip('"')])
    # read vex file to get the weights for each authors, and loads au pubductitvity into the au_label list
    # will use the most productive author as the label for the cluster
    # if the cluster doesn't have a hub node
    vec = open(accu_prefix + '.vec', 'rU')
    vec_line = vec.read().split('\n')
    vec.close()
    for i in range(1, int(vec_line[0].split(' ')[1]) + 1):
        au_label[i - 1].append(vec_line[i])

    return nodes, clusters, au_label
    
# this function is to get cluster names based on either hub nodes or
# the most productive author in the cluster if hub nodes are absent
def getCluName(accu_prefix, clusters, au_label):
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
            if int(au_label[int(n)-1][2]) >= productivity:
                productivity = int(au_label[int(n)-1][2])
                most_prod = au_label[int(n)-1][1]

            if n in hub_nodes:
                if clu not in clu_lab:
                    clu_lab[clu] = [au_label[int(n)-1][1]]
                else:
                    clu_lab[clu].append(au_label[int(n)-1][1])

        if clu not in clu_lab:
            clu_lab[clu] = [most_prod]
    return clu_lab

# this function is to get discrete network node info and create a map 
# between node in disc and accu network, and it produce both cluster and edge info
def getMatch(au_label, disc_prefix, clusters):
    # load discrete network with its author names and match back to get a new dictionary with clusters
    net = open(disc_prefix + '.net', 'rU')
    net_lines = net.read().split('\n')
    net.close()
    # match back to the original node labels
    au_map = []
    for i in range(1, int(net_lines[0].split(' ')[1]) + 1):
        for au in au_label:
            sp = net_lines[i].split(' ')
            if len(sp) == 3:
                lab = (sp[1] + ' ' + sp[2]).strip('"')
            elif len(sp) == 2:
                lab = sp[1].strip('"')
            if lab == au[1]:
                au_map.append([str(i), au[0]]) # second element is the original label
    
    # get all the edge info from discrete network and match back to base network
    disc_edges = []
    for i in range(int(net_lines[0].split(' ')[1]) + 2, len(net_lines) - 1):
        pair = set()
        for new, ori in au_map:
            if net_lines[i].split(' ')[0] == new or net_lines[i].split(' ')[1] == new:
                pair.add(ori)   
        # each element contains a set of pair of nodes and edge weight
        disc_edges.append([pair, net_lines[i].split(' ')[2]])

    # create a new dict to match discrete net work nodes based on the original clusters dict
    disc_clu = dict()
    for clu, ns in clusters.iteritems():
        disc_clu[clu] = []
        for lab in au_map:
            if lab[1] in ns:
                disc_clu[clu].append(lab[1])

    return disc_edges, disc_clu

def getInteract(clu1, clu2, nodes):
    tot_weight = 0      # sum of total edge weights
    pairs = []          # a list contains all the pairs of nodes between two clusters
    for i in clu1:
        for j in nodes[i][1]:       #look through its adjacent nodes
            if j in clu2:
                pairs.append((i, j))
                tot_weight += int(nodes[i][2][nodes[i][1].index(j)])
    return tot_weight, pairs      #return a tuple with total weights and pairs

# function to classify transfer and collaboration links based on a list of pairs 
# of nodes between two clusters
def classifier(pairs):
    a = set()
    b = set()
    for pair in pairs:
        a.add(pair[0])
        b.add(pair[1])
    if len(a) > 2 and len(b) > 2:
        link_type = 'collaberate'
    else:
        link_type = 'transfer'
    return link_type

def getOutputs(disc_prefix, clu_lab, disc_clu, disc_edges, nodes):
    # get all the collaberate link pairs from the base network
    output1 = open(disc_prefix + '_collaboration.net', 'wb')
    output2 = open(disc_prefix + '_transfer.net', 'wb')
    vec_output1 = open(disc_prefix + '_collaboration.vec', 'wb')
    vec_output2 = open(disc_prefix + '_transfer.vec', 'wb')
    output1.write('*Vertices ' + str(len(disc_clu)) + '\n')
    output2.write('*Vertices ' + str(len(disc_clu)) + '\n')
    vec_output1.write('*Vertices ' + str(len(disc_clu)) + '\n')
    vec_output2.write('*Vertices ' + str(len(disc_clu)) + '\n')

    for clu, ns in sorted(disc_clu.iteritems(), key = lambda x: int(x[0])):
        output1.write(clu + ' "' + '; '.join(clu_lab[clu]) + '"' + '\n')
        output2.write(clu + ' "' + '; '.join(clu_lab[clu]) + '"' + '\n')

    for clu, ns in sorted(disc_clu.iteritems(), key = lambda x: int(x[0])):
        vec_output1.write(str(len(ns)) + '\n')
        vec_output2.write(str(len(ns)) + '\n')
    vec_output1.close()
    vec_output2.close()
    output1.write('*Edges' + '\n')
    output2.write('*Edges' + '\n')


    # here the pairs are cluster pairs, we need to classify them into two dicts
    for pair in itertools.combinations(range(1, len(disc_clu) + 1), 2):
        weight, interaction = getInteract(disc_clu[str(pair[0])], disc_clu[str(pair[1])], nodes)
        if len(interaction) != 0:
            if classifier(interaction) == 'collaborate':
                output1.write(str(pair[0]) + ' ' + str(pair[1]) + ' ' + str(weight) + '\n')
            elif classifier(interaction) == 'transfer':
                output2.write(str(pair[0]) + ' ' + str(pair[1]) + ' ' + str(weight) + '\n')

    output1.close()
    output2.close()

if __name__ == '__main__':
    accu_prefix = 'sigmod1run3_accumulative1991-2010_20years_wholenet'
    disc_prefixes = glob.glob('*5years_wholenet.net')
    nodes, clusters, au_label = getCluNode(accu_prefix)
    clu_lab = getCluName(accu_prefix, clusters, au_label)
    for disc_prefix in disc_prefixes:
        print disc_prefix
        disc_edges, disc_clu = getMatch(au_label, disc_prefix[:-4], clusters)
        getOutputs(disc_prefix[:-4], clu_lab, disc_clu, disc_edges, nodes)
        