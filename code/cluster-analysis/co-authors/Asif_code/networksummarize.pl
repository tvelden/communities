#!/usr/bin/perl

# args: dirname fileprefix
# example: lab5run1_3 Lab5-lab5run1_3

# run from the "code" directory

# input: .net, .clu, .vec files
# output: 1 single file .snet
#  node_id size cluster
#  list of adjacent nodes
#  list of edge weights corresponding to adjacent nodes

use strict;

my $dirname= $ARGV[0];
my $basename= $ARGV[1];

my %nodesize= ();
my %clusterid= ();

my %adjacent= ();
my %weight= ();


open(NET, "$dirname/$basename.net");
#open(NET, "/Users/Kallol/Testing/nwa-field2/runs/run1/output/networks/discrete1991-2010_20years/whole_net/pajek/net_files/discrete1991-2010_20yearsCoauthorshipNetwork.net");

while(my $l= <NET>){
    chomp($l);
    if($l =~ /^\s*(\d+) \".*$/){
	$nodesize{$1}= 1;
	$clusterid{$1}= 0;
	my @a= ();
	$adjacent{$1}= \@a;
	my @b= ();
	$weight{$1}= \@b;
    }

    if($l =~ /^\s*(\d+)\s+(\d+)\s+(\d+)\s*$/){
	push(@{$adjacent{$1}}, $2);
	push(@{$adjacent{$2}}, $1);

	push(@{$weight{$1}}, $3);
	push(@{$weight{$2}}, $3);
    }
}

close(NET);

my $node;

open(SIZE, "$dirname/$basename.vec");
#open(SIZE, "/Users/Kallol/Testing/nwa-field2/runs/run1/output/networks/discrete1991-2010_20years/whole_net/pajek/net_files/discrete1991-2010_20yearsCoauthorshipNetwork.vec");

$node= 1;
while(my $l= <SIZE>){
    chomp($l);
    if($l =~ /^\s*(\d+)\s*$/){
	$nodesize{$node}= $1;
	$node++;
    }
}

close(SIZE);

open(CLUST, "$dirname/$basename.clu");
#open(CLUST, "/Users/Kallol/Testing/nwa-field2/runs/run1/output/networks/discrete1991-2010_20years/whole_net/pajek/net_files/discrete1991-2010_20yearsCoauthorshipNetwork.clu");

$node= 1;
while(my $l= <CLUST>){
    chomp($l);
    if($l =~ /^\s*(\d+)\s*$/){
	$clusterid{$node}= $1;
	$node++;
    }
}

close(CLUST);


open(SNET, ">$dirname/$basename.snet");
#open(SNET, ">/Users/Kallol/Testing/nwa-field2/runs/run1/output/networks/discrete1991-2010_20years/whole_net/pajek/net_files/discrete1991-2010_20yearsCoauthorshipNetwork.snet");


foreach $node (sort {$a <=> $b} keys %nodesize){
    print SNET "$node $nodesize{$node} $clusterid{$node}\n";
    $"= " ";
    print SNET "@{$adjacent{$node}}\n";
    print SNET "@{$weight{$node}}\n";
}

close(SNET);
