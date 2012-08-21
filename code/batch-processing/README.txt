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

At the moment there are two options:

cluster_analysis.sh - this script mainly finds the hubs of each cluster
within a network.

lc_size-diam_plot.sh - this script does a series of data visualizations
for analysis of the large component including size vs. time,
change in diameter over time, and structural visualization of the network

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
This .csv table contains data on the starting year, ending year, total size of the network in nodes, total size of the network in edges,
size of the large component in nodes, size of the large component in edges, 
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
