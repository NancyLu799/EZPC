#! /usr/bin/perl

use strict;

if ($#ARGV < 5)
{
	die "usage: inputfeaturesfile col-constraintsfile row-constraintsfile groupconstraints pcsizemin pcsizemax solutionfile\n";
}


## read the config with 4 inputs -- policy, topology, mbox, switch
my $inputfile = $ARGV[0];
my $constraintsfile = $ARGV[1];
my $rowconstraintsfile = $ARGV[2];
my $groupconstraintsfile = $ARGV[3];
my $pcsizeminfile = $ARGV[4];
my $pcsizemaxfile = $ARGV[5];
my $formulationfile = "formulation.ilp";
my $solutionfile = $ARGV[6];

open (f,"<$pcsizeminfile") or die "Cant read configfile\n";
my $pcsizemin = do { local $/; <f> };
print "$pcsizemin";
close(f);
open (f,"<$pcsizemaxfile") or die "Cant read configfile\n";
my $pcsizemax = do { local $/; <f> };
close(f);
print "$pcsizemax";

open (f,"<$inputfile") or die "Cant read configfile\n";

my $firstline = <f>;
chomp($firstline);
my @featurenames = split(/,/,$firstline);
print "HERE $featurenames[$#featurenames] XXX\n";

my %feature_constraints = ();
my %candidates_features = ();
my %features_candidates = ();
my %candidates_index= ();
my %index_candidates= ();

my $data = "";
my $numcandidates = 0;
while ($data = <f>)
{
	chomp($data);
	my @candidate_fields = split(/,/,$data);
	my $candidate_name = $candidate_fields[0];
	$candidates_index{$candidate_name} = $numcandidates;
	$index_candidates{$numcandidates} = $candidate_name;
	my $j = 0;
	for ($j =1; $j <= $#candidate_fields; $j++)
	{
		my $featurename = $featurenames[$j];
		#print "HERE $j $featurename\n";
		if ($candidate_fields[$j] == 1)
		{
			$candidates_features{$candidate_name}->{$featurename}  =1;
			$features_candidates{$featurename}->{$candidate_name}  =1;
			if ($featurename eq "Industry")
			{
				print "Came here $candidate_name\n";
			}
		} 
	}
	$numcandidates++;
}
close(f);

open (f,"<$constraintsfile") or die "Cant read configfile\n";
my $firstline = <f>;
while ($data = <f>)
{
	chomp($data);
	my @constraints = split(/,/,$data);
	$feature_constraints{$constraints[0]}->{"min"} = $constraints[1];
	$feature_constraints{$constraints[0]}->{"max"} = $constraints[2];
}
close(f);


my %candidate_constraints = ();
open (f,"<$rowconstraintsfile") or die "Cant read configfile\n";
my $data = "";
while ($data = <f>)
{
	chomp($data);
	print "HERE $data\n";
	my @constraints = split(/,/,$data);
	$candidate_constraints{$constraints[0]} = $constraints[1];
	print "here $constraints[0] $constraints[1]\n"
}
close(f);




my $selectedvar = "d"; 

open(out1,">$formulationfile") or die "cant open $formulationfile\n";

print out1 "Minimize\n Cost:   ";

for (my $i  =0; $i < $numcandidates; $i++)
{
	my $thiscoveragevar ="$selectedvar"."_$index_candidates{$i}";	
	if ($i == 0)
	{
		print out1 "$thiscoveragevar";
	}
	else
	{
		print out1 " + $thiscoveragevar";
	}
}
print out1 " \n";


print out1 "Subject To\n";


## Number of members to select 
my $class = "";
print out1 "TOTALPCSIZEMAX: ";
for (my $i  =0; $i < $numcandidates; $i++)
{
	my $thiscoveragevar ="$selectedvar"."_$index_candidates{$i}";	
	if ($i == 0)
	{
		print out1 "$thiscoveragevar";
	}
	else
	{
		print out1 " + $thiscoveragevar";
	}
}
print out1 "  <= $pcsizemax\n";


print out1 "TOTALPCSIZEMIN: ";
for (my $i  =0; $i < $numcandidates; $i++)
{
	my $thiscoveragevar ="$selectedvar"."_$index_candidates{$i}";	
	if ($i == 0)
	{
		print out1 "$thiscoveragevar";
	}
	else
	{
		print out1 " + $thiscoveragevar";
	}
}
print out1 "  >= $pcsizemin\n";


## per feature constraints

my $feature = "";
foreach $feature (keys %feature_constraints)
{
	my $min = $feature_constraints{$feature}->{"min"};
	print out1 "FEATUREMIN.$feature: ";
	my $candidate = "";
	my $flag = 0;
	foreach $candidate (keys %{$features_candidates{$feature}})
	{	
		my $index = $candidates_index{$candidate};
		my $thiscoveragevar ="$selectedvar"."_$candidate";	
		if ($flag == 0)
		{
			print out1 "$thiscoveragevar";
			$flag = 1;

		}
		else
		{
			print out1 " + $thiscoveragevar";
		}
	}
	print out1 " >= $min\n"; 
	my $max = $feature_constraints{$feature}->{"max"};
	print out1 "FEATUREMAX.$feature: ";
	my $candidate = "";
	my $flag = 0;
	foreach $candidate (keys %{$features_candidates{$feature}})
	{	
		my $index = $candidates_index{$candidate};
		my $thiscoveragevar ="$selectedvar"."_$candidate";	
		if ($flag == 0)
		{
			print out1 "$thiscoveragevar";
			$flag = 1;
		}
		else
		{
			print out1 " + $thiscoveragevar";
		}
	}
	print out1 " <= $max\n"; 
}

## per candidate constraints
my $candidate = "";
foreach $candidate (keys %candidate_constraints)
{
	my $thiscoveragevar ="$selectedvar"."_$candidate";	
	print out1 "CANDIDATE.$candidate:  $thiscoveragevar = $candidate_constraints{$candidate}\n";
}

## Candidate group constraints

open (f,"<$groupconstraintsfile") or die "Cant read configfile\n";
my $groupid = 1;
while ($data = <f>)
{
	chomp($data);
	print "HERE $data\n";
	my ($constname, $names,$max) = split(/\s+/,$data);
	my @people = split(/,/,$names);
	print out1 "GROUPCONST.$constname: ";
	my $flag = 0;
	foreach $candidate (@people)
	{
		my $thiscoveragevar ="$selectedvar"."_$candidate";	
		if ($flag ==0 )
		{
			print out1 "  $thiscoveragevar ";
			$flag = 1;
		}	
		else
		{
			print out1 " +  $thiscoveragevar ";

		}
	}
	print out1 " <= $max\n";
	$groupid++;
}
close(f);



	

print out1 "Binaries\n";

my $class = "";
for (my $i  =0; $i < $numcandidates; $i++)
{
	my $thisactivevar ="$selectedvar"."_$index_candidates{$i}";	
	print out1 "$thisactivevar\n";
}


print out1 "End\n";
close(out1); 

system(" glpsol --lp $formulationfile -o $solutionfile");