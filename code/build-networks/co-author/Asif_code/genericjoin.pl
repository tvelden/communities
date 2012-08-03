# !/bin/perl

# input list of files as arguments
# every line of every file should be in "key value" format
# the output is the join of all the files

my %h= ();

for my $arg (@ARGV){
    open(FIN, $arg);
    
    while(my $l= <FIN>){
	chomp($l);
	# key format \d+
	if($l =~ /(\d+)\s+(.+)/){
	    if(!exists($h{$1})){
		my @a= ();
		$h{$1}= \@a;
	    }
	    push(@{$h{$1}}, $2);
	}
    }

    close(FIN);
}

for my $paper (sort {$a <=> $b} keys %h){
#for my $paper (keys %h){
    # every table has this key
    if($#{$h{$paper}} == $#ARGV){
	$,= " ";
#	print "@{$h{$paper}}\n";
	print "$paper @{$h{$paper}}\n";
    }
}
