# vim:cindent:ts=2:sw=2:et:fdm=marker:cms=\ #\ %s
#
# $Id: DB.pm 129 2008-04-07 18:36:39Z robert $
#

package Debian::DocBase::DB;

use strict;
use warnings;

use MLDBM qw(GDBM_File Storable);
use Fcntl;
use Carp;
use Debian::DocBase::Common;
use Debian::DocBase::Utils;
use Data::Dumper;

my $filesdb  = undef;
my $statusdb = undef;

sub new { # {{{
    my $class   = shift;
    my $dbfile  = shift;
    my $enckey  = shift;
    my $self    = {
        DB      => {},
        FILE    => $dbfile,
        ENCKEY  => $enckey

    };
    bless($self, $class);
    $self->_Init();
    return $self;
} # }}}

sub _Init() { # {{{
  my $self = shift;
  # read-only access for `install-docs --status or --dump-db' run as non-root user
  my $readonly = $> != 0;
  return if ($readonly && ! -f $self->{'FILE'}); # db not yet exists and can't be created
    
  my $flags = (!$readonly) ? (O_CREAT | O_RDWR) : O_RDONLY;

  tie %{$self->{'DB'}}, 'MLDBM', $self->{'FILE'}, $flags, 0644
    or croak "Can't access $self->{'FILE'}: $!\n";
} # }}}

sub PutData($$$) { # {{{
    my ($self, $key, $data)  = @_;
    $self->{'DB'}->{$self->EncodeKey($key)}   = $data;
} # }}}

sub GetData($$) { # {{{
  my ($self, $key) = @_;
  return $self->{'DB'}->{$self->EncodeKey($key)}
} # }}}

sub GetDB() { # {{{
  my $self = shift;
  return $self->{'DB'};
} # }}}

sub RemoveData($$) # {{{
{
  my ($self, $key) = @_;
  delete $self->{'DB'}->{$self->EncodeKey($key)};
} # }}}

sub Exists($) { # {{{
  my ($self, $key) = @_;
  my $data = $self->{'DB'}->{$self->EncodeKey($key)};
  return $data and %{$data};
} # }}}

sub DumpDB($) { # {{{
  my $self = shift;
  my $db   = $self->{'DB'};

  my $dumper = Data::Dumper->new([$db], [$self->{'FILE'}]);
  $dumper->Indent(1);
  $dumper->Terse(1);
  print "Contents of `" .$self->{'FILE'}."\':\n";
  print $dumper->Dump();
} # }}}

sub EncodeKey($$) { # {{{
  my ($self, $key) = @_;
  return $key unless $self->{'ENCKEY'};
  $key =~ s/\/+/\//go;
  $key =~ s/^~/~~/o;
  $key =~ s/^$CONTROL_DIR/~1/o;
  $key =~ s/^$LOCAL_CONTROL_DIR/~2/o;
  return $key;
} # }}}

sub DecodeKey($$) { # {{{ 
  my ($self, $key) = @_;
  return $key unless $self->{'ENCKEY'};

  $key =~ s/^~1/$CONTROL_DIR/o;
  $key =~ s/^~2/$LOCAL_CONTROL_DIR/o;
  $key =~ s/^~~/~/o;
  return $key;
} # }}}

### STATIC FUNCTIONS
sub GetFilesDB() { # {{{
  $filesdb     = Debian::DocBase::DB->new($DB_FILES, 1) unless $filesdb;
  return $filesdb;
} # }}}

sub GetStatusDB() { # {{{
  $statusdb     = Debian::DocBase::DB->new($DB_STATUS, 0) unless $statusdb;
  return $statusdb;
} # }}}

1
