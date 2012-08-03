# !/usr/bin/perl

# args: dirname ensembles
# example: lab5run1_3 10

# reads the dirname.snet file
# generates random ensemble of snets

use strict;

my $dirname= $ARGV[0];
my $ensembles= $ARGV[1];

print STDERR "Generating $ensembles random networks for $dirname...\n";


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


################ edge list ####################

my %edgeweights= ();
my %intercluster= ();

foreach my $i (keys %nsize){
    for(my $jj= 0; $jj <= $#{$e{$i}}; $jj++){
	my $j= ${$e{$i}}[$jj];
	my $wt= ${$w{$i}}[$jj];

	if($i < $j){
	    my $s= "$i-$j";
	    $edgeweights{$s}= $wt;

	    my $t= "$cid{$i}-$cid{$j}";
	    $t= "$cid{$j}-$cid{$i}" if $cid{$j} < $cid{$i};

	    if(!exists($intercluster{$t})){
		my @c= ();
		$intercluster{$t}= \@c;
	    }

	    push(@{$intercluster{$t}}, $s);
	}
    }
}

###############################################


for(my $it= 1; $it <= $ensembles; $it++){

    print STDERR " $it";

    my %tew= ();

    my %cedgeweights= %edgeweights; ## copy weights
    
    foreach my $t (keys %intercluster){
	my @c= sort {$edgeweights{$a} <=> $edgeweights{$b}} @{$intercluster{$t}};

	while($#c > 0){
	    my $s1= $c[$#c];
	    $#c--; # largest edge removed

	    while($cedgeweights{$s1} > 0 && $#c >= 0){
		my $j= int(rand($#c));
		my $s2= $c[$j];

		## random weights
		#my $dmax= $cedgeweights{$s1};
		#$dmax= $cedgeweights{$s2} if $cedgeweights{$s2} < $cedgeweights{$s1};
		#my $d= 1+int(rand($dmax-1));
		
		my $d= 1;

		$cedgeweights{$s1}-= $d;
		
		$cedgeweights{$s2}-= $d;

		if($cedgeweights{$s2} == 0){
		    $c[$j]= $c[$#c]; $#c--;
		}

		my $i1;
		my $j1;
		if($s1 =~ /(\d+)\-(\d+)/){
		    $i1= $1;
		    $j1= $2;
		}
		
		my $i2;
		my $j2;
		if($s2 =~ /(\d+)\-(\d+)/){
		    $i2= $1;
		    $j2= $2;
		}
		
		if($cid{$i1} == $cid{$i2}){
		    $tew{"$i1-$j2"}+= $d if $i1 <= $j2;
		    $tew{"$j2-$i1"}+= $d if $i1 > $j2;
		    
		    $tew{"$i2-$j1"}+= $d if $i2 <= $j1;
		    $tew{"$j1-$i2"}+= $d if $i2 > $j1;
		}
		else{
		    $tew{"$i1-$i2"}+= $d if $i1 <= $i2;
		    $tew{"$i2-$i1"}+= $d if $i1 > $i2;
		    
		    $tew{"$j1-$j2"}+= $d if $j1 <= $j2;
		    $tew{"$j2-$j1"}+= $d if $j1 > $j2;
		}
	    }
	}

	$tew{$c[0]}= $cedgeweights{$c[0]} if $#c == 0;

######################## random reweighting ####################################

#	while($#c > 0){
#	    ## pick 2 edges
	    
#	    my $i= int(rand($#c));
#	    my $s1= $c[$i];
#	    $c[$i]= $c[$#c];
#	    $#c--; ## throw out done edges

#	    my $j= int(rand($#c));
#	    my $s2= $c[$j];
#	    $c[$j]= $c[$#c];
#	    $#c--; ## throw out done edges
#	    
#	    my $dmax= $edgeweights{$s1};
#	    $dmax= $edgeweights{$s2} if $edgeweights{$s2} < $edgeweights{$s1};

#	    my $d= 1+int(rand($dmax-1));

#	    $tew{$s1}= $edgeweights{$s1}-$d;
#	    $tew{$s2}= $edgeweights{$s2}-$d;

#	    my $i1;
#	    my $j1;
#	    if($s1 =~ /(\d+)\-(\d+)/){
#		$i1= $1;
#		$j1= $2;
#	    }

#	    my $i2;
#	    my $j2;
#	    if($s2 =~ /(\d+)\-(\d+)/){
#		$i2= $1;
#		$j2= $2;
#	    }
	    
#	    if($cid{$i1} == $cid{$i2}){
#		$tew{"$i1-$j2"}+= $d if $i1 < $j2;
#		$tew{"$j2-$i1"}+= $d if $i1 > $j2;

#		$tew{"$i2-$j1"}+= $d if $i2 < $j1;
#		$tew{"$j1-$i2"}+= $d if $i2 > $j1;
#	    }
#	    else{
#		$tew{"$i1-$i2"}+= $d if $i1 < $i2;
#		$tew{"$i2-$i1"}+= $d if $i1 > $i2;

#		$tew{"$j1-$j2"}+= $d if $j1 < $j2;
#		$tew{"$j2-$j1"}+= $d if $j1 > $j2;
#	    }
#	}

#	## if odd number of edges
#	$tew{$c[0]}= $edgeweights{$c[0]} if $#c == 0;

####################################################################################	

    }



    #### back to snet and print #####

    my %te= ();
    my %tw= ();
    
    foreach my $s (keys %tew){
	if($s =~ /(\d+)\-(\d+)/){
	    my $i= $1;
	    my $j= $2;
	    
	    if(!exists($te{$i})){
		my @a= ();
		$te{$i}= \@a;
		
		my @b= ();
		$tw{$i}= \@b;
	    }
	    if(!exists($te{$j})){
		my @a= ();
		$te{$j}= \@a;
		
		my @b= ();
		$tw{$j}= \@b;
	    }
	    
	    push(@{$te{$i}}, $j);
	    push(@{$te{$j}}, $i);
	    
	    push(@{$tw{$i}}, $tew{$s});
	    push(@{$tw{$j}}, $tew{$s});
	}
    }
    
    open(RE, ">../data/output/random-ensemble/$dirname/$it.snet");

    foreach my $i (keys %nsize){
	print RE "$i $nsize{$i} $cid{$i}\n";
	if(exists($te{$i})){
	    $"= " "; print RE "@{$te{$i}}\n";
	    $"= " "; print RE "@{$tw{$i}}\n";
	}
	else{
	    print STDERR "No edges : $i\n";
	}
    }

    close(RE);
}

print STDERR "\n";
