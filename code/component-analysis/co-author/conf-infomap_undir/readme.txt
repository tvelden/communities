The software is provided "as is" and is free for academic and non-profit use. For commercial use and licensing please contact Martin Rosvall, martin.rosvall@physics.umu.se. Please cite in any publication: Martin Rosvall and Carl T. Bergstrom, Mapping change in large networks, PLoS ONE 5(1): e8694 (2010).

Extract the gzipped tar archive, run 'make' to compile and, for example, './conf-infomap 344 flow_undir.net 10 100 0.90' to run the code.
tar xzvf conf-infomap_dir.tgz
cd conf-infomap_dir
make
./conf-infomap 344 flow_undir.net 10 100 0.9
Here conf-infomap is the name of executable, 344 is a random seed (can be any positive integer value), flow_undir.net is the network to partition (in Pajek format), 10  is the number of attempts to partition the network (can be any integer value equal or larger than 1) and each of the 100 bootstrap networks. Finally, 0.90 is the confidence level for the significance analysis.

The output file with extension .smap has the format:

# modules: 4
# modulelinks: 4
# nodes: 16
# links: 20
# codelength: 3.15098
*Undirected
*Modules 4
1 "9,..." 0.25 0.05
2 "1,..." 0.25 0.05
3 "5,..." 0.25 0.05
4 "13,..." 0.25 0.05
*Insignificants: 2
4>2
3>2
*Nodes 16
1;1 "9" 0.075
1;2 "10" 0.075
1;3 "11" 0.05
1:4 "12" 0.05
2;1 "1" 0.075
2;2 "2" 0.075
2;3 "3" 0.05
2:4 "4" 0.05
3;1 "5" 0.075
3;2 "6" 0.075
3;3 "7" 0.05
3:4 "8" 0.05
4;1 "13" 0.075
4:2 "14" 0.075
4;3 "15" 0.05
4;4 "16" 0.05
*Links 4
1 3 0.025
1 4 0.025
2 3 0.025
2 4 0.025

This file contains the necessary information to generate a significance map in the alluvial generator. The names under *Modules are derived from the node with the highest flow volume within the module and 0.25 0.05 represent, respectively, the aggregated flow volume of all nodes within the module and the per step exit flow from the module. The nodes are listed with their module assignments together with their flow volumes. Finally, all links between the modules are listed in order from high flow to low flow

This file also contains information about which modules that are not significantly standalone and which modules they most often are clustered together with. The notation "4>2" under "*Insignificants 2" in the example file above means that the significant nodes in module 4 more often than the confidence level are clustered together with the significant nodes in module 2. In the module assignments, we use colons to denote significantly clustered nodes and semicolons to denote insignificantly clustered nodes. For example, the semicolon in '1;1 "9" 0.075' means that the node belongs to the largest, measured by flow, set of nodes that are clustered together in at least a fraction of bootstrap networks that is given by the confidence level.