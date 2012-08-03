# !/usr/bin/perl

# arg: dirname fileprefix $y1 $y2

# $y1 and $y2 marks the middle period (inclusive)
# (, y1) [y1, y2] (y2, )

use strict;

my $dirname= $ARGV[0];
my $fileprefix= $ARGV[1];
my $y1= $ARGV[2];
my $y2= $ARGV[3];

open(YEAR, "../data/input/$dirname/$fileprefix-coauthors_community-net_giant-yearinfo.txt");
open(YC, ">../data/output/misc/$dirname.yearly.txt");

while(my $l= <YEAR>){
    chomp($l);
    my @a= split(/\s+/, $l);
    my $cu= shift(@a);

    my @b= (0, 0, 0);

    my $j;
    for($j= 0; $j <= $#a; $j++){
	if($a[$j] =~ /(\d{4}):(\d+)/){

	    my $y= $1;
	    my $c= $2;

	    $b[0]+= $c if $y < $y1;
	    $b[1]+= $c if $y >= $y1 && $y <= $y2;
	    $b[2]+= $c if $y > $y2;

	}
    }

    next if $b[0]+$b[1]+$b[2] == 0;

    my $class= 0;

    if($b[1] == 0){
	$class= 1 if $b[0] > 0;
	$class= 3 if $b[2] > 0;
	$class= 6 if $b[0] > 0 && $b[2] > 0;
    }
    else{
	$class= 2 if $b[0] == 0 && $b[2] == 0;
	$class= 4 if $b[0] > 0 && $b[2] == 0;
	$class= 5 if $b[0] == 0 && $b[2] > 0;
	$class= 6 if $b[0] > 0 && $b[2] > 0;
    }

    $"= " "; print YC "$cu @b $class\n";
}

close(YC);
close(YEAR);
