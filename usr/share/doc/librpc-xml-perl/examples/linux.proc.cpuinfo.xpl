<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE proceduredef SYSTEM "rpc-method.dtd">
<!--
    Generated automatically by make_method v1.12, Wed Nov  5 03:59:32 2008

    Any changes made here will be lost.
-->
<proceduredef>
<name>linux.proc.cpuinfo</name>
<version>1.0</version>
<signature>struct</signature>
<help>
Read the system's "/proc/cpuinfo" special file and return the information in
the form of a STRUCT with the members based on the lines returned from the
"file". All values are either INT or STRING, based on the disposition of the
data itself. The exception to this is the key "flags", which is an ARRAY of
STRING.
</help>
<code language="perl">
<![CDATA[
#!/usr/bin/perl
###############################################################################
#
#   Sub Name:       linux_proc_cpuinfo
#
#   Description:    Read the /proc/cpuinfo on a Linux server and return a
#                   STRUCT with the information.
#
#   Arguments:      None.
#
#   Returns:        hashref
#
###############################################################################
sub linux_proc_sysinfo
{
    use strict;

    my (%cpuinfo, $line, $key, $value);
    local *F;

    open(F, '/proc/cpuinfo') or
        return RPC::XML::fault->new(501, "Cannot open /proc/cpuinfo: $!");

    while (defined($line = <F>))
    {
        chomp $line;
        next if ($line =~ /^\s*$/);

        ($key, $value) = split(/\s+:\s+/, $line, 2);
        $key =~ s/ /_/g;
        $cpuinfo{$key} = ($key eq 'flags') ? [ split(/ /, $value) ] : $value;
    }
    close(F);

    \%cpuinfo;
}

__END__
]]></code>
</proceduredef>
