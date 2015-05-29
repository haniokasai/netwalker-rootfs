# NOTE: Derived from blib/lib/RPC/XML/Procedure.pm.
# Changes made here will be lost when autosplit is run again.
# See AutoSplit.pm.
package RPC::XML::Procedure;

#line 758 "blib/lib/RPC/XML/Procedure.pm (autosplit into blib/lib/auto/RPC/XML/Procedure/reload.al)"
###############################################################################
#
#   Sub Name:       reload
#
#   Description:    Reload the method's code and ancillary data from the file
#
#   Arguments:      NAME      IN/OUT  TYPE      DESCRIPTION
#                   $self     in      ref       Object of this class
#
#   Returns:        Success:    $self
#                   Failure:    error message
#
###############################################################################
sub reload
{
    my $self = shift;

    return ref($self) . '::reload: No file associated with method ' .
        $self->{name} unless $self->{file};
    my $tmp = $self->load_XPL_file($self->{file});

    if (ref $tmp)
    {
        # Update the information on this actual object
        $self->{$_} = $tmp->{$_} for (keys %$tmp);
        # Re-calculate the signature table, in case that changed as well
        return $self->make_sig_table;
    }

    return $tmp;
}

# end of RPC::XML::Procedure::reload
1;
