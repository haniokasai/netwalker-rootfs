#!/usr/bin/perl -Tw
require 5.006_001;
use strict;

=head1 NAME

Spamitarium - where the spam's head gets fixed...

=cut

my $version = "0.2.1";

################################################
############### Copyleft Notice ################
################################################

# Copyright � 2004 Order amid Chaos, Inc.
# Author: Tom Anderson 
# neo+spamitarium@orderamidchaos.com
# 
# This program is open-source software; you can redistribute it 
# and/or modify it under the terms of the GNU General Public 
# License, v2, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with this program; if not, write to: 
#
# Free Software Foundation 
# 59 Temple Place, Suite 330
# Boston, MA 02111-1307  USA
#
# http://www.gnu.org/

#################################################
################# Documentation #################
#################################################

# use "perldoc spamitarium" or "spamitarium -h" to read this

=head1 SYNOPSIS

=head2 Command line usage:

B<spamitarium> [I<options>] [I<permitted_headers>] < [I<rfc822_email>]

=head2 Procmail usage (recommended):

Add to ~/.procmailrc the following recipe, where I<$HOME> 
is your home directory, if not set in the environment:

  :0
  {
	:0 fhw
	| $HOME/.bogofilter/spamitarium -sread
  
	# filter through bogofilter, tagging as spam 
	# or not and updating the word lists
	:0 fw
	| bogofilter -uep

	# add back the "From" header for proper delivery
	:0 fhw
	| formail -I "From " -a "From "
  }

=head2 Command line options:

=over 4

=item B<h>

display this help file

=item B<s>

allow standard fields only (RFC 822/2822/1049/1341/1521/2183/1864) ...
all others are stripped from the email

=item B<r>

insert new received line containing verified received-line tokens

=item B<e>

include helo string in received line

=item B<d>

allow DNS lookups (forward and reverse) to help fill in all 
necessary received fields

=item B<f>

force rDNS lookups even when provided already by the MTA

=item B<a>

perform ASN lookups and include in received lines

=item B<w>

parse and display the body of the email in addition to the headers

=item B<b>

display benchmarking info

=back


=head2 User-defined header field list:

If using the B<s> option, you may want to allow certain header fields
other than those specified by RFCs.  These might include fields set
by your mailing list or proxy or other custom application.  You may
specify such a list of fields by appending them comma-delimited at
the end of your command line.  For example, if you wanted the 
I<list-id> and I<encrypted> fields passed through, you would change
your procmail recipe as follows:

  | $HOME/.bogofilter/spamitarium -sread list-id,encrypted


=head1 REQUIRES

=over 4

=item *

Perl 5.6.1

=back


=head1 DESCRIPTION

Spamitarium helps to remove unnecessary noise from email headers and
to highlight just the portions which contribute positively to spam
filtering using statistical methods.

The only non-spoofable, -forgable, or -tweakable part of
an email is the received line, as it is generated by the receiving
mail server which ought to have no reason to munge it.  Every other
part of an email can be influenced directly by the sender.  Received
line tokens, when verified authentic, are therefore highly indicative
of whether or not a given message is spam.  

Spamitarium reads the received headers, determines which ones are
authentic, and then prints tokens into the header which may be keyed
on by statistical filters.  This works much like a blacklist/whitelist, 
but when coupled with a statistical filter such as bogofilter, these 
lists are automatically generated and require no manual maintenance 
other than normal training.

Moreover, headers which do not directly influence the email in any
functional way, nor are visible to the end-user in a standard
graphical MUA, are highly likely to contain information which 
spammers think will detract from normal statistical filtering. It
is therefore desireable to remove these elements, specifically 
X-headers, prior to filtering.  Spamitarium removes all invisible,
non-functional header lines.

Finally, spamitarium looks up any IP addresses or rDNS addresses
which are not provided in order to provide the maximum tokens on
which to filter.  Moreover, it looks up the ASN (autonomous system
number) associated with each "from" address in order to provide
a small set of tokens representing the various major subnets of the
internet.

Together, all of these techniques help to remove the noise which
accompanies, either incidentally or maliciously, most email messages.
This results in a cleaner header consisting of more easily scored
tokens.  This permits better accuracy with statistical filters as
well as quicker processing and a smaller token database.


=head1 FAQ

=head2 Ask a question

Ye may receive an answer here if it is asked frequently


=head1 BUGS

=over 4

=item *

Please report any.

=back


=head1 TODO

=over 4

=item *

Suggestions welcome.

=back


=head1 SEE ALSO

=over 4

=item *

L<procmail>

=item *

L<bogofilter>

=back


=head1 AUTHOR

Tom Anderson <neo+spamitarium@orderamidchaos.com>

=cut

#################################################
############### User Variables  #################
#################################################

# please edit according to your setup

# default path
our $path = "/bin:/usr/bin:/usr/local/bin";

# default shell
our $shell = "/bin/sh";

# seconds before we bail waiting on input
our $timeout = 3;

# server to use for ASN lookups
our $asn_server = "asn.routeviews.org";

# of course, modify the first line of this file,
# the shebang, to point to your perl interpreter

# do not edit below this line unless you really
# know what you're doing

#################################################
############## Include Libraries ################
#################################################

use Benchmark;

#################################################
############## Default Globals ##################
#################################################

$> = $<; # set effective user ID to real UID
$) = $(; # set effective group ID to real GID

# Make %ENV safer
delete @ENV{qw(IFS CDPATH ENV BASH_ENV PATH SHELL)};

# Set the environment explicitely
$ENV{PATH} = $path;
$ENV{SHELL} = $shell;

# options flags
our $options = "";

# list of allowed headers
our $user_fields = "";

# define the control-linefeed syntax for this system
our $CRLF = 
"\n";
#($^O=~/VMS/i)? 	"\n": 		# VMS
#("\t" ne "\011")? 	"\r\n": 	# EBCDIC
#			"\015\012"; 	# others 

################################################
##################### Main #####################
################################################

# process options
if (!defined @ARGV || $ARGV[0] !~ /[^\s]/ || $ARGV[0] =~ /h/) 
{
	my $spamitarium = $1 if $0 =~ /^([\w\/.\-~]*)$/;
	system("perldoc $spamitarium"); exit(0);
}
if ($ARGV[0] =~ /r/) { $options .= "r"; }	# process received headers
if ($ARGV[0] =~ /d/) { $options .= "d"; }	# perform domain lookups where needed
if ($ARGV[0] =~ /f/) { $options .= "f"; }	# force RDNS lookups even where MTA provided
if ($ARGV[0] =~ /a/) { $options .= "a"; }	# perform ASN lookups
if ($ARGV[0] =~ /s/) { $options .= "s"; }	# standard fields only (strip others)
if ($ARGV[0] =~ /e/) { $options .= "e"; }	# include the helo received field in output
if ($ARGV[0] =~ /b/) { $options .= "b"; }	# output benchmarking info
if ($ARGV[0] =~ /w/) { $options .= "w"; }	# process whole email (including body)

# get the permitted headers
if ($options =~ /s/ && $ARGV[1]) { $user_fields = $ARGV[1]; }

# start timing the process
my $start_time = new Benchmark if $options =~ /b/;

# get STDIN and process the email
eval 
{
	# set an alarm so that we don't hang on an empty STDIN
	local $SIG{ALRM} = sub { die "timeout" };
	alarm $timeout;

	# parse the header
	my $header = parse_header();
	
	# cancel timeout if we got this far
	alarm 0;
	
	# process the received lines
	$header->{'received'} = process_rcvd($header->{'received'},$header->{'date'}->[0]->{'string'}) if $options =~ /r/;

	#print "received: " . $header->{'received'} . ": " . $header->{'received'}->[0] . ": " . $header->{'received'}->[0]->{'sane'} . "\n";

	# output the new header containing the changes
	print set_header($header);

	# add the body if desired
	print parse_body() if $options =~ /w/;
};

# propagate errors
die if $@ && $@ !~ /timeout/i;

# print timeout message
if ($@ =~ /timeout/i) { error("die","Timed out... make sure to supply an email for processing.  Try 'spamitarium -h' for details.\n"); }

# calculate total running time
if ($options =~ /b/)
{
	my $end_time = new Benchmark;  
	my $td = timediff($end_time, $start_time);
	my $usr = $td->[1]+$td->[3]; my $sys = $td->[2]+$td->[4];
	my $cpu = $usr+$sys; my $wall = $td->[0];
	print "Total running time was $wall wallclock secs; $usr usr + $sys sys = $cpu CPU secs.$CRLF";
}

exit(0);

################################################
################ Parse Header  #################
################################################

sub parse_header
{
	my %header;
	my $name = "";

	while (<STDIN>)
	{
		alarm 0; 

		my $line = $_;

		# we're done with the header when we've found a blank line
		last if (!defined $line || $line !~ /[^\s]/);

		# start matching header lines
		if ($line =~ /^((?:\w|-)+?): (.*?)$/)
		{
			my $head = $1; my $value = $2;
			$name = $head;
			
			$name =~ tr/A-Z/a-z/;	# header names are case insensitive
			$value =~ s/\s+?/ /gis;	# unfold header lines by removing CRLF
			$value =~ s/(\S)$/$1 /;
			
			# if this header name has already been found, append to the end of the array
			my $count = ((defined $header{$name}) && (ref($header{$name}) eq "ARRAY"))? scalar @{$header{$name}} : 0;
			
			# record this header line
			$header{$name}[$count]{'string'} = $value;
			$header{$name}[$count]{'name'} = $head; # just for consistency
			
			#print "$name [$count] = $value$CRLF";
		}
		
		# if this line doesn't start with "header:", append to last line found (if exists)
		elsif ($name) { $line =~ s/\s+?/ /gis; $line =~ s/^\s//; $header{$name}[(scalar @{$header{$name}} - 1)]{'string'} .= $line if ((defined $header{$name}) && (ref($header{$name}) eq "ARRAY")); }
	}
	
	return \%header;
}

################################################
################# Parse Body  ##################
################################################

sub parse_body
{
	# this function is really only used for
	# email-to-email comparisons, where processing
	# the entire email is required... usually
	# we'll just process the header

	my $body = "";
	while (<STDIN>) { $body .= $_; }
	return $body;
}		

################################################
########### Process Received Lines  ############
################################################

sub process_rcvd
{
	my $rcvd = shift;
	my $date = shift;
	
	# heuristics
	my $LUSER	= qr~(?:\w|-|\.)+?~;
	my $DOMAIN	= qr~(?:\w|-|\.)+\.\w{2,4}~;
	my $IP		= qr~(?:\d{1,3}\.){3}\d{1,3}~;
	my $EMAIL 	= qr~$LUSER\@$DOMAIN~;
	my $HELO	= qr~[^\s\0\/\\\#]+?~;
	my $RDNS	= qr~(?:$DOMAIN|\[?$IP\]?|unknown|unverified)~;
	
	my $edge_ip = "";
	my $untrusted = 0;

	# check if we were passed a valid array of received lines
	unless ((defined $rcvd) && (ref($rcvd) eq "ARRAY") && $rcvd->[0]->{'string'})
	{
		no strict 'refs';
		my %rcvd_hash = ('string'=>"from localhost; $date", 'name'=>"Received");
		my @rcvd_array; $rcvd_array[0] = \%rcvd_hash;  $rcvd = \@rcvd_array;
	}

	# iterate through each received header, parsing and validating the info
	for (my $x = 0; $x < scalar @$rcvd; $x++)
	{
		# skip processing if we already lost confidence in this trail of received lines
		if ($untrusted) { $rcvd->[$x]->{'sane'} = "untrusted"; next; }
	
		my $helo=""; my $ipad=""; my $rdns=""; my $idnt=""; my $from=""; 
		my $mtan=""; my $mtai=""; my $mtav=""; my $fore=""; my $with=""; my $date="";
		
		# try to take into account all known MTA formats
		
		if    ($rcvd->[$x]->{'string'} =~ s/\(envelope-(?:sender|from) <($EMAIL)>\)//gis) 			{ $from=$1; 					}#print "X-$x-matched-01: from=$from$CRLF"; }
		if    ($rcvd->[$x]->{'string'} =~ s/;\s+?(\w{3}, \d{1,2} \w{3} \d{2,4}.*?)$//gis)			{ $date=$1; 					}#print "X-$x-matched-02: date=$date$CRLF"; }
		if    ($rcvd->[$x]->{'string'} =~ s/for\s+?<?($EMAIL)>?(?: \(single-drop\))?//gis) 			{ $fore=$1; 					}#print "X-$x-matched-03: fore=$fore$CRLF"; }
		if    ($rcvd->[$x]->{'string'} =~ s/by\s+?(\S+?) \(($IP)\) \((.*?)\)//gis) 				{ $mtan=$1; $mtai=$2; $mtav=$3; 		}#print "X-$x-matched-04: mtan=$mtan, mtai=$mtai, mtav=$mtav$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/by\s+?(\S+?) \[($IP)\]//gis) 					{ $mtan=$1; $mtai=$2; 				}#print "X-$x-matched-05: mtan=$mtan, mtai=$mtai$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/by\s+?(\S+?) \((.+?)\)//gis) 					{ $mtan=$1; $mtav=$2; 				}#print "X-$x-matched-06: mtan=$mtan, mtav=$mtav$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/by\s+?($IP)(?=\W|;|$)//gis) 					{ $mtai=$1; 					}#print "X-$x-matched-07: mtai=$mtai$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/by\s+?($DOMAIN)(?=\W|;|$)//gis) 					{ $mtan=$1; 					}#print "X-$x-matched-08: mtan=$mtan$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/by\s+?(\S+?)(?=\W|;|$)//gis) 					{ $mtan=$1; 					}#print "X-$x-matched-09: mtan=$mtan$CRLF"; }
		if    ($rcvd->[$x]->{'string'} =~ s/(?:with)\s+?(\S+?) \((.*?)\)//gis) 					{ $with=$1; $mtav=$2 if !$mtav; 		}#print "X-$x-matched-10: with=$with, mtav=$mtav$CRLF";}
		elsif ($rcvd->[$x]->{'string'} =~ s/(?:with)\s+?(\S+?)(?=\W|;|$)//gis) 					{ $with=$1; 					}#print "X-$x-matched-11: with=$with$CRLF"; }
		if    ($rcvd->[$x]->{'string'} =~ s/^from\s+?($RDNS) \(HELO ($HELO)\) \(($LUSER)\@\[?($IP)\]?//gis) 	{ $rdns=$1; $helo=$2; $idnt=$3; $ipad=$4; 	}#print "X-$x-matched-12: rdns=$rdns, helo=$helo, idnt=$idnt, ipad=$ipad$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($RDNS) \(HELO ($HELO)\) \(\[?($IP)\]?//gis) 		{ $rdns=$1; $helo=$2; $ipad=$3; 		}#print "X-$x-matched-13: rdns=$rdns, helo=$helo, ipad=$ipad$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($RDNS) \(\[($IP)\] helo=($HELO)\)//gis) 			{ $rdns=$1; $ipad=$2; $helo=$3; 		}#print "X-$x-matched-14: rdns=$rdns, ipad=$ipad, helo=$helo$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($RDNS) \(($LUSER)\@\[?($IP)\]?\)//gis) 			{ $rdns=$1; $idnt=$2; $ipad=$3; 		}#print "X-$x-matched-15: rdns=$rdns, idnt=$idnt, ipad=$ipad$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($RDNS)\(($IP)\)//gis) 					{ $rdns=$1; $ipad=$2; 				}#print "X-$x-matched-16: rdns=$rdns, ipad=$ipad$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?\[($IP)\] \(helo=($HELO) ident=($LUSER)\)//gis) 		{ $ipad=$1; $helo=$2; $idnt=$3; 		}#print "X-$x-matched-17: ipad=$ipad, helo=$helo, idnt=$idnt$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?\[($IP)\] \(account ($LUSER) HELO ($HELO)\)//gis) 		{ $ipad=$1; $idnt=$2; $helo=$3; 		}#print "X-$x-matched-18: ipad=$ipad, idnt=$idnt, helo=$helo$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?\[($IP)\] \(helo=($HELO)\)//gis) 				{ $ipad=$1; $helo=$2; 				}#print "X-$x-matched-19: ipad=$ipad, helo=$helo$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?\[?($IP)\]?:?\d*? \(HELO ($HELO)\)//gis) 			{ $ipad=$1; $helo=$2; 				}#print "X-$x-matched-20: ipad=$ipad, helo=$helo$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($HELO) \(IDENT:($LUSER)\@($RDNS) \[($IP)\]//gis) 		{ $helo=$1; $idnt=$2; $rdns=$3; $ipad=$4; 	}#print "X-$x-matched-21: helo=$helo, idnt=$idnt, rdns=$rdns, ipad=$ipad$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($HELO) \(<?($RDNS)>?\s?\[($IP)\]//gis) 			{ $helo=$1; $rdns=$2; $ipad=$3; 		}#print "X-$x-matched-22: helo=$helo, rdns=$rdns, ipad=$ipad$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($HELO) \(\[($IP)\] ident=($LUSER)\)//gis) 		{ $helo=$1; $ipad=$2; $idnt=$3; 		}#print "X-$x-matched-23: helo=$helo, ipad=$ipad, idnt=$idnt$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($HELO) \(proxying for ($IP)\) \(.*? user ($LUSER)\)//gis)	{ $helo=$1; $ipad=$2; $idnt=$3; 		}#print "X-$x-matched-24: helo=$helo, ipad=$ipad, idnt=$idnt$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($HELO) \(account ($LUSER) \[($IP)\] verified\)//gis) 	{ $helo=$1; $idnt=$2; $ipad=$3; 		}#print "X-$x-matched-25: helo=$helo, idnt=$idnt, ipad=$ipad$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?\(?($HELO) \(?\[?($IP)\]?\)?//gis) 			{ $helo=$1; $ipad=$2; 				}#print "X-$x-matched-26: helo=$helo, ipad=$ipad$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($HELO) \(localhost \[.*?:($IP)\]\)//gis) 			{ $helo=$1; $ipad=$2; 				}#print "X-$x-matched-27: helo=$helo, ipad=$ipad$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($HELO) \(($LUSER)\@($RDNS)\)//gis) 			{ $helo=$1; $idnt=$2; $rdns=$3; 		}#print "X-$x-matched-28: helo=$helo, idnt=$idnt, rdns=$rdns$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($HELO) \(($RDNS)\)//gis) 					{ $helo=$1; $rdns=$2; 				}#print "X-$x-matched-29: helo=$helo, rdns=$rdns$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/\(from\s+?($LUSER)\@($RDNS)\)//gis)					{ $idnt=$1; $rdns=$2; 				}#print "X-$x-matched-30: idnt=$idnt, rdns=$rdns$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/\(from\s+?($LUSER)\@($HELO)\)//gis)					{ $idnt=$1; $helo=$2; 				}#print "X-$x-matched-31: idnt=$idnt, helo=$helo$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?\(?\[?($IP)\]?\)?//gis) 					{ $ipad=$1; 					}#print "X-$x-matched-32: ipad=$ipad$CRLF"; }
		elsif ($rcvd->[$x]->{'string'} =~ s/^from\s+?($HELO)(?=\W|;|$)//gis) 					{ $helo=$1; 					}#print "X-$x-matched-33: helo=$helo$CRLF"; }

		# lookup IP if not provided
		$ipad = host($rdns) if !$ipad && $rdns && $options =~ /d/;
		$ipad = host($helo) if !$ipad && !$rdns && $helo && $helo =~ /$DOMAIN/ && $options =~ /d/;

		# exclude lines with no IP
		next if !$ipad && ((scalar @$rcvd) > 1);

		# save "from" info for comparison in next iteration
		$rcvd->[$x]->{'rdns'}	= $rdns;		
		$rcvd->[$x]->{'ipad'}	= $ipad;

		# exclude lines from local, private (RFC 1918), and invalid IP address ranges
		my $reserved = qr~^((?:127\.)|(?:10\.)|(?:172\.(?:1[6-9]|2[0-9]|31)\.)|(?:192\.168\.)|(?:169\.254\.))~;
		my $valid = qr~^((?:0?0?\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(?:0?0?\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(?:0?0?\d|[01]?\d\d|2[0-4]\d|25[0-5])\.(?:0?0?\d|[01]?\d\d|2[0-4]\d|25[0-5]))$~;
		next if ($rdns =~ /localhost/i || $ipad =~ /$reserved/ || $ipad !~ /$valid/) && ((scalar @$rcvd) > 1);
		
		# lookup MTA IP/rDNS if not provided
		$mtai = host($mtan) if !$mtai && $mtan && $options =~ /d/;
		$mtan = host($mtai) if !$mtan && $mtai && $options =~ /d/;

		# exclude lines from within our class B (/16) network
		next if (($edge_ip && $ipad && is_same_class_B($edge_ip,$ipad))||(!$edge_ip && $mtai && $ipad && is_same_class_B($mtai,$ipad))) && ((scalar @$rcvd) > 1);
		
		# perform reverse DNS lookup if not provided by MTA
		$rdns = host($ipad) if !$rdns && $ipad && $options =~ /d/;
		
		# force a reverse DNS lookup on all IPs, even those with an RDNS set by the MTA
		$rdns = host($ipad) if $ipad && $options =~ /f/;
		
		# perform ASN lookup (RFC 1930/2270)
		my $asn = asn($ipad) if $ipad && $options =~ /a/;

		# we implicitely trust the received line set "by" our own server as valid (first untrusted "from")
		if (!$edge_ip) { $edge_ip = $mtai; $rcvd->[$x]->{'sane'} = set_rcvd($helo,$ipad,$idnt,$rdns,$from,$mtan,$mtai,$mtav,$fore,$with,$date,$asn); }

		# now we'll try to establish the validity of each nonlocal received line by
		# checking for continuity and rejecting lines that don't fit the "from/by" chain
		else
		{
			#print " by " . $mtan . " / prev from " . $rcvd->[$x-1]->{'rdns'} . "$CRLF";
			#print " by " . $mtai . " / prev from " . $rcvd->[$x-1]->{'ipad'} . "$CRLF";
			if ((($mtan && $rcvd->[$x-1]->{'rdns'} && $mtan =~ /$rcvd->[$x-1]->{'rdns'}/) || 
			     ($mtai && $rcvd->[$x-1]->{'ipad'} && $mtai =~ /$rcvd->[$x-1]->{'ipad'}/)) && (!$untrusted)) 
			     { $rcvd->[$x]->{'sane'} = set_rcvd($helo,$ipad,$idnt,$rdns,$from,$mtan,$mtai,$mtav,$fore,$with,$date,$asn); }
			else { $rcvd->[$x]->{'sane'} = "untrusted"; $untrusted = 1; }
		}
	}
	
	return $rcvd;
}

sub is_same_class_B
{
	my ($ip1,$ip2) = @_;
	$ip1 =~ s/^(\d{1,3}\.\d{1,3}\.).*?$/$1/gis;
	$ip2 =~ s/^(\d{1,3}\.\d{1,3}\.).*?$/$1/gis;
	
	return ($ip1 eq $ip2)? 1:0;
}

sub asn
{
	my $target = shift;
	my $output = "";

	if ( $target =~ s/(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/$4.$3.$2.$1.$asn_server/ )
	{
		open (HOST, "host -t txt $target 2>/dev/null |") or error("warn", "Host lookup failed: $!");
		while (<HOST>) { $output = $1 if /\Q$target\E(?: descriptive)? text "(\d*?)".*/; }
		close HOST;
	} 

	return $output;
}

sub host
{
	my $target = shift;
	my $output = "";
	
	my $IP		= qr~(?:\d{1,3}\.){3}\d{1,3}~;	
	my $DOMAIN	= qr~[\w|-|\.]+\.\w{2,4}~;

	if ($target =~ s/($IP|$DOMAIN)/$1/)
	{
		open (HOST, "host $target 2>/dev/null |") or error("warn", "Host lookup failed: $!");
		while (<HOST>) { $output = $1 if /$DOMAIN (?:domain name pointer|has address) ($IP|$DOMAIN)\.?/; }
		close HOST;
	}
	
	return $output;
}

sub set_rcvd
{
	my ($helo,$ipad,$idnt,$rdns,$from,$mtan,$mtai,$mtav,$fore,$with,$date,$asn) = @_;

	my $output = "from";
	if ($options =~ /e/) {
	$output .= ($helo)? 		" helo-$helo" 	: "";} 		# sender's salutation
	$output .= ($rdns)? 		" $rdns" 	: "";		# sender's name
	$output .= ($ipad)? 		" $ipad" 	: "";		# sender's IP
	$output .= ($asn)?  		" as$asn" 	: "";		# sender's ASN
	$output .= ($mtan||$mtai)? 	" $CRLF\t  by"	: "";
	$output .= ($mtan)? 		" $mtan" 	: "";		# receiving MTA's name
	$output .= ($mtai)? 		" $mtai" 	: "";		# receiving MTA's IP
	$output .= ($fore)? 		" $CRLF\t  for" : "";
	$output .= ($fore)? 		" <$fore>" 	: "";		# envelope to address
	$output .= ($date)? 		"; $date" 	: "";		# received date/time
}

################################################
################ Output Header #################
################################################

sub set_header
{
	my $header = shift;
	my $output = "";
	
	# these are all of the fields specified in RFC 822/2822, case-insensitive, in the suggested order
	# the only *required* fields according to RFC 2822 are "from", "sender", "reply-to", and "date", others are just suggested
	my $spec_fields = "return-path,received,resent-date,resent-from,resent-sender,resent-reply-to,".
			  "resent-to,resent-cc,resent-bcc,resent-message-id,date,from,sender,reply-to,".
			  "to,cc,bcc,message-id,in-reply-to,references,subject,comments,keywords,encrypted";

	# MIME header fields (RFC 1049/1341/1521/2183)
	$spec_fields .=	  ",mime-version,content-type,content-transfer-encoding,content-id,content-description,content-disposition";

	# security/checksum (RFC 1864)
	$spec_fields .=   ",content-md5";

	# mailing list headers (RFC 2369/2919) may be added if you like, but for now I'm choosing to leave them out
	#$spec_fields .=   ",list-id,list-help,list-unsubscribe,list-subscribe,list-post,list-owner,list-archive";

	# let's exclude unnecessary fields (if you know of a valid, necessary use for these, let me know)
	my $masked_fields = "keywords,comments,encrypted,content-id,content-description";

	# controversial and not strictly necessary:
	$masked_fields .= ",reply-to";

	# message-id fields are only machine-readable and not visible to nor readable by the recipient
	# however, they can be useful if your client produces discussion threading
	# uncomment this line if you don't care about threading:
	# $masked_fields .= ",message-id,resent-message-id,in-reply-to,references";
	
	# resent fields are strictly informational (and not generally user-visible), therefore allowing them through is optional:
	# MIME specifies a different way of resending messages with the "Message" content-type, so these may be considered deprecated:
	$masked_fields .= ",resent-date,resent-from,resent-sender,resent-reply-to,resent-to,resent-cc,resent-bcc,resent-message-id";

	# see RFC 2076 / "Common Internet Message Header Fields" for a synopsis of common mail headers

	# exclude the "masked fields" from display
	foreach my $name (split(/,/,$masked_fields)) { $spec_fields =~ s/(?<=,)$name,?//; }

	# output the fields in the order specified by RFC 2822
	foreach my $name (split(/,/,$spec_fields)) { $output .= set_field($header,$name); delete $header->{$name}; }

	# set any user-specified fields
	foreach my $name (split(/,/,$user_fields)) { $output .= set_field($header,$name); delete $header->{$name}; }

	# then set any remaining fields (if allowed to set non-standard fields)
	if ($options !~ /s/) { foreach my $name (keys %{$header}) { $output .= set_field($header,$name); } }
	
	$output .= $CRLF;
	
	return $output;
}

sub set_field
{
	my $header = shift;
	my $name = shift;
	my $output = "";
	
	if ((defined $header->{$name}) && (ref($header->{$name}) eq "ARRAY"))
	{
		for (my $x = 0; $x < scalar @{$header->{$name}}; $x++)
		{
			if (($name eq "received") && ($options =~ /r/))
			{
				#if (defined $header->{$name}->[$x]->{'sane'}) {	$output .= ucfirst($name) . ": " . $header->{$name}->[$x]->{'sane'} . $CRLF; }
				if (defined $header->{$name}->[$x]->{'sane'}) {	$output .= $header->{$name}->[$x]->{'name'} . ": " . $header->{$name}->[$x]->{'sane'} . $CRLF; }
			}
			#else { $output .= ucfirst($name) . ": " . $header->{$name}->[$x]->{'string'} . $CRLF; }
			else { $output .= $header->{$name}->[$x]->{'name'} . ": " . $header->{$name}->[$x]->{'string'} . $CRLF; }
		}
	}
	
	return $output;
}

################################################
################ Error Handling ################
################################################

sub error
{
	my ($action,$msg) = @_;

	die $msg if $action eq "die";
	warn $msg unless $action eq "die";
	# add other actions if you like
}

sub sig_trap
{
	my $sig = shift;
	my ($action,$more) = ("warn","");

	sig: 
	{
		$action = "die",  last sig if $sig =~ /ALRM/;
		$action = "warn", last sig if $sig =~ /PIPE/;
		$action = "warn", last sig if $sig =~ /CHLD/;
		$action = "die" , last sig if $sig =~ /INT/;
		$action = "die" , last sig if $sig =~ /HUP/;
		$action = "warn";
	}
	
	my $waitedpid = wait;
	$more = "; Reaped pid $waitedpid, exited with status " . ($? >> 8) if $waitedpid;

	$SIG{$sig} = \&sig_trap;

	error ($action, "Trapped signal SIG$sig$more");
}

################################################
################################################
################################################
