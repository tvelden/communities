# create collaboration and transer network window based on the accumulative network
# use accumulative network clusters to form fixed cluster nodes for these network windows
# approach 2 for the discrete network cluster analysis
import sys, itertools, glob

# accu_prefix = sys.argv[1]
# discre_prefix = sys.argv[2]
# discre_prefix = [dis[:-4] for dis in glob.glob('*5years_wholenet.net')]

accu_prefix = 'field2run1_accumulative1991-2012_22years_wholenet'
discre_prefix = 'field2run1_discrete1991-1995_5years_wholenet'

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
        sp = discre_net_lines[i].split(' ')
        if len(sp) == 3:
            lab = (sp[1] + ' ' + sp[2]).strip('"')
        elif len(sp) == 2:
            lab = sp[1].strip('"')
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
# both clusters are only the valuses (node_id list in a cluster) from clusters above
def get_interact(clu1, clu2):
    # tot_weight = 0      # sum of total edge weights
    pairs = []          # a list contains all the pairs of nodes between two clusters
    for i in clu1:
        for j in nodes[i][1]:       #look through its adjacent nodes
            if j in clu2:
                pairs.append((i, j))
                # tot_weight += int(nodes[i][2][nodes[i][1].index(j)])
    return pairs      #return a tuple with total weights and pairs

# function to classify transfer and collaboration links based on a list of pairs 
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
transfer_pairs = dict()
for pair in itertools.combinations(range(1, len(clusters) + 1), 2):
    interaction = get_interact(clusters[str(pair[0])], clusters[str(pair[1])])
    if classifier(interaction) == 'collaberate':
        collab_pairs[pair] = interaction
    elif classifier(interaction) == 'transfer':
        transfer_pairs[pair] = interaction

# now we can get edges for the new collab network
new_edge_collab = dict()
for edge in discre_edges:
    for pair, link in collab_pairs.iteritems():
        if edge[0] in [set(x) for x in link]:
            if pair not in new_edge_collab:
                new_edge_collab[pair] = int(edge[1])
            else:
                new_edge_collab[pair] += int(edge[1])

new_edge_transfer = dict()
for edge in discre_edges:
    for pair, link in transfer_pairs.iteritems():
        if edge[0] in [set(x) for x in link]:
            if pair not in new_edge_transfer:
                new_edge_transfer[pair] = int(edge[1])
            else:
                new_edge_transfer[pair] += int(edge[1])

# write nodes into cluster network files
output1 = open(discre_prefix + '_collaboration.net', 'wb')
output2 = open(discre_prefix + '_transfer.net', 'wb')
vec_output1 = open(discre_prefix + '_collaboration.vec', 'wb')
vec_output2 = open(discre_prefix + '_transfer.vec', 'wb')
output1.write('*Vertices ' + str(len(clusters)) + '\n')
output2.write('*Vertices ' + str(len(clusters)) + '\n')
vec_output1.write('*Vertices ' + str(len(clusters)) + '\n')
vec_output2.write('*Vertices ' + str(len(clusters)) + '\n')

for clu, ns in sorted(clusters.iteritems(), key = lambda x: int(x[0])):
    output1.write(clu + ' "' + '; '.join(clu_lab[clu]) + '"' + '\n')
    output2.write(clu + ' "' + '; '.join(clu_lab[clu]) + '"' + '\n')

for clu, ns in sorted(discre_clu.iteritems(), key = lambda x: int(x[0])):
    vec_output1.write(str(len(ns)) + '\n')
    vec_output2.write(str(len(ns)) + '\n')
vec_output1.close()
vec_output2.close()

output1.write('*Edges' + '\n')
output2.write('*Edges' + '\n')

for pair, weight in new_edge_collab.iteritems():
    output1.write(str(pair[0]) + ' ' + str(pair[1]) + ' ' + str(weight) + '\n')

for pair, weight in new_edge_transfer.iteritems():
    output2.write(str(pair[0]) + ' ' + str(pair[1]) + ' ' + str(weight) + '\n')

output1.close()
output2.close()
