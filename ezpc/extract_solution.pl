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
	if ($data =~  /\*\s+0\s+0\s+1/)
	{
		
		open(my $fh, '>', "media/files/parsedsolution.txt");
		print $fh "Not Selected: $currentcandidate\n";
		close $fh;
		print "Selected: $currentcandidate";
		
	}
	if ($data =~  /\*\s+1\s+0\s+1/)
	{
		open(my $fh, '>>', "media/files/parsedsolution.txt");
		print $fh "Selected: $currentcandidate\n";
		close $fh;
		print "Selected: $currentcandidate";
	}
	
}


