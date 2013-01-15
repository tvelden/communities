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

There are currently five options (as of 12/29/12):

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

cluster_analysis.sh
	After make_dirs_for_timeslice.sh has finished the script runs
netbuild-pajek.py to create the .net files needed.  These files are
located within :
<run>/output/networks/<slice scheme>/generic/<time slice>/whole_net/pajek
Next, Rosvall's code is compiled and run on each whole network .net file
producing a corresponding .tree, .clu, .snet, .vec, .map, _map.net, and
_map.vec files in the pajek directory.  However, only the .clu, .snet, and the original .net file
are need to run the next script.  The next script is one of Asif's legacy
scripts, networksummarize.pl which produces .all.txt, .authcount.txt, .con.txt, and .hubcount.txt files in the <time slice>/whole_net/hubs.
Finally, zP.pl is run to produce the .hub file into the hub directory
containing the list of hub nodes in the network.
___________________________________________________________________________

lc_size-diam_plot.sh
	After make_dirs_for_timeslice.sh is finished, the script then runs
netbuild-pajek.py to create the necessary .net files.  When the .net files
are completed, lcbuild.R and sndlcbuild.R are run to create the corresponding
.net files for the largest component and second largest component. lcbuild.R
also creates a table of data for statistical analysis located in 
<run>/output/statistics/<slice scheme>/generic/allyears/whole_net/tables
This .csv table contains data on the starting year, ending year, total size of the 
network in nodes, total size of the network in edges, size of the large component
 in nodes, size of the large component in edges, 
and the diameter of the large component for each individual time slice. 
sndlcbuild.R also creates a .csv table that conatins starting year, 
ending year, size of the second largest component in nodes, size of the 
second largest component in edges, and the diameter of the second largest
component for each time slice.

After these scripts have run and the necessary data tables have been created
the following plots are produced by net_sizevstime.R :
-change in large component size in nodes (actual numbers) over time
-change in second largest component size in nodes (% of the whole network) over time
-change in large component size in edges (actual numbers) over time
-change in second largest component size in edges (% of the whole network) over time

next the net_diamvstime.R script produces
-change in the diameter of the largest component over time

next the net_diamvsize.R script produces
-change in the diameter vs. size of the largest component in nodes(actual numbers)
-change in the diameter vs. size of the largest component in nodes(% of the whole network)
-change in the diameter vs. size of the largest component in edges(actual numbers)
-change in the diameter vs. size of the largest component in edges(% of the whole network)

finally, network visualizations are produced using netvis.R.  It is important
to note that, for computers using 32-bit R, it is likely that graphs with over
8000 nodes will not be rendered because of the amount of memory needed to be
allocated for processing.
________________________________________________________________________

network_visualization.sh
________________________________________________________________________
cluster_analysis.sh
________________________________________________________________________
gephi_processing.sh
________________________________________________________________________

