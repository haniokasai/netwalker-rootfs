# vim:cindent:ts=2:sw=2:et:fdm=marker:cms=\ #\ %s
#
# $Id: Document.pm 154 2008-11-11 10:14:45Z robert $
#

package Debian::DocBase::Document;

use strict;
use warnings;

use Debian::DocBase::Common;
use Debian::DocBase::Utils;
use Debian::DocBase::DocBaseFile;
use Debian::DocBase::DB;
use Carp;
#use Scalar::Util qw(weaken);

our %DOCUMENTS = ();
my %section_map = ();

#################################################
###        PUBLIC STATIC FUNCTIONS            ###
#################################################

# return list of all proceseed documents
sub GetDocumentList() { # {{{
  return values %DOCUMENTS;
} # }}}

# check if $docid exists in status database
sub IsRegistered($) { # {{{
  my $docid = shift;
  return Debian::DocBase::DB::GetStatusDB()->Exists($docid);
} # }}}

# return all documents id from status database
sub GetAllRegisteredDocumentIDs() { # {{{
  my $db    = Debian::DocBase::DB::GetStatusDB()->GetDB();
  my @result = sort keys %$db;
  return @result;
} # }}}

sub new { # {{{
    my $class      = shift;
    my $documentId = shift;
    return $DOCUMENTS{$documentId} if defined  $DOCUMENTS{$documentId};

    my $self = {
        DOCUMENT_ID       => $documentId,
        MAIN_DATA         => {},
        FORMAT_LIST       => {},
        CONTROL_FILES     => {},
        STATUS_DICT       => {},
        MERGED_CTRL_FILES => 0,
        INVALID           => 1
    };
    bless($self, $class);
    $self->_ReadStatusDB($documentId);
    $DOCUMENTS{$documentId} = $self;
#  weaken $DOCUMENTS{$documentId};
    return $self;
} # }}}

#################################################
###            PUBLIC FUNCTIONS               ###
#################################################

sub DESTROY { # {{{
  my $self = shift;
  delete $DOCUMENTS{$self->GetDocumentID()};
} # }}}

sub GetDocumentID() { # {{{
  my $self = shift;
  return $self->{'DOCUMENT_ID'};
} # }}}

sub Invalid() { # {{{
  my $self = shift;
  return $self->{'INVALID'};
} # }}}


# getters for common fields
sub GetAbstract() { # {{{
  my $self = shift;
  return $self->_GetMainFld($FLD_ABSTRACT);
} # }}}

sub GetTitle() { # {{{
  my $self = shift;
  return $self->_GetMainFld($FLD_TITLE);
} # }}}

sub GetSection() { # {{{
  my $self = shift;
  return $self->_GetMainFld($FLD_SECTION);
} # }}}

sub GetAuthor() { # {{{
  my $self = shift;
  return $self->_GetMainFld($FLD_AUTHOR);
}   # }}}

# returns hash with format data (i.e. with FLD_FORMAT, $FLD_INDEX, $FLD_FILES keys)
# for $format_name
sub GetFormat($$) { # {{{
  my $self = shift;
  my $format_name = shift;
  return undef unless $self->_HasControlFiles();
  $self->_CheckMerged();
  return $self->{'FORMAT_LIST'}->{$format_name};
} # }}}

# returns status data for $key
sub GetStatus() { # {{{
  my $self = shift;
  my $key  = shift;
  return $self->{'STATUS_DICT'}->{$key};
}   # }}}

sub SetStatus($%) { # {{{
  my $self      = shift;
  my %status    = @_;

  my $changed = 0;

  foreach my $key (keys %status) {
    my $oldvalue = $self->{'STATUS_DICT'}->{$key};
    my $value   = $status{$key};

    if (defined $value) {
      $self->{'STATUS_DICT'}->{$key} = $value;
    } else {
       delete $self->{'STATUS_DICT'}->{$key};
    }

    $changed = 1 if ( (defined $value xor defined $oldvalue)
                   or (defined $value and $value ne $oldvalue) );
  }

  $changed ? $self->_WriteStatusDB()
           : Debug("Status of `" . join ("', `", keys %status) . "' in " .
                    $self->GetDocumentID() . " not changed");
}   # }}}

# displays informations about the document (called by `install-docs -s')
sub DisplayStatusInformation($) { # {{{
  my $self            = shift;
  my $docid           = $self->GetDocumentID();
  my $status_file     = "$DATA_DIR/$docid.status";
  my $var_ctrl_file   = "$VAR_CTRL_DIR/$docid";

  if (-f $var_ctrl_file) {
    if (open(F, '<', $var_ctrl_file)) {
      print "---document-information---\n";
      while (<F>) {
        next if /^Control-Files:/;
        s/^$/\n---format-description---/;
        print $_;
      }
      close(F);
    } else {
      Warn("Cannot open `$var_ctrl_file': $!");
    }
  }

  print "\n---status-information---\n";
  foreach my $cf (sort keys %{$self->{'CONTROL_FILES'}} ) {
    print "Control-File: $cf (changed: ". localtime ($self->{'CONTROL_FILES'}->{$cf}->GetLastChangeTime()) . ")\n";
  }

  foreach my $key (sort keys %{$self->{'STATUS_DICT'}} ) {
    print "$key: $self->{'STATUS_DICT'}->{$key}\n";
  }
} # }}}

sub Register($$) { # {{{
  my $self          = shift;
  my $db_file       = shift;
  my $db_filename   = $db_file->GetSourceFileName();

  Debug("Registering `$db_filename'");

  if ($db_file->GetDocumentID() ne $self->GetDocumentID()) {
    delete $self->{'CONTROL_FILES'}->{$db_filename};
    $db_file->OnRegistered(0);
    return Error("Document id in `$db_filename' does not match our document id (" .
                  $db_file->GetDocumentID() . ' != ' . $self->GetDocumentID() . ")");
  }

  if ($db_file->Invalid()) {
    delete $self->{'CONTROL_FILES'}->{$db_filename};
    $db_file->OnRegistered(0);
    return Warn($db_file->GetSourceFileName() . " contains errors, not registering");
  }

  $db_file->OnRegistered(1);
  $self->{'CONTROL_FILES'}->{$db_filename} = $db_file;
} # }}}

sub Unregister($$) { # {{{
  my $self          = shift;
  my $db_file       = shift;
  my $db_filename   = $db_file->GetSourceFileName();

  unless (exists $self->{'CONTROL_FILES'}->{$db_filename}) {
    # remove any file data from our existing files database if it's there
    Debian::DocBase::DB::GetFilesDB()->RemoveData($db_filename);
    return Warn( "File `" . $db_filename . "' is not registered, cannot remove");
  }

  $self->{'CONTROL_FILES'}->{$db_filename}->OnUnregistered();
  delete $self->{'CONTROL_FILES'}->{$db_filename};

} # }}}

sub UnregisterAll($) { # {{{
  my $self          = shift;

  Debug('Unregistering all control files from document `' . $self->GetDocumentID() . "'");

  foreach my $doc ( values %{$self->{'CONTROL_FILES'}} ) {
    $doc->OnUnregistered();
  }


  $self->{'CONTROL_FILES'} = {};
} # }}}

# generate and write new merged control file into /var/lib/doc-base/documents
sub WriteNewCtrlFile() { # {{{
  my $self     = shift;
  my $docid    = $self->GetDocumentID();
  my $tmpfile  = $VAR_CTRL_DIR . "/." . $docid . ".tmp";
  my $file     = $VAR_CTRL_DIR . "/" . $docid;
  my $fld      = undef;

  $self->_CheckMerged();

  if ($self->Invalid() || !$self->_HasControlFiles()) {
    if (-e $file)  {
      Debug("Removing control file $file");
      unlink $file or carp "Can't remove $file: $!";
    }
    return;
  }


  open(F, '>', $tmpfile) or
    carp ("Can't open $tmpfile for writing: $_");

  foreach $fld (GetFldKeys($FLDTYPE_MAIN)) {
    print F ucfirst($fld) . ": " .  $self->{'MAIN_DATA'}->{$fld} . "\n"
      if $self->{'MAIN_DATA'}->{$fld};
  }

  foreach my $format (sort keys %{$self->{'FORMAT_LIST'}}) {
    print F "\n";
    foreach $fld (GetFldKeys($FLDTYPE_FORMAT)) {
      print F ucfirst($fld) . ": " .  $self->{'FORMAT_LIST'}->{$format}->{$fld} . "\n"
        if $self->{'FORMAT_LIST'}->{$format}->{$fld};
    }
  }

  close F or carp "Can't close $file: $!";

  rename $tmpfile, $file or carp "Can't rename $tmpfile to $file: $!";
} # }}}

# merge contents of all available control files for the document
#  into $self->{'MAIN_DATA'} and $self->{'FORMAT_LIST'}
# Fields 'Document' and 'Section' must have the same value in all control files.
# Value of fields 'Author', 'Abstract', 'Title' is taken from the first control file
#  in which the value is not empty.
# Format sections are joined. It's an error if the same format is defined in more
#  than one control file.
sub MergeCtrlFiles($) { # {{{
  my $self    = shift;
  my $doc_id  = $self->GetDocumentID();

  $self->_ParseControlFiles();

  $self->{'INVALID'}           = 1;
  $self->{'MERGED_CTRL_FILES'} = 1;
  $self->{'MAIN_DATA'}         = {};
  $self->{'FORMAT_LIST'}       = {};

  foreach my $db_file_name ($self->_GetControlFileNames()) {
    my $doc_data  = $self->{'CONTROL_FILES'}->{$db_file_name};
    my $doc_fname = $doc_data->GetSourceFileName();

    if ($doc_data->GetDocumentID() ne $doc_id) {
      Warn("Document id in `" . $doc_fname ."' does not match our document id (" .
                  $doc_data->GetDocumentID()  . ' != ' . $self->GetDocumentID() . ")");
      $self->Unregister($doc_data);
      next;
    }

    # merge main sections' fields
    foreach my $fld (GetFldKeys($FLDTYPE_MAIN)) {
      my $old_val = $self->{'MAIN_DATA'}->{$fld};
      my $new_val = $doc_data->GetFldValue($fld);
      if ($new_val) {
        $new_val = $self->_MangleSection($new_val) if $fld eq $FLD_SECTION;

        if ($old_val and $old_val ne $new_val and
            ($fld eq $FLD_DOCUMENT or $fld eq $FLD_SECTION)) {
            return Error("Error while merging $doc_id with $doc_fname: inconsistent values of $fld");
        }
        $self->{'MAIN_DATA'}->{$fld} = $new_val unless $old_val;
      }
    }

    # merge formats
    foreach my $format ($doc_data->GetFormatNames()) {
      return Error("Error while merging $doc_id with $doc_fname: format $format already defined") if $self->{'FORMAT_LIST'}->{$format};
      $self->{'FORMAT_LIST'}->{$format} = $doc_data->GetFormat($format);
    }
  }
  return unless  %{$self->{'FORMAT_LIST'}};
  $self->{'INVALID'}           = 0;
} # }}}


# Save status changes, calls _WriteStatusDB()
sub SaveStatusChanges($) { # {{{
  my $self = shift;

  $self->_WriteStatusDB();
} # }}}

#################################################
###            PRIVATE FUNCTIONS              ###
#################################################

# dies with Internal error if document hasn't been merged yet
sub _CheckMerged($) { # {{{
  my $self = shift;

  croak "Internal error: Document " . $self->GetDocumentID(). " not yet merged"
    unless $self->{'MERGED_CTRL_FILES'};
} # }}}

# returns $fld from $self->{'MAIN_DATA'}
sub _GetMainFld($$) { # {{{
  my $self = shift;
  my $fld  = shift;

  $self->_CheckMerged();

  return "" if $self->Invalid();

  return "" unless $self->{'MAIN_DATA'}->{$fld};

  return $self->{'MAIN_DATA'}->{$fld};
} # }}}

sub _HasControlFiles() { # {{{
  my $self = shift;
  return $self->{'CONTROL_FILES'}
} # }}}

# reads our status file and sets $self->{'STATUS_DICT'} and sets keys of
# $self->{'CONTROL_FILES'}
sub _ReadStatusDB { # {{{
  my $self        = shift;
  my $docid       = $self->GetDocumentID();
  my $data        = Debian::DocBase::DB::GetStatusDB()->GetData($docid);

  if ($data) {
    my %cf = map { $_ => Debian::DocBase::DocBaseFile->new($_) } keys %{$data->{'CF'}};
    $self->{'CONTROL_FILES'}  = \%cf;
    $self->{'STATUS_DICT'}    = $data->{'SD'};
  } else {
    $self->{'CONTROL_FILES'} = {};
    $self->{'STATUS_DICT'}   = {};
  };
  $self->{'INVALID'} = 0;

} # }}}

# writes our status file
sub _WriteStatusDB { # {{{
  my $self  = shift;
  my $docid = $self->GetDocumentID();

  if (%{$self->{'CONTROL_FILES'}} or %{$self->{'STATUS_DICT'}}) {
    my %cf = map { $_ => undef }  keys %{$self->{'CONTROL_FILES'}};

    my $data = { 'CF' => \%cf,
                 'SD' => $self->{'STATUS_DICT'}
               };
   Debian::DocBase::DB::GetStatusDB()->PutData($docid, $data);
  } else {
   Debian::DocBase::DB::GetStatusDB()->RemoveData($docid);
  }
} # }}}

# if called without any argument, returns array of control files' names
# if called with an argument returns string containing names of the control files
#  joined with value of the argument
sub _GetControlFileNames($;$) { # {{{
  my $self      = shift;
  my $join_str  = shift;

  my @cfnames = sort keys %{$self->{'CONTROL_FILES'}};

  return @cfnames unless ($join_str);
  return join($join_str, @cfnames);
} # }}}

# reads and parses all control files mentioned in $self->{'CONTROL_FILES'}
sub _ParseControlFiles($) { # {{{
  my $self = shift;

  foreach my $cfname ($self->_GetControlFileNames()) {
    croak "Internal error: $cfname not created\n" unless $self->{'CONTROL_FILES'}->{$cfname};
    $self->{'CONTROL_FILES'}->{$cfname}->Parse();
  }
} # }}}

sub _MangleSection($) { # {{{
  my $self      = shift;
  my $section   = shift;

  ReadMap($DOCBASE_SECTIONS_MAP, \%section_map) unless %section_map;

  $section  = lc $section;
  $section  =~ s/\s+/ /g;       $section  =~ s/\/+/\//g;
  $section  =~ s/[\/\s]$//g;    $section  =~ s/^[\/\s]//g;
  $section  =~ s/\b./\U$&\E/g;

  my @sect_comps = split (/\/+/, $section);
  my $result     = "";

  while ($#sect_comps > -1) {
    my $tmp   =  shift(@sect_comps);
    $result   =  ($result) ? $result . "/" .  $tmp : $tmp;

    $tmp      = lc $result;
    $result   = $section_map{$tmp} if exists $section_map{$tmp};
  }

  return $result if $result;
  return "Unknown";
} # }}}

1;