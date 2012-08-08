# !/usr/bin/perl

# args : dirname

use strict;

my $dirname= $ARGV[0];

##############################################
my %nsize= ();
my %cid= ();
my %e= ();
my %w= ();
my %cs= ();

sub loadgraph {
    open(SNET, "../data/output/network/$dirname.snet");

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

my %role= ();

open(ROLE, "../data/output/zP/$dirname.all.txt");

while(my $l= <ROLE>){
    chomp($l);

    my @a= split(/\s+/, $l);

    $role{$a[0]}= $a[6];
}

close(ROLE);

open(ER, ">../data/output/edgeswithnoderoles/$dirname.txt");

foreach my $u (keys %role){
    my @eu= @{$e{$u}};
    my @wu= @{$w{$u}};

    for(my $i= 0; $i <= $#eu; $i++){
	my $v= $eu[$i];
	my $ww= $wu[$i];

	if(exists($role{$v}) && ($role{$u} le $role{$v})){
	    print ER "$role{$u}-$role{$v} $ww $cid{$u} $cid{$v}\n";
	}
    }
}

close(ER);
