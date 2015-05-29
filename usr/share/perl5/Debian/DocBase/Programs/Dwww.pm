# vim:cindent:ts=2:sw=2:et:fdm=marker:cms=\ #\ %s
#
# $Id: Dwww.pm 143 2008-04-27 08:07:20Z robert $
#

package Debian::DocBase::Programs::Dwww;

use Exporter();
use strict;
use warnings;

use vars qw(@ISA @EXPORT);
@ISA = qw(Exporter);
@EXPORT = qw(RegisterDwww);

use Debian::DocBase::Common;
use Debian::DocBase::Utils;

our $dwww_build_menu = "/usr/sbin/dwww-build-menu";

# Registering to dwww:
sub RegisterDwww($@) { # {{{
  my $showinfo = shift;
  my @documents = @_;

  Debug("RegisterDwww started");

  if (-x $dwww_build_menu) {
    Inform("Registering documents with dwww...") if $showinfo and $opt_update_menus;
    Execute($dwww_build_menu) if $opt_update_menus;
  } else {
    Debug("Skipping execution of $dwww_build_menu - dwww package doesn't seem to be installed");
  }
  Debug("RegisterDwww finished");

} # }}}
