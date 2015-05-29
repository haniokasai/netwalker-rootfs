<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE proceduredef SYSTEM "rpc-method.dtd">
<!--
    Generated automatically by make_method v1.12, Wed Nov  5 03:59:32 2008

    Any changes made here will be lost.
-->
<proceduredef>
<name>linux.proc.meminfo</name>
<version>1.0</version>
<signature>struct</signature>
<help>
Read the system's "/proc/meminfo" special file and return the information in
the form of a STRUCT with the following members:

        Key         Type     Value

        mem_total   INT      Total memory available, in bytes
        mem_used    INT      Total memory currently used, in bytes
        mem_free    INT      Memory remaining, in bytes
        mem_shared  INT      Memory being shared between processes, in bytes
        mem_buffers INT      Number of memory buffers
        mem_cached  INT      Cached memory
        MemTotal    STRING   Total memory, in kB
        MemFree     STRING   Free memory, in kB
        MemShared   STRING   Shared memort, in kB
        Buffers     STRING   Memory buffers, in kB
        Cached      STRING   Cached memory, in kB
        SwapTotal   STRING   Total swap memory, in kB
        SwapFree    STRING   Available swap memory, in kB
</help>
<code language="perl">
<![CDATA[
#!/usr/bin/perl
###############################################################################
#
#   Sub Name:       linux_proc_meminfo
#
#   Description:    Read the /proc/meminfo on a Linux server and return a
#                   STRUCT with the information.
#
#   Arguments:      None.
#
#   Returns:        hashref
#
###############################################################################
sub linux_proc_meminfo
{
    use strict;

    my (%meminfo, $line, $key, @parts);
    local *F;

    open(F, '/proc/meminfo') or
        return RPC::XML::fault->new(501, "Cannot open /proc/meminfo: $!");

    while (defined($line = <F>))
    {
        next if ($line =~ /^\s+/);
        chomp $line;

        @parts = split(/\s+/, $line);
        $key = shift(@parts);
        if ($key eq 'Mem:')
        {
            @meminfo{qw(mem_total mem_used mem_free mem_shared mem_buffers
                        mem_cached)} = @parts;
        }
        elsif ($key eq 'Swap:')
        {
            @meminfo{qw(swap_total swap_used swap_free)} = @parts;
        }
        else
        {
            chop $key; # Lose the trailing ':'
            $meminfo{$key} = join(' ', @parts);
        }
    }
    close(F);

    \%meminfo;
}

__END__
]]></code>
</proceduredef>
