# !/usr/bin/perl

# args: dirname fileprefix
# example: lab5run1_3 Lab5-lab5run1_3

# reads the dirname.snet file
# outputs 2 files for two graphs
#   transfer and collaborative edges

use strict;

my $dirname= $ARGV[0];
my $fileprefix= $ARGV[1];

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


my %eu= ();
my %ev= ();

my %ew= ();
my %ec= ();

foreach my $u (keys %nsize){
    for(my $j= 0; $j <= $#{$e{$u}}; $j++){
	my $v= ${$e{$u}}[$j];
	my $wt= ${$w{$u}}[$j];
	
	if($cid{$u} < $cid{$v}){
	    my $s= "$cid{$u}:$cid{$v}";
	    
	    if(!exists($ec{$s})){
		$ec{$s}= 0;
		my @au= (); $eu{$s}= \@au;
		my @av= (); $ev{$s}= \@av;
		my @aw= (); $ew{$s}= \@aw;
	    }
	    
	    push(@{$eu{$s}}, $u);
	    push(@{$ev{$s}}, $v);
	    push(@{$ew{$s}}, $wt);
	    
	    # edge weight count
	    $ec{$s}+= $wt;
	}
    }
}


open(OM, ">../data/output/transfercollaboration/$dirname.transfer.net");
open(MM, ">../data/output/transfercollaboration/$dirname.collab.net");

open(COMNET, "../data/input/$dirname/$fileprefix-coauthors_giant.net");

open(E, ">../data/output/misc/$dirname.edges.txt");

my $l= <COMNET>;
chomp($l);

if($l =~ /^\*Vertices\s+(\d+)\s*$/){

    my $cl= $1;

    print OM  "*Vertices $cl\r\n";
    print MM  "*Vertices $cl\r\n";

    my $i;
    for($i= 0; $i < $cl; $i++){
	$l= <COMNET>;
	
	print OM  "$l";
	print MM  "$l";
    }

    print OM  "*Edges\r\n";
    print MM  "*Edges\r\n";

    foreach my $s (keys %ec){
	my %fu= ();
	foreach my $u (@{$eu{$s}}){
	    $fu{$u}++;
	}

	my $uc= scalar(keys %fu);

	my %fv= ();
	foreach my $v (@{$ev{$s}}){
	    $fv{$v}++;
	}
	
	my $vc= scalar(keys %fv);

	my @a= split(/:/, $s);
	my $cu= shift(@a);
	my $cv= shift(@a);


	my $fc= 0; # 0 for collab, 1 for trans

	# m-m, m > 2
	if($uc > 2 && $vc > 2){
	    my @kfu= keys %fu;
	    my @kfv= keys %fv;

	    my @tfu= @kfu;
	    my @tfv= @kfv;

	    for(my $i= 0; $i <= $#kfu && $fc == 0; $i++){
		my $tu= $kfu[$i];

		$tfu[$i]= $kfu[$#kfu];
		pop(@tfu);

		for(my $j= 0; $j <= $#kfv && $fc == 0; $j++){
		    my $tv= $kfv[$j];

		    $tfv[$j]= $kfv[$#kfv];
		    pop(@tfv);

		    $fc++ if !isconnected(\@tfu, \@tfv);

		    push(@tfv, $kfv[$#kfv]);
		    $tfv[$j]= $tv;
		}

		push(@tfu, $kfu[$#kfu]);
		$tfu[$i]= $tu;
	    }
	}
	# 1-m, m >= 1 and 2-m, m >= 2
	else{
	    $fc++;
	}
	
	# print edges
	my %dn= ();
	
	foreach my $u (@{$eu{$s}}){
	    
	    next if exists($dn{$u});
	    $dn{$u}++;
	    
	    my @el= @{$e{$u}};
	    my @wl= @{$w{$u}};
	    
	    for(my $j= 0; $j <= $#el; $j++){
		my $v= $el[$j];

		if($cid{$v} == $cv){
		    if($fc == 0){
			print MM "$u $v $wl[$j]\r\n";
			print E "$u $v $wl[$j] 2\n";
		    }
		    else{
			print OM "$u $v $wl[$j]\r\n";
			print E "$u $v $wl[$j] 1\n";
		    }
		}
	    }
	}
    }

    foreach my $u (keys %e){
	my @el= @{$e{$u}};
	my @wl= @{$w{$u}};

	for(my $j= 0; $j <= $#el; $j++){
	    my $v= $el[$j];

	    next if ($u > $v || $cid{$u} != $cid{$v});
		
	    print MM "$u $v $wl[$j]\r\n";
	    print OM "$u $v $wl[$j]\r\n";
	    print E "$u $v $wl[$j] 0\n";
	}
    }

}
else{
    print STDERR "Something went wrong!\n";
}

close(E);

close(COMNET);

close(MM);
close(OM);

sub isconnected {
    # return 1 if the two set of nodes have any edge
    my @p= @{$_[0]};
    my @q= @{$_[1]};

    foreach my $i (@p){
	foreach my $j (@q){
	    return 1 if $i == $j;
	    if(scalar(@{$e{$i}}) <= scalar(@{$e{$j}})){
		foreach my $k (@{$e{$i}}){
		    return 1 if $j == $k;
		}
	    }
	    else{
		foreach my $k (@{$e{$j}}){
		    return 1 if $i == $k;
		}
	    }
	}
    }

    return 0;
}
