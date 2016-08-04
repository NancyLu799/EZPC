#! /usr/bin/perl 

use strict;

if ($#ARGV < 0)
{
	die "usage: solutionfile\n";
}

open(f,"<$ARGV[0]") or die "Cant open the file $ARGV[0]\n";
my $data = "";
my $currentcandidate = "";
while ($data = <f>)
{
	chomp($data);
	
	if ($data =~ /d_(\w+)/)
	{
		$currentcandidate = $1;
	}
	
	if ($data =~  /\*\s+1\s+0\s+1/)
	{
		open(my $fh, '>>', "$ARGV[1]");
		print $fh "$currentcandidate,";
		close $fh;
	}
	
}


