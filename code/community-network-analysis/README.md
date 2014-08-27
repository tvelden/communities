###Collaboration network
====
scripts:
* link_type.py
* window.py

After getting accumulative network and all the time slide networks, put them togethor in a directory.

The process will start with script link_type.py. It produces collaboration network and transfer network files and their vector files for accumulative network.
In command window: type python link_type.py accumulative_prefix 
accumulative_prefix is sigmod1run3_accumulative1991-2010_20years_wholenet for sigmod1run3_accumulative1991-2010_20years_wholenet.net.

It takes following four accumulative network files:

    * field2run1_accumulative1991-2012_22years_wholenet.net
    * field2run1_accumulative1991-2012_22years_wholenet.clu
    * field2run1_accumulative1991-2012_22years_wholenet.vec
    * field2run1_accumulative1991-2012_22years_wholenet.all.txt

The next script to run is window.py. It produces collaboration networks and vector files for discrete networks. Before running the scrip, need to change the accumulative prefix and discrete prefix at the bottom.

###Geo Partition files:
=====================
Before we produce geo partition files, we need to check all the countries of the publications in our data has their country and continent in continent bank.
scripts:
* country.py
* codata.py

input file:

    * all_records.json

For country.py, we need all_records.json, generated at data processing steps, as input to check the countries for all publications. Run it once, and see if any country it prints out. If it printed out counties, them should be added into codata.py, i.e., add the country name as key, and give it a country code in cn_to_ccn. Then, add the country code as key, and continent as value to ccn_to_ctca2. Then, check again with country.py to see no country is printed.

scripts:
* geoAnalysis.py
* remapGC_geo.py

input files:

    * output.txt
    * all_records.json
    * field2run1_accumulative1991-2012_22years_wholenet.net
    * field2run1_accumulative1991-2012_22years_wholenet.clu

In geoAnalysis.py, some parameters need to be adjusted. 

    * accumulative prefix
    * years
    * discrete prefix
    * discrete postfix
    * year Range

After running for the first time, a json file contains intermediate dictionary for continent, year and cluster relationships saved in the directory. for editing, some line should be commented out. See details in script.

Two parameters in remapGC_geo.py:

    *accumulative GC network file
    *discrete collaboration network prefix


###Topic Partition Files:
=========================
scripts:
* topicAnalysis.py
* remapGC_topic.py

input files:

    * output.txt
    * field2run1_accumulative1991-2012_22years_wholenet.net
    * field2run1_accumulative1991-2012_22years_wholenet.clu
    * ArticleID-TopicID

In topicAnalysis.py, some parameters need to be adjusted. 

    * accumulative prefix
    * years
    * discrete prefix
    * discrete postfix
    * year Range
    * max TopicID in ArticleID-TopicID

After running topicAnalysis.py for the first time, a json file contains intermediate dictionary for topic, year and cluster relationships saved in the directory. For editing, some line should be commented out. See details in script.

Two parameters in remapGC_topic.py:

    * accumulative GC network file
    * discrete collaboration network prefix

###Topic Collaboration files: creates subview of collAboration network based on publications in a single topic area
=============================
scripts:
* topicCollab.py
* remapGC_topic_collab.py

input files:

    * output.txt
    * field2run1_accumulative1991-2012_22years_wholenet.net
    * field2run1_accumulative1991-2012_22years_wholenet.clu
    * discrete network prefix (all)
    * ArticleID-TopicID
    
In topicCollab.py, some parameters need to be adjusted. 

    * accumulative prefix
    * discrete prefix
this script produces topic concentated collaboration network based on discrete collaboration network. It also produces an intermediate file called records_topic.json, it saves all relationship between topic and publications

Two parameters in remapGC_topic.py:

    * accumulative GC network file
    * discrete collaboration network prefix

some other scripts:
* pub_gc.py
* quantitative.py
* evoPlot.py

pub_gc.py checks number of publications in giant component only by topics. it takes in accumulative collaboration network, accumulative collaboratoin giant component and records_topic.json to produce a plot of topic growth trends.

* quantitative.py and * evoPlot.py were used for sigmod, they can be edited to suit for other purposes.

