----------------------------------------------------------------
Last Modified by Shiyan Yan on 7/22/14
Changed all the directories of shell scripts on 6/4/14.

The parameters needed now are:
FIELD: the field of the data e.g. field1, field2
RUN: used as the mark of each run of the codes e.g. run1
START_YEAR, END_YEAR: the time span of the literature analyzed e.g. 1991,2012
SIZE: the window size for the time slices of affinity network
ROOT_PATH: the path of the root directory for all the files e.g. ../Dropbox/files/

There are five shell scripts for the citation network and affinity network analysis.
1. /pre-processing/make_dir_cit_aff.sh
The codes will generate the data and output directory for the field using FIELD and RUN. And the users need to put the input file named 'in-norm-dis-hfree-red.txt' into the ${ROOT_PATH}/${FIELD}/data/data1/reduced/

2. /batch-processing/cluster_analysis_dynamic.sh
The codes will generate the citation network, extract the giant component and run clustering over the network. All the results will be stored in ${ROOT_PATH}${FIELD}/runs/${RUN}/output/network/accumulative${START_YEAR}-${END_YEAR}/citation/   the Pajek .net file DirectCitationNetworkGiantComponent.net and .clu file DirectCitationNetworkGiantComponent_Synthe2.clu will be used in the following steps

3. /batch-processing/AffinityNetworkGenerateStep1.sh
The codes are used to build the accumulative affinity network (both citation based and shared-author based) 
all the network files (.net and .gexf) will be saved in ${ROOT_PATH}${FIELD}/runs/${RUN}/output/network/accumulative${START_YEAR}-${END_YEAR}/affinity/
all the statistics information (number of papers, residual matrix, number of shared authors, etc.) will be saved in ${ROOT_PATH}${FIELD}/runs/${RUN}/output/statistics/accumulative${START_YEAR}-${END_YEAR}/affinity/

4. /batch-processing/AffinityNetworkGenerateStep2.sh
The codes are used to build the dynamic affinity network (both citation based and shared-author based ).
Before running the codes, users need to open the two gephi files with the suffix of .gexf in  ${ROOT_PATH}${FIELD}/runs/${RUN}/output/network/accumulative${START_YEAR}-${END_YEAR}/affinity/, changed the layout and save them as {Original names}Changed.gexf in the same directory.

All the network results (e.g. AuthorsDynamicAffinityNetwork.gexf) will be saved in ${ROOT_PATH}${FIELD}/runs/${RUN}/output/network/dynamic${START_YEAR}-${END_YEAR}_${WINDOW}years/affinity/
All the statistics information (number of papers, residual matrix, number of shared authors, etc.) will be saved 
in ${ROOT_PATH}${FIELD}/runs/${RUN}/output/statistics/accumulative${START_YEAR}-${END_YEAR}/affinity/

5. /batch-processing/clusterInformationGenerate.sh
The codes will generate the key information for every cluster in citation network, the journal frequency for every cluster and cluster sizes. They should be run after the citation network is generated.

All the statistics are saved in ${ROOT_PATH}${FIELD}/runs/${RUN}/output/statistics/accumulative${START_YEAR}-${END_YEAR}/citation/


The final directory will be like this:

. (ROOT_PATH)
├── data
│   └── data1
│       ├── raw
│       └── reduced
│           └── in-norm-dis-hfree-red.txt
└── runs
    └── run1
        └── output
            ├── network
            │   ├── accumulative1991-2012
            │   │   ├── affinity
            │   │   │   ├── AccumulativeNetworkAuthor.gexf
            │   │   │   ├── AccumulativeNetworkAuthorChanged.gexf
            │   │   │   ├── AccumulativeNetworkCitation.gexf
            │   │   │   ├── AccumulativeNetworkCitationChanged.gexf
            │   │   │   ├── Authors\ 1991-2012.net
            │   │   │   ├── Citation\ 1991-2012.net
            │   │   │   ├── positionAuthor
            │   │   │   └── positionCitation
            │   │   └── citation
            │   │       ├── DirectCitationNetwork.net
            │   │       ├── DirectCitationNetworkGiantComponent.clu
            │   │       ├── DirectCitationNetworkGiantComponent.map
            │   │       ├── DirectCitationNetworkGiantComponent.net
            │   │       ├── DirectCitationNetworkGiantComponent.tree
            │   │       ├── DirectCitationNetworkGiantComponent_Shrunk.clu
            │   │       ├── DirectCitationNetworkGiantComponent_Shrunk.map
            │   │       ├── DirectCitationNetworkGiantComponent_Shrunk.net
            │   │       ├── DirectCitationNetworkGiantComponent_Shrunk.tree
            │   │       ├── DirectCitationNetworkGiantComponent_Shrunk_map.net
            │   │       ├── DirectCitationNetworkGiantComponent_Shrunk_map.vec
            │   │       ├── DirectCitationNetworkGiantComponent_Synthe.clu
            │   │       ├── DirectCitationNetworkGiantComponent_Synthe2.clu
            │   │       ├── DirectCitationNetworkGiantComponent_map.net
            │   │       └── DirectCitationNetworkGiantComponent_map.vec
            │   └── dynamic1991-2012_5years
            │       └── affinity
            │           ├── Authors\ 1991-1995.net
            │           ├── Authors\ 1992-1996.net
            │           ├── ...
            │           ├── AuthorsDynamicAffinityNetwork.gexf
            │           ├── AuthorsDynamicAffinityNetworkNotFix.gexf
            │           ├── Citation\ 1991-1995.net
            │           ├── Citation\ 1992-1996.net
            │           ├── ...
            │           ├── CitationDynamicAffinityNetwork.gexf
            │           ├── CitationDynamicAffinityNetworkNotFix.gexf
            │           ├── layoutAuthor
            │           └── layoutCitation
            └── statistics
                ├── accumulative1991-2012
                │   ├── affinity
                │   │   ├── NumberOfAuthors1991-2012
                │   │   ├── NumberOfAuthorsDisJoin1991-2012
                │   │   ├── NumberOfCitatoin1991-2012
                │   │   ├── NumberOfPapers1991-2012
                │   │   ├── NumberOfSharedAuthors1991-2012
                │   │   ├── NumberOfSharedAuthorsDisJoin1991-2012
                │   │   ├── ResidualMatrixAuthors1991-2012
                │   │   └── ResidualMatrixCitation1991-2012
                │   └── citation
                │       ├── JournalFreq
                │       │   └── JournalFrequency.txt
                │       ├── clustersize
                │       │   └── clustersize.txt
                │       └── keyinfo
                │           ├── ArticleID-ClusterID
                │           ├── cluster0
                │           ├── cluster1
                │           ├── cluster2
                │           └── ...
                └── dynamic1991-2012_5years
                    └── affinity
                        ├── NumberOfAuthors1991-1995
                        ├── NumberOfAuthors1992-1996
                        ├── ...
                        ├── NumberOfAuthorsDisJoin1991-1995
                        ├── NumberOfAuthorsDisJoin1992-1996
                        ├── ...
                        ├── NumberOfCitatoin1991-1995
                        ├── NumberOfCitatoin1992-1996
                        ├── ...
                        ├── NumberOfPapers1991-1995
                        ├── NumberOfPapers1992-1996
                        ├── ...
                        ├── NumberOfSharedAuthors1991-1995
                        ├── NumberOfSharedAuthors1992-1996
                        ├── ...
                        ├── NumberOfSharedAuthorsDisJoin1991-1995
                        ├── NumberOfSharedAuthorsDisJoin1992-1996
                        ├── ...
                        ├── ResidualMatrixAuthors1991-1995
                        ├── ResidualMatrixAuthors1992-1996
                        ├── ...
                        ├── ResidualMatrixCitation1991-1995
                        ├── ResidualMatrixCitation1992-1996
                        └── ...
----------------------------------------------------------------
Last Modified by Shiyan Yan on 6/4/14
There are four new shell scripts in batch-processing.
They all need parameters PATHI which indicates the folder all the results will be in, STYR and EDYR which indicate the time period codes will process.
cluster-analysis-dynamic.sh: The code needs the inputfile named as in.txt in the target folder. And it will generate the direct citation network, find the giant component and run the two round clustering algorithms to generate .clu files.

AffinityNetworkGenerateStep1.sh: The code will generate the affinity network for the accumulative network. The .gexf files will be saved in the PATHI/affinity/

After running the AffinityNetworkGenerateStep1.sh, users should use gephi to tune the layout of .gexf files. The layout will be used in the process of generating dynamic affinity netowork. Users should tune the layout of AccumulativeNetworkAuthor.gexf and save it as AccumulativeNetworkAuthorChanged.gexf in the same folder, tune the layout of AccumulativeNetworkCitation.gexf and save it as AccumulativeNetworkCitationChanged.gexf in the same folder.

AffinityNetworkGenerateStep2.sh: The code will generate dynamic affinity network with 5 years time winodw. All the files will be saved in affinity2/

clusterInformationGenerate.sh: The code will generate some important information for the cluster analysis including: keyInformation files in the folder keyinfo/, JournalFrequency.txt and variation of clustersize for top 11 clusters.

----------------------------------------------------------------

Last modified by Scott Cambo on 8/21/12

Before running any of the batch-processing scripts, you must have a
specific directory structure setup on your computer to use for the input and
output of these scripts.

To set up a directory for the input and output of the processing it is
recommended that you first run ../pre-processing/make_core_dirs.sh

This script sets up the following directory tree:

nwa-field_example
		├── data
		└── runs

In the parameter file there is a field labeled NET_PATH which should be
set as the relative path from the root of the communities repository to
the directory that will be used for input and output.

Also within the parameter file is a field labeled DATA_PATH which should
be set as the relative path from the data directory shown above to the 
input data itself.

After the core of the directory is made, the data is in the appropriate
directory, and the parameter file has been set, a batch-processing run can
begin.

There are currently six options (as of 2/6/13), for further details of any individual script please
refer to a comment header in the script itself:

    entrance_scenario.sh - this script's main purpose is to take the gephi files made by
    gephi_processing.sh, add additional attributes to each node that describe the author's
    specific entrance scenario and the category of its component.  Then the visualization script
    Category_And_Scenario_Vis.R or Category_And_Scenario_Pub_Vis.R is run to create visualizations
    of the change in authors entering these scenarios over time.

    cluster_analysis.sh - this script mainly finds the hubs of each cluster
    within a network.

    network_visualization.sh - This script builds largest component and second largest
    component subnetworks (in pajek .net format) from the original whole network .net files.
    It also collects data that is necessary for other network metrics as well. 

    lc_size-diam_plot.sh - this script does a series of data visualizations
    for analysis of the large component including size vs. time,
    change in diameter over time, a scatter plot of the diameter vs. size,
    and structural visualization of the network.  It is important to note that
    this method of structural visualization can be very computationally expensive
    and will commonly run R out of memory for 32-bit installations of R with larger
    networks.

    lc_size-diam_plot_wo_filecheck.sh - This script runs the same processes described
    in the above script, but does so without checking first to see if the files have
    already been created.  These two options are useful because there will be times,
    when one of the processing scripts might need to be adjusted and it would be preferable
    to have not do the completed processes over again while the files are in place (which 
    is when it is a god time to use the lc_size-diam_plot.sh which will check to see if the
    files are there first before processing them all over again).  The latter version will
    simply do all the processes again, overwriting the old files.

    gephi_processing.sh - The main function of this script is to create .gexf files from
    the pajek .net files that represent the whole network.  It also adds the following attributes
    to each node ...
        HUB -> set as 'hub' if this node is designated as a hub by the hublist created in cluster_analysis.sh
            and 'nonhub' if it is not found within the hublist.
        toHub -> set as 'yes' if this node is connected to a hub and 'no' otherwise.
        OLDNEW -> set as 'NEW' if the author has just entered the network and 'OLD' if this author has never
            appeared in the network.
        SIZEBYPUB -> this represents the number of publications this author has made up to and including the temporal
            slice of the dynamic network that its network file represents.
        SIZEBYACTIVEYEARS -> this represents the number of temporal slices (most often the slicing is set to 1 year, by
            the SIZE parameter of the parameter-global.txt file) that this author has been active up to and including
            the temporal slice of the dynamic network that its network file represents. 
        GROUP -> this attribute groups the author into one of the four following groups for use in Gephi which has limited
            ability with dynamically changing node attributes as the time of the network progresses.
                hubConnectedToHub -> hub joined the network connected to all hubs
                hubConnectedToNonHub -> hub joined the network connected to at least one nonhub
                nonHubConnectedToHub -> nonhub joined the network connected to a hub
                nonHubConnectedToHub -> nonhub joined the network connected to a nonhub
            **It is important to note that these groupings only apply to the author's attributes at the time that the
            author entered the network.  This is because Gephi (as of Gephi 0.8.1 Beta) is not capable of
            automatically/dynamically applying changes to attributes and so the attributes must represent a static,
            non-changing value.**
        
For more details see below
__________________________________________________________________________

Each script first runs a pre-processing script called
make_dirs_for_timeslice.sh which creates the necessary directory 
structure within runs for the output that is produced by the rest of the
batch-processing script

The directory structure will look something like this :
.
├── data
│   └── data1
│       ├── raw
│       │   └── in.txt
│       └── reduced
│           └── reducedData.txt
└── runs
    └── example
        └── output
            ├── networks
            │   └── accumulative1991-1998_2years
            │       ├── collaboration
            │       │   ├── 1991-1992
            │       │   │   ├── author_level_net
            │       │   │   │   ├── 2ndlargest_component
            │       │   │   │   ├── components
            │       │   │   │   ├── large_component
            │       │   │   │   └── whole_net
            │       │   │   └── cluster_level_net
            │       │   │       ├── 2ndlargest_component
            │       │   │       ├── components
            │       │   │       ├── large_component
            │       │   │       └── whole_net
            │       │   ├── 1991-1994
            │       │   │   ├── author_level_net
            │       │   │   │   ├── 2ndlargest_component
            │       │   │   │   ├── components
            │       │   │   │   ├── large_component
            │       │   │   │   └── whole_net
            │       │   │   └── cluster_level_net
            │       │   │       ├── 2ndlargest_component
            │       │   │       ├── components
            │       │   │       ├── large_component
            │       │   │       └── whole_net
            │       │   ├── 1991-1996
            │       │   │   ├── author_level_net
            │       │   │   │   ├── 2ndlargest_component
            │       │   │   │   ├── components
            │       │   │   │   ├── large_component
            │       │   │   │   └── whole_net
            │       │   │   └── cluster_level_net
            │       │   │       ├── 2ndlargest_component
            │       │   │       ├── components
            │       │   │       ├── large_component
            │       │   │       └── whole_net
            │       │   ├── 1991-1998
            │       │   │   ├── author_level_net
            │       │   │   │   ├── 2ndlargest_component
            │       │   │   │   ├── components
            │       │   │   │   ├── large_component
            │       │   │   │   └── whole_net
            │       │   │   └── cluster_level_net
            │       │   │       ├── 2ndlargest_component
            │       │   │       ├── components
            │       │   │       ├── large_component
            │       │   │       └── whole_net
            │       │   └── allyears
            │       │       ├── author_level_net
            │       │       │   ├── 2ndlargest_component
            │       │       │   ├── components
            │       │       │   ├── large_component
            │       │       │   └── whole_net
            │       │       └── cluster_level_net
            │       │           ├── 2ndlargest_component
            │       │           ├── components
            │       │           ├── large_component
            │       │           └── whole_net
            │       ├── generic
            │       │   ├── 1991-1992
            │       │   │   ├── 2ndlargest_component
            │       │   │   │   ├── images
            │       │   │   │   └── pajek
            │       │   │   ├── components
            │       │   │   │   └── 4alluvial
            │       │   │   ├── large_component
            │       │   │   │   ├── images
            │       │   │   │   └── pajek
            │       │   │   └── whole_net
            │       │   │       ├── hubs
            │       │   │       ├── images
            │       │   │       └── pajek
            │       │   ├── 1991-1994
            │       │   │   ├── 2ndlargest_component
            │       │   │   │   ├── images
            │       │   │   │   └── pajek
            │       │   │   ├── components
            │       │   │   │   └── 4alluvial
            │       │   │   ├── large_component
            │       │   │   │   ├── images
            │       │   │   │   └── pajek
            │       │   │   └── whole_net
            │       │   │       ├── hubs
            │       │   │       ├── images
            │       │   │       └── pajek
            │       │   ├── 1991-1996
            │       │   │   ├── 2ndlargest_component
            │       │   │   │   ├── images
            │       │   │   │   └── pajek
            │       │   │   ├── components
            │       │   │   │   └── 4alluvial
            │       │   │   ├── large_component
            │       │   │   │   ├── images
            │       │   │   │   └── pajek
            │       │   │   └── whole_net
            │       │   │       ├── hubs
            │       │   │       ├── images
            │       │   │       └── pajek
            │       │   ├── 1991-1998
            │       │   │   ├── 2ndlargest_component
            │       │   │   │   ├── images
            │       │   │   │   └── pajek
            │       │   │   ├── components
            │       │   │   │   └── 4alluvial
            │       │   │   ├── large_component
            │       │   │   │   ├── images
            │       │   │   │   └── pajek
            │       │   │   └── whole_net
            │       │   │       ├── hubs
            │       │   │       ├── images
            │       │   │       └── pajek
            │       │   └── allyears
            │       │       ├── 2ndlargest_component
            │       │       │   ├── images
            │       │       │   └── pajek
            │       │       ├── components
            │       │       │   └── 4alluvial
            │       │       ├── large_component
            │       │       │   ├── images
            │       │       │   └── pajek
            │       │       └── whole_net
            │       │           ├── hubs
            │       │           ├── images
            │       │           └── pajek
            │       └── transfer
            │           ├── 1991-1992
            │           │   ├── author_level_net
            │           │   │   ├── 2ndlargest_component
            │           │   │   ├── components
            │           │   │   ├── large_component
            │           │   │   └── whole_net
            │           │   └── cluster_level_net
            │           │       ├── 2ndlargest_component
            │           │       ├── components
            │           │       ├── large_component
            │           │       └── whole_net
            │           ├── 1991-1994
            │           │   ├── author_level_net
            │           │   │   ├── 2ndlargest_component
            │           │   │   ├── components
            │           │   │   ├── large_component
            │           │   │   └── whole_net
            │           │   └── cluster_level_net
            │           │       ├── 2ndlargest_component
            │           │       ├── components
            │           │       ├── large_component
            │           │       └── whole_net
            │           ├── 1991-1996
            │           │   ├── author_level_net
            │           │   │   ├── 2ndlargest_component
            │           │   │   ├── components
            │           │   │   ├── large_component
            │           │   │   └── whole_net
            │           │   └── cluster_level_net
            │           │       ├── 2ndlargest_component
            │           │       ├── components
            │           │       ├── large_component
            │           │       └── whole_net
            │           ├── 1991-1998
            │           │   ├── author_level_net
            │           │   │   ├── 2ndlargest_component
            │           │   │   ├── components
            │           │   │   ├── large_component
            │           │   │   └── whole_net
            │           │   └── cluster_level_net
            │           │       ├── 2ndlargest_component
            │           │       ├── components
            │           │       ├── large_component
            │           │       └── whole_net
            │           └── allyears
            │               ├── author_level_net
            │               │   ├── 2ndlargest_component
            │               │   ├── components
            │               │   ├── large_component
            │               │   └── whole_net
            │               └── cluster_level_net
            │                   ├── 2ndlargest_component
            │                   ├── components
            │                   ├── large_component
            │                   └── whole_net
            └── statistics
                └── accumulative1991-1998_2years
                    ├── collaboration
                    │   ├── 1991-1992
                    │   │   ├── 2ndlargest_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── components
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── large_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   └── whole_net
                    │   │       ├── images
                    │   │       └── tables
                    │   ├── 1991-1994
                    │   │   ├── 2ndlargest_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── components
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── large_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   └── whole_net
                    │   │       ├── images
                    │   │       └── tables
                    │   ├── 1991-1996
                    │   │   ├── 2ndlargest_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── components
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── large_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   └── whole_net
                    │   │       ├── images
                    │   │       └── tables
                    │   ├── 1991-1998
                    │   │   ├── 2ndlargest_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── components
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── large_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   └── whole_net
                    │   │       ├── images
                    │   │       └── tables
                    │   └── allyears
                    │       ├── 2ndlargest_component
                    │       │   ├── images
                    │       │   └── tables
                    │       ├── components
                    │       │   ├── images
                    │       │   └── tables
                    │       ├── large_component
                    │       │   ├── images
                    │       │   └── tables
                    │       └── whole_net
                    │           ├── images
                    │           └── tables
                    ├── generic
                    │   ├── 1991-1992
                    │   │   ├── 2ndlargest_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── components
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── large_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   └── whole_net
                    │   │       ├── images
                    │   │       └── tables
                    │   ├── 1991-1994
                    │   │   ├── 2ndlargest_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── components
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── large_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   └── whole_net
                    │   │       ├── images
                    │   │       └── tables
                    │   ├── 1991-1996
                    │   │   ├── 2ndlargest_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── components
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── large_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   └── whole_net
                    │   │       ├── images
                    │   │       └── tables
                    │   ├── 1991-1998
                    │   │   ├── 2ndlargest_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── components
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   ├── large_component
                    │   │   │   ├── images
                    │   │   │   └── tables
                    │   │   └── whole_net
                    │   │       ├── images
                    │   │       └── tables
                    │   └── allyears
                    │       ├── 2ndlargest_component
                    │       │   ├── images
                    │       │   └── tables
                    │       ├── components
                    │       │   ├── images
                    │       │   └── tables
                    │       ├── large_component
                    │       │   ├── images
                    │       │   └── tables
                    │       └── whole_net
                    │           ├── images
                    │           └── tables
                    └── transfer
                        ├── 1991-1992
                        │   ├── 2ndlargest_component
                        │   │   ├── images
                        │   │   └── tables
                        │   ├── components
                        │   │   ├── images
                        │   │   └── tables
                        │   ├── large_component
                        │   │   ├── images
                        │   │   └── tables
                        │   └── whole_net
                        │       ├── images
                        │       └── tables
                        ├── 1991-1994
                        │   ├── 2ndlargest_component
                        │   │   ├── images
                        │   │   └── tables
                        │   ├── components
                        │   │   ├── images
                        │   │   └── tables
                        │   ├── large_component
                        │   │   ├── images
                        │   │   └── tables
                        │   └── whole_net
                        │       ├── images
                        │       └── tables
                        ├── 1991-1996
                        │   ├── 2ndlargest_component
                        │   │   ├── images
                        │   │   └── tables
                        │   ├── components
                        │   │   ├── images
                        │   │   └── tables
                        │   ├── large_component
                        │   │   ├── images
                        │   │   └── tables
                        │   └── whole_net
                        │       ├── images
                        │       └── tables
                        ├── 1991-1998
                        │   ├── 2ndlargest_component
                        │   │   ├── images
                        │   │   └── tables
                        │   ├── components
                        │   │   ├── images
                        │   │   └── tables
                        │   ├── large_component
                        │   │   ├── images
                        │   │   └── tables
                        │   └── whole_net
                        │       ├── images
                        │       └── tables
                        └── allyears
                            ├── 2ndlargest_component
                            │   ├── images
                            │   └── tables
                            ├── components
                            │   ├── images
                            │   └── tables
                            ├── large_component
                            │   ├── images
                            │   └── tables
                            └── whole_net
                                ├── images
                                └── tables

After this is directory structure is created the batch-processing scripts
continue to their main functions.



