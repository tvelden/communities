#!/usr/bin/perl

# args: dirname
# example : lab5run1_3

# reads the dirname.snet file
# outputs (z, P) pair for each node,
#  skipping clusters with 0 std dev

use strict;

my $dirname= $ARGV[0];
my $outdirname= $ARGV[1];

my %nsize= ();
my %cid= ();
my %e= ();
my %w= ();
my %cs= ();

sub loadgraph {
    open(SNET, "$dirname.snet");
    #open(SNET, "/Users/Kallol/Testing/nwa-field2/runs/run1/output/networks/discrete1991-2010_20years/whole_net/pajek/net_files/discrete1991-2010_20yearsCoauthorshipNetwork.snet");

    my $li= 0;
    my $ln= 0;

    while(my $l= <SNET>){
	chomp($l);
	my @a= split(/\s+/, $l);

	if($li % 3 == 0){
	    $ln= $a[0];

	    $nsize{$ln}= $a[1];
	    $cid{$ln}= $a[2];

	    $cs{$a[2]}++;
	}

	if($li % 3 == 1){
	    $e{$ln}= \@a;
	}


	if($li % 3 == 2){
	    $w{$ln}= \@a;
	}


	$li++;
    }

    close(SNET);
}
##############################################

loadgraph;

my %ks= ();
my %kt= ();

foreach my $u (keys %nsize){
    my $t= 0;
    my %a= ();

    for(my $j= 0; $j <= $#{$e{$u}}; $j++){
	my $v= ${$e{$u}}[$j];
	my $wt= ${$w{$u}}[$j];

	$t+= $wt;
	$a{$cid{$v}}+= $wt;
    }

    $kt{$u}= $t;
    $ks{$u}= \%a;
}

my %ktc= ();
my %ktc2= ();

foreach my $u (keys %nsize){
    my $cu= $cid{$u};
    my $ku= ${$ks{$u}}{$cu};
    $ktc{$cu}+= $ku/$cs{$cu};
    $ktc2{$cu}+= $ku*$ku/$cs{$cu};
}


my %z= ();
my %P= ();

my $totalnodes= scalar(keys %nsize);

foreach my $u (keys %nsize){
    my $cu= $cid{$u};

    #next if $cs{$cu} <= $skipclustersize;

    next if $ktc2{$cu} <= $ktc{$cu}*$ktc{$cu};
    
    $z{$u}= (${$ks{$u}}{$cu} - $ktc{$cu})/sqrt($ktc2{$cu} - $ktc{$cu}*$ktc{$cu});

    $P{$u}= 1;

    foreach my $c (keys %cs){
	$P{$u}-= (${$ks{$u}}{$c}/$kt{$u})*(${$ks{$u}}{$c}/$kt{$u});
    }
}


my $processednodes= scalar(keys %z);

print "z-P values computed for $processednodes out of $totalnodes\n";

# number of authors in a cluster
my %authcount= ();

# number of hubs in a cluster
my %hubcount= ();


open(ALL, ">$outdirname.all.txt");
#open(ALL, ">/Users/Kallol/Testing/nwa-field2/runs/run1/output/networks/discrete1991-2010_20years/whole_net/pajek/net_files/discrete1991-2010_20yearsCoauthorshipNetwork.all.txt");
open(CON, ">$outdirname.con.txt");
#open(CON, ">/Users/Kallol/Testing/nwa-field2/runs/run1/output/networks/discrete1991-2010_20years/whole_net/pajek/net_files/discrete1991-2010_20yearsCoauthorshipNetwork.con.txt");

foreach my $u (sort {$z{$b} <=> $z{$a}} keys %z){

    my $cu= $cid{$u};
    my $mu= $ktc{$cu};
    my $sigma= sqrt($ktc2{$cu} - $ktc{$cu}*$ktc{$cu});

    my $ku= ${$ks{$u}}{$cu};

    my $class= 0;

    if($z{$u} < 2.5){ # non-hub
	$class= 1 if $P{$u} <= 0.05;
	$class= 2 if $P{$u} > 0.05 && $P{$u} <= 0.62;
	$class= 3 if $P{$u} > 0.62 && $P{$u} <= 0.8;
	$class= 4 if $P{$u} > 0.8;
    }
    else{ # hub
	$class= 5 if $P{$u} <= 0.3;
	$class= 6 if $P{$u} > 0.3 && $P{$u} <= 0.75;
	$class= 7 if $P{$u} > 0.75;
    }

    print ALL "$u $z{$u} $P{$u} $ku $mu $sigma R$class\n";

    my @a= @{$e{$u}};
    my $d= 0;
    for(my $j= 0; $j <= $#a; $j++){
	my $v= $a[$j];
	if($cid{$u} != $cid{$v}){
	    $d++;
	}
    }
    if($d > 0){
	print CON "$u $z{$u} $P{$u} $ku $mu $sigma R$class\n";
    }

    $authcount{$cu}++;
    $hubcount{$cu}++ if $class > 4;
}

close(CON);
close(ALL);

open(AU, ">$outdirname.authcount.txt");
open(HB, ">$outdirname.hubcount.txt");

#open(AU, ">/Users/Kallol/Testing/nwa-field2/runs/run1/output/networks/discrete1991-2010_20years/whole_net/pajek/net_files/discrete1991-2010_20yearsCoauthorshipNetwork.authcount.txt");
#open(HB, ">/Users/Kallol/Testing/nwa-field2/runs/run1/output/networks/discrete1991-2010_20years/whole_net/pajek/net_files/discrete1991-2010_20yearsCoauthorshipNetwork.hubcount.txt");

foreach my $cu (keys %authcount){
    print AU "$cu $authcount{$cu}\n";
    $hubcount{$cu}= 0 if !exists($hubcount{$cu});
    print HB "$cu $hubcount{$cu}\n";
}

close(HB);
close(AU);
