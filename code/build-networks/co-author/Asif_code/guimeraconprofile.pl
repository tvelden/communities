# !/usr/bin/perl

# argument : dirname fileprefix ensembles
# example: lab5run1_3 Lab5-lab5run1_3 100

use strict;

my $dirname= $ARGV[0];
my $fileprefix= $ARGV[1];

my $ensembles= $ARGV[2];

my %r= ();

open(R, "../data/output/zP/$dirname.all.txt");

while(my $l= <R>){
    chomp($l);
    my @a= split(/\s+/, $l);
    my $k= $a[0];
    $r{$k}= $a[6];
}

close(R);

my %rij= ();

my $ef= 0;

open(A, "../data/input/$dirname/$fileprefix-coauthors_giant.net");

while(my $l= <A>){
    chomp($l);
    
    if($ef == 1){

	if($l =~ /^\s*(\d+)\s+(\d+)\s+(\d+).*/){

	    my $u= $1;
	    my $v= $2;
	    my $w= $3;

	    if(exists($r{$u}) && exists($r{$v})){

		my $ru= $r{$u};
		my $rv= $r{$v};
		
		my $ruv;
		if($ru le $rv){
		    $ruv= "$ru-$rv";
		}
		else{
		    $ruv= "$rv-$ru";
		}
		
		$rij{$ruv}+= $w;
	    }
	}
    }
    
    $ef= 1 if $l =~ /^\*Edges.*/;
}

close(A);

my @trij= ();

for(my $i= 1; $i <= $ensembles; $i++){
    open(RE, "../data/output/random-ensemble/$dirname/$i.snet");

    my %nsize= ();
    my %cid= ();
    my %e= ();
    my %w= ();
    my %cs= ();

    my $li= 0;
    my $ln= 0;

    while(my $l= <RE>){
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

    close(RE);

    my %c= ();
    push(@trij, %c);

    foreach my $u (keys %nsize){
	for(my $k= 0; $k <= $#{$e{$u}}; $k++){
	    my $v= ${$e{$u}}[$k];
	    my $w= ${$w{$u}}[$k];

	    next if $u > $v;

	    if(exists($r{$u}) && exists($r{$v})){

		my $ru= $r{$u};
		my $rv= $r{$v};
		
		my $ruv;
		if($ru le $rv){
		    $ruv= "$ru-$rv";
		}
		else{
		    $ruv= "$rv-$ru";
		}
		
		${$trij[$i-1]}{$ruv}+= $w;
	    }
	    
	}
    }
    
}


#open(G, ">../data/output/guimeraprofile/$dirname.txt");

open(G, ">../data/output/misc/guimeraprofile.$dirname.txt");

for(my $t1= 1; $t1 <= 7; $t1++){
    for(my $t2= $t1; $t2 <= 7; $t2++){
	my $ruv= "R$t1-R$t2";

	$rij{$ruv}= 0 if !exists($rij{$ruv});

	print G "$rij{$ruv}";
	for(my $i= 1; $i <= $ensembles; $i++){
	    ${$trij[$i-1]}{$ruv}= 0 if !exists(${$trij[$i-1]}{$ruv});
	    print G " ${$trij[$i-1]}{$ruv}";
	}
	print G "\n";
    }
}

close(G);
