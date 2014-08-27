import sys, itertools

prefix = sys.argv[1]

# re-implement classifier for links between clusters
summary = open(prefix + '.snet', 'rU')
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
net = open(prefix + '.net', 'rU')
net_line = net.read().split('\n')
net.close()
au_label = []
for i in range(1, int(net_line[0].split(' ')[1]) + 1):
    au_label.append([net_line[i].split(' ')[0], (net_line[i].split(r' ')[1] + ' ' + net_line[i].split(r' ')[2]).strip('"')])

# read vex file to get the weights for each authors, and loads au pubductitvity into the au_label list
# will use the most productive author as the label for the cluster
# if the cluster doesn't have a hub node
vec = open(prefix + '.vec', 'rU')
vec_line = vec.read().split('\n')
vec.close()
for i in range(1, int(vec_line[0].split(' ')[1]) + 1):
    au_label[i - 1].append(vec_line[i])

# read hub file to get node role information, only extract hub nodes into a list
hub = open(prefix + '.all.txt', 'rU')
hub_line = hub.read().split('\n')
hub.close()
hub_nodes = []
for line in hub_line:
    if line.split(' ')[-1] in ['R5', 'R6', 'R7']:
        hub_nodes.append(line.split(' ')[0])

# set cluster names as hub nodes of the cluster if exist, otherwise make the most
# productive author to be the label for the cluster
clu_lab = {}
for clu, ns in clusters.iteritems():
    productivity = 0
    for n in ns:
        if int(au_label[int(n)-1][2]) > productivity:
            productivity = int(au_label[int(n)-1][2])
            most_prod = au_label[int(n)-1][1]

        if n in hub_nodes:
            if clu not in clu_lab:
                clu_lab[clu] = [au_label[int(n)-1][1]]
            else:
                clu_lab[clu].append(au_label[int(n)-1][1])

    if clu not in clu_lab:
        clu_lab[clu] = [most_prod]

# function to produce interaction information between two clusters
# both clusters are only the valuses (node_id list in a cluster) from clusters above
def get_interact(clu1, clu2):
    tot_weight = 0      # sum of total edge weights
    pairs = []          # a list contains all the pairs of nodes between two clusters
    for i in clu1:
        for j in nodes[i][1]:       #look through its adjacent nodes
            if j in clu2:
                pairs.append((i, j))
                tot_weight += int(nodes[i][2][nodes[i][1].index(j)])
    return (tot_weight, pairs)      #return a tuple with total weights and pairs

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

# write nodes into cluster network files
output1 = open(prefix + '_collaberation.net', 'wb')
output2 = open(prefix + '_transfer.net', 'wb')
vec_output1 = open(prefix + '_collaberation.vec', 'wb')
vec_output2 = open(prefix + '_transfer.vec', 'wb')
output1.write('*Vertices ' + str(len(clusters)) + '\n')
output2.write('*Vertices ' + str(len(clusters)) + '\n')
vec_output1.write('*Vertices ' + str(len(clusters)) + '\n')
vec_output2.write('*Vertices ' + str(len(clusters)) + '\n')

for clu, ns in sorted(clusters.iteritems(), key = lambda x: int(x[0])):
    output1.write(clu + ' "' + '; '.join(clu_lab[clu]) + '"' + '\n')
    output2.write(clu + ' "' + '; '.join(clu_lab[clu]) + '"' + '\n')
    vec_output1.write(str(len(ns)) + '\n')
    vec_output2.write(str(len(ns)) + '\n')
vec_output1.close()
vec_output2.close()

output1.write('*Edges' + '\n')
output2.write('*Edges' + '\n')

# write edges using the classifier and get_interact funcitons above
for pair in itertools.combinations(range(1, len(clusters) + 1), 2):
    if classifier(get_interact(clusters[str(pair[0])], clusters[str(pair[1])])[1]) == 'collaberate':
        output1.write(str(pair[0]) + ' ' + str(pair[1]) + ' ' + str(get_interact(clusters[str(pair[0])], clusters[str(pair[1])])[0]) + '\n')
    elif classifier(get_interact(clusters[str(pair[0])], clusters[str(pair[1])])[1]) == 'transfer' and get_interact(clusters[str(pair[0])], clusters[str(pair[1])])[0] > 0:
        output2.write(str(pair[0]) + ' ' + str(pair[1]) + ' ' + str(get_interact(clusters[str(pair[0])], clusters[str(pair[1])])[0]) + '\n')

output1.close()
output2.close()
