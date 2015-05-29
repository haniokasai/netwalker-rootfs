<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE methoddef SYSTEM "rpc-method.dtd">
<!--
    Generated automatically by make_method v1.12, Wed Nov  5 03:59:22 2008

    Any changes made here will be lost.
-->
<methoddef>
<name>system.status</name>
<version>1.2</version>
<signature>struct</signature>
<signature>struct boolean</signature>
<help>
Report on the various status markers of the server itself. The return value is
a STRUCT with the following members:

        Key         Type     Value

        host        STRING   Name of the (possibly virtual) host name to which
                             requests are sent.
        port        INT      TCP/IP port the server is listening on.
        name        STRING   The name of the server software, as it identifies
                             itself in transport headers.
        version     STRING   The software version. Note that this is defined as
                             a STRING, not a DOUBLE, to allow for non-numeric
                             values.
        path        STRING   URL path portion, for use when sending POST
                             request messages.
        date        ISO8601  The current date and time on the server, as an
                             ISO 8601 date string.
        date_int    INT      The current date as a UNIX time() value. This is
                             encoded as an INT rather than the dateTime.int
                             type, so that it is readable by older clients.
        started     ISO8601  The date and time when the current server started
                             accepting connections, as an ISO 8601 string.
        started_int
                    INT      The server start-time as a UNIX time() value. This
                             is also encoded as INT for the same reasons as
                             the "date_int" value above.
        total_requests
                    INT      Total number of requests served thus far
                             (including the current one). This will not include
                             requests for which there was no matching method,
                             or HTTP-HEAD requests.
        methods_known
                    INT      The number of different methods the server has
                             registered for serving requests.

If this method is called with a single boolean value, that value determines
whether the current call should be counted against the value of the
"total_requests" field. This is also handled at the server level. Setting
this boolean value to a "true" value causes the server (and the resulting
data structure returned) to not count this call. This feature allows external
tools (monitors, etc.) to check the status regularly without falsely running
up the value of "total_requests".
</help>
<code language="perl">
<![CDATA[
#!/usr/bin/perl
###############################################################################
#
#   Sub Name:       status
#
#   Description:    Create a status-reporting struct and returns it.
#
#   Arguments:      NAME      IN/OUT  TYPE      DESCRIPTION
#                   $srv      in      ref       Server object instance
#                   $no_inc   in      boolean   A true/false value that tells
#                                                 whether to count this call
#                                                 in the total_requests field.
#
#   Returns:        hashref
#
###############################################################################
sub status
{
    use strict;

    my $srv = shift;
    my $no_inc = shift || 0;

    my $status = {};
    my $time = time;
    my $URI;

    require URI;

    $status->{name} = ref($srv);
    $status->{version} = RPC::XML::string->new($srv->version);
    $status->{host} = $srv->host || $srv->{host} || '';
    $status->{port} = $srv->port || $srv->{port} || '';
    $status->{path} = RPC::XML::string->new($srv->path);
    $status->{date} = RPC::XML::datetime_iso8601
        ->new(RPC::XML::time2iso8601($time));
    $status->{started} = RPC::XML::datetime_iso8601
        ->new(RPC::XML::time2iso8601($srv->started));
    $status->{date_int} = $time;
    $status->{started_int} = $srv->started;
    $status->{total_requests} = $srv->requests();
    # In special cases where the call to system.status is not going to incr
    # the total, don't add the extra here, either...
    $status->{total_requests}++ unless $no_inc;
    $status->{methods_known} = scalar($srv->list_methods);

    $status;
}

__END__
]]></code>
</methoddef>
