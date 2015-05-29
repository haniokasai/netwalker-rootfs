#!/usr/bin/perl

# vim:cindent:ts=2:sw=2:et:fdm=marker:cms=\ #\ %s
#
# $Id: InstallDocs.pm 147 2008-05-13 19:42:14Z robert $

package Debian::DocBase::InstallDocs;

use warnings;
use strict;

use base qw(Exporter);
use vars qw(@EXPORT);
our @EXPORT = qw(SetMode InstallDocsMain
                 $MODE_INSTALL $MODE_REMOVE $MODE_STATUS $MODE_REMOVE_ALL $MODE_INSTALL_ALL
                 $MODE_INSTALL_CHANGED $MODE_DUMP_DB $MODE_CHECK  $verbose $debug);

use Carp;
use Debian::DocBase::Common;
use Debian::DocBase::Utils;
use Debian::DocBase::Document;
use Debian::DocBase::DocBaseFile;
use Debian::DocBase::DB;
use Debian::DocBase::Programs::Dhelp;
use Debian::DocBase::Programs::Dwww;
use Debian::DocBase::Programs::Scrollkeeper;
use File::Path;


# constants
our $MODE_INSTALL         = 1;
our $MODE_REMOVE          = 2;
our $MODE_INSTALL_ALL     = 3;
our $MODE_REMOVE_ALL      = 4;
our $MODE_STATUS          = 5;
our $MODE_CHECK           = 6;
our $MODE_INSTALL_CHANGED = 7;
our $MODE_DUMP_DB         = 8;

# global module variables
our $mode                 = undef;
our @arguments            = undef;

#################################################
###        PUBLIC STATIC FUNCTIONS            ###
#################################################

# Sets work mode
sub SetMode($@) { # {{{
  my $newmode = shift;
  my @args    = @_;


  croak("Internal error: mode already set: $mode, $newmode") if (defined $mode);

  $mode = $newmode;

  Inform("Value of --rootdir option ignored") if ($mode != $MODE_CHECK) and ($opt_rootdir ne "");

  if ($#args == 0 and $args[0] eq '-') {
    # get list from stdin
    @arguments = map {+chomp} <STDIN>;
  }
  else {
    @arguments = @args;
  }

} # }}}

# Main procedure that gets called by install-docs
sub InstallDocsMain() { # {{{

  croak("Internal error: Unknown mode") unless defined $mode;

  if ($mode == $MODE_CHECK) {
    _HandleCheck();
  } elsif ($mode == $MODE_STATUS) {
    _HandleStatus();
  } elsif ($mode == $MODE_DUMP_DB) {
    _HandleDumpDB();
  } elsif ($mode == $MODE_REMOVE_ALL) {
    _HandleRemovalOfAllDocs();
  } else {
    _HandleRegistrationAndUnregistation();
  }

  # don't fail on reregistering docs
  $exitval = 0 if    $mode == $MODE_INSTALL_ALL
                  or $mode == $MODE_REMOVE_ALL
                  or $mode == $MODE_INSTALL_CHANGED;

} # }}}

#################################################
###        PRIVATE STATIC FUNCTIONS           ###
#################################################

# Check correctness of doc-base file
sub _HandleCheck() { # {{{
  foreach my $file (@arguments) {
    if (! -f $file) {
      Error("Can't read doc-base file `$file'");
      next;
    }

    my $docfile = Debian::DocBase::DocBaseFile->new($file, 1);
    $docfile->Parse();
    if ($docfile->Invalid()) {
        Inform("$file: Fatal error found, the file won't be registered");
    } elsif ((my $cnt = $docfile->GetWarnErrCount()) > 0) {
        Inform("$file: $cnt warning(s) or non-fatal error(s) found");
    } else {
        Inform("$file: No problems found");
    }
  }
} # }}}

# Show document status
sub _HandleStatus() { # {{{
  foreach my $docid (@arguments) {
    unless (Debian::DocBase::Document::IsRegistered($docid)) {
      Inform ("Document `$docid' is not registered");
      next;
    }
    my $doc = Debian::DocBase::Document->new($docid);
    $doc -> DisplayStatusInformation();
  }
} # }}}

# Dump our databases
sub _HandleDumpDB() { # {{{
  foreach my $arg (@arguments) {
    if ($arg eq "files.db") {
      Debian::DocBase::DB::GetFilesDB()->DumpDB();
    } elsif ($arg eq "status.db") {
      Debian::DocBase::DB::GetStatusDB()->DumpDB();
    } else {
      Error("Invalid argument `$arg' passed to --dump-db option");
      exit (1);
    }
  }
} # }}}

# Remove all docs simply by deleting our db and other created files
sub _HandleRemovalOfAllDocs() { # {{{
  my $suffix  = ".removed.$$";
  my @dbdirs  = ($OMF_DIR, $VAR_CTRL_DIR);

  unlink $DB_FILES or croak("Can't remove $DB_FILES: $!") if -f $DB_FILES;
  foreach my $d (@dbdirs) {
    next unless -d $d;
    rename ($d, $d.$suffix) or croak("Can't rename $d to ${d}${suffix}: $!");
    mkpath ($d, 0, 0755);
    rmtree ($d.$suffix, 0, 0);
  }
  unlink $DB_STATUS or croak("Can't remove $DB_STATUS: $!") if -f $DB_STATUS;

  my @documents = ();
  RegisterDwww(1, @documents);
  RegisterDhelp(1, 1, @documents);
  RegisterScrollkeeper(1, @documents);

} # }}}

# Register or de-register particular docs or register all or only changed docs
sub _HandleRegistrationAndUnregistation() { # {{{
  my @toinstall     = ();       # list of files to install
  my @toremove      = ();       # list of files to remove
  my @toremovedocs  = ();       # list of docs to remove
  my $msg           = "";

  if ($mode == $MODE_INSTALL_CHANGED) {
    my @stats = Debian::DocBase::DocBaseFile::GetChangedDocBaseFiles(\@toremove, \@toinstall);

    my $i      = 0;
    $msg      .= ($i++ ? ""   : "") . $stats[0] .  " removed" if $stats[0];
    $msg      .= ($i++ ? ", " : "") . $stats[1] .  " changed" if $stats[1];
    $msg      .= ($i++ ? ", " : "") . $stats[2] .  " added"   if $stats[2];
    Inform("Processing $msg doc-base file(s)...") if $msg;
  }

  elsif ($mode == $MODE_INSTALL_ALL) {
    @toremovedocs  = Debian::DocBase::Document::GetAllRegisteredDocumentIDs();
    @toinstall     = Debian::DocBase::DocBaseFile::GetAllDocBaseFiles() if $mode == $MODE_INSTALL_ALL;
    my @stats      = ($#toremovedocs+1, $#toinstall+1);
    my $i          = 0;
    $msg          .=  ($i++ ? "" : "")  .  "De-registering "       . $stats[0] if $stats[0];
    $msg          .=  ($i++ ? ", re-registering "  : "Registering ") . $stats[1] if $stats[1];
    Inform("$msg doc-base file(s)...") if $msg;
  }

  elsif  ($mode == $MODE_INSTALL) {
    @toinstall = @arguments;
  }

  elsif ($mode == $MODE_REMOVE)  {
    @toremove     = grep { /\//  } @arguments;
    @toremovedocs = grep { /^[^\/]+$/ } @arguments; # for backward compatibility  -> arguments are document-ids

  }

  foreach my $docid (@toremovedocs) {
    unless (Debian::DocBase::Document::IsRegistered($docid)) {
      Inform ("Ignoring nonregistered document `$docid'");
      next;
    }
    Debug("Trying to remove document $docid");
    my $doc   = Debian::DocBase::Document->new($docid);
    $doc->UnregisterAll();
  }

  foreach my $file (@toremove) {
    my $docid   = Debian::DocBase::DocBaseFile::GetDocIdFromRegisteredFile($file);
    unless ($docid) {
      Inform ("Ignoring nonregistered file `$file'");
      next;
    }
    my $docfile = Debian::DocBase::DocBaseFile->new($file);
    my $doc     = Debian::DocBase::Document->new($docid);
    $doc->Unregister($docfile);
  }

  foreach my $file (@toinstall) {
    unless (-f $file) {
      Error("Can't read doc-base file `$file'");
      next;
    }
    Debug("Trying to install file $file");
    my $docfile = Debian::DocBase::DocBaseFile->new($file,  $opt_verbose);
    $docfile->Parse();
    my $docid   = $docfile->GetDocumentID();
    next unless defined $docid;
    my $doc     = Debian::DocBase::Document->new($docid);

    $doc->Register($docfile);
  }

  my @documents = Debian::DocBase::Document::GetDocumentList();

  UnregisterDhelp(@documents) if @documents and $mode != $MODE_INSTALL_ALL;

  foreach my $doc (@documents) {
      $doc -> MergeCtrlFiles();
  }

  IgnoreSignals();
  foreach my $doc (@documents) {
    $doc -> WriteNewCtrlFile();
    $doc -> SaveStatusChanges();
  }
  RestoreSignals();

  if (@documents)
  {
    my $showmsg = ($opt_verbose or $msg);

    RegisterDwww($showmsg,          @documents);
    RegisterDhelp($showmsg,         $mode == $MODE_INSTALL_ALL, @documents);
    RegisterScrollkeeper($showmsg,  @documents);
  }

  undef @toinstall;
  undef @toremove;
  undef @toremovedocs;

} # }}}

1;
