# !/usr/bin/perl

# args : dirname fileprefix
# example: lab5run1_3 Lab5-lab5run1_3

# outputs <original cluster id, pubs>

use strict;

my $dirname= $ARGV[0];
my $fileprefix= $ARGV[1];

# get the original index of the clusters

my @comind= (); # original index

open(CLU, "../data/input/$dirname/$fileprefix-coauthors_community-net_giant.clu");

my $l= <CLU>;
while($l= <CLU>){
    chomp($l);
    if($l =~ /^\s*(\d+)\s*$/){
	push(@comind, $1);
    }
    else{
	print STDERR "Error in parsing .clu\n";
    }
}

close(CLU);

# get the sizes

open(VEC, "../data/input/$dirname/$fileprefix-coauthors_community-net_giant-sizes_pubs.vec");

open(PUBS, ">../data/output/misc/$dirname.pubs.txt");

my $i= 0;
$l= <VEC>;
while($l= <VEC>){
    chomp($l);
    if($l =~ /^\s*(\d+)\s*$/){
	print PUBS "$comind[$i] $1\n";
    }
    else{
	print STDERR "Error in parsing .clu\n";
    }
    $i++;
}

close(PUBS);
close(VEC);
