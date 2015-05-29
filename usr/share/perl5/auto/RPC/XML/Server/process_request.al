# NOTE: Derived from blib/lib/RPC/XML/Server.pm.
# Changes made here will be lost when autosplit is run again.
# See AutoSplit.pm.
package RPC::XML::Server;

#line 1354 "blib/lib/RPC/XML/Server.pm (autosplit into blib/lib/auto/RPC/XML/Server/process_request.al)"
###############################################################################
#
#   Sub Name:       process_request
#
#   Description:    This is provided for the case when we run as a subclass
#                   of Net::Server.
#
#   Arguments:      NAME      IN/OUT  TYPE      DESCRIPTION
#                   $self     in      ref       This class object
#                   $conn     in      ref       If present, it's a connection
#                                                 object from HTTP::Daemon
#
#   Returns:        void
#
###############################################################################
sub process_request
{
    my $self = shift;
    my $conn = shift;

    my ($req, $reqxml, $resp, $respxml, $do_compress, $parser, $com_engine,
        $length, $read, $buf, $resp_fh, $tmpfile,
        $peeraddr, $peerhost, $peerport);

    my $me = ref($self) . '::process_request';
    unless ($conn and ref($conn))
    {
        $conn = $self->{server}->{client};
        bless $conn, 'HTTP::Daemon::ClientConn';
        ${*$conn}{'httpd_daemon'} = $self;

        if ($IO::Socket::SSL::VERSION and
            $RPC::XML::Server::IO_SOCKET_SSL_HACK_NEEDED)
        {
            no strict 'vars';
            unshift @HTTP::Daemon::ClientConn::ISA, 'IO::Socket::SSL';
            $RPC::XML::Server::IO_SOCKET_SSL_HACK_NEEDED = 0;
        }
    }

    # These will be attached to any and all request objects that are
    # (successfully) read from $conn.
    $peeraddr = $conn->peeraddr;
    $peerport = $conn->peerport;
    $peerhost = $conn->peerhost;
    while ($req = $conn->get_request('headers only'))
    {
        if ($req->method eq 'HEAD')
        {
            # The HEAD method will be answered with our return headers,
            # both as a means of self-identification and a verification
            # of live-status. All the headers were pre-set in the cached
            # HTTP::Response object. Also, we don't count this for stats.
            $conn->send_response($self->response);
        }
        elsif ($req->method eq 'POST')
        {
            # Get a XML::Parser::ExpatNB object
            $parser = $self->parser->parse();

            if (($req->content_encoding || '') =~ $self->compress_re)
            {
                unless ($self->compress)
                {
                    $conn->send_error(RC_BAD_REQUEST,
                                      "$me: Compression not permitted in " .
                                      'requests');
                    next;
                }

                $do_compress = 1;
            }

            if (($req->content_encoding || '') =~ /chunked/i)
            {
                # Technically speaking, we're not supposed to honor chunked
                # transfer-encoding...
            }
            else
            {
                $length = $req->content_length;
                if ($do_compress)
                {
                    # Spin up the compression engine
                    unless ($com_engine = Compress::Zlib::inflateInit())
                    {
                        $conn->send_error(RC_INTERNAL_SERVER_ERROR,
                                          "$me: Unable to initialize the " .
                                          'Compress::Zlib engine');
                        next;
                    }
                }

                $buf = '';
                while ($length > 0)
                {
                    if ($buf = $conn->read_buffer)
                    {
                        # Anything that get_request read, but didn't use, was
                        # left in the read buffer. The call to sysread() should
                        # NOT be made until we've emptied this source, first.
                        $read = length($buf);
                        $conn->read_buffer(''); # Clear it, now that it's read
                    }
                    else
                    {
                        $read = sysread($conn, $buf,
                                        ($length < 2048) ? $length : 2048);
                        unless ($read)
                        {
                            # Convert this print to a logging-hook call.
                            # Umm, when I have real logging hooks, I mean.
                            # The point is, odds are very good that $conn is
                            # dead to us now, and I don't want this package
                            # taking over SIGPIPE as well as the ones it
                            # already monopolizes.
                            #print STDERR "Error: Connection Dropped\n";
                            return undef;
                        }
                    }
                    $length -= $read;
                    if ($do_compress)
                    {
                        unless ($buf = $com_engine->inflate($buf))
                        {
                            $conn->send_error(RC_INTERNAL_SERVER_ERROR,
                                              "$me: Error inflating " .
                                              'compressed data');
                            # This error also means that even if Keep-Alive
                            # is set, we don't know how much of the stream
                            # is corrupted.
                            $conn->force_last_request;
                            next;
                        }
                    }

                    eval { $parser->parse_more($buf); };
                    if ($@)
                    {
                        $conn->send_error(RC_INTERNAL_SERVER_ERROR,
                                          "$me: Parse error in (compressed) " .
                                          "XML request (mid): $@");
                        # Again, the stream is likely corrupted
                        $conn->force_last_request;
                        next;
                    }
                }

                eval { $reqxml = $parser->parse_done(); };
                if ($@)
                {
                    $conn->send_error(RC_INTERNAL_SERVER_ERROR,
                                      "$me: Parse error in (compressed) " .
                                      "XML request (end): $@");
                    next;
                }
            }

            # Dispatch will always return a RPC::XML::response.
            # RT29351: If there was an error from RPC::XML::Parser (such as
            # a message that didn't conform to spec), then return it directly
            # as a fault, don't have dispatch() try and handle it.
            if (ref $reqxml)
            {
                # Set localized keys on $self, based on the connection info
                local $self->{peeraddr} = $peeraddr;
                local $self->{peerhost} = $peerhost;
                local $self->{peerport} = $peerport;
                $respxml = $self->dispatch($reqxml);
            }
            else
            {
                $respxml = RPC::XML::fault->new(RC_INTERNAL_SERVER_ERROR,
                                                $reqxml);
                $respxml = RPC::XML::response->new($respxml);
            }

            # Clone the pre-fab response and set headers
            $resp = $self->response->clone;
            # Should we apply compression to the outgoing response?
            $do_compress = 0; # In case it was set above for incoming data
            if ($self->compress and
                ($respxml->length > $self->compress_thresh) and
                (($req->header('Accept-Encoding') || '') =~
                 $self->compress_re))
            {
                $do_compress = 1;
                $resp->header(Content_Encoding => $self->compress);
            }
            # Next step, determine the response disposition. If it is above the
            # threshhold for a requested file cut-off, send it to a temp file
            if ($self->message_file_thresh and
                $self->message_file_thresh < $respxml->length)
            {
                require File::Spec;
                # Start by creating a temp-file
                $tmpfile = $self->message_temp_dir || File::Spec->tmpdir;
                $tmpfile = File::Spec->catfile($tmpfile,
                                               __PACKAGE__ . $$ . time);
                $tmpfile =~ s/::/-/g;
                unless (open($resp_fh, "+> $tmpfile"))
                {
                    $conn->send_error(RC_INTERNAL_SERVER_ERROR,
                                      "$me: Error opening $tmpfile: $!");
                    next;
                }
                unlink $tmpfile;
                # Make it auto-flush
                my $old_fh = select($resp_fh); $| = 1; select($old_fh);

                # Now that we have it, spool the response to it. This is a
                # little hairy, since we still have to allow for compression.
                # And though the response could theoretically be HUGE, in
                # order to compress we have to write it to a second temp-file
                # first, so that we can compress it into the primary handle.
                if ($do_compress)
                {
                    my $fh2;
                    $tmpfile .= '-2';
                    unless (open($fh2, "+> $tmpfile"))
                    {
                        $conn->send_error(RC_INTERNAL_SERVER_ERROR,
                                          "$me: Error opening $tmpfile: $!");
                        next;
                    }
                    unlink $tmpfile;
                    # Make it auto-flush
                    $old_fh = select($fh2); $| = 1; select($old_fh);

                    # Write the request to the second FH
                    $respxml->serialize($fh2);
                    seek($fh2, 0, 0);

                    # Spin up the compression engine
                    unless ($com_engine = Compress::Zlib::deflateInit())
                    {
                        $conn->send_error(RC_INTERNAL_SERVER_ERROR,
                                          "$me: Unable to initialize the " .
                                          'Compress::Zlib engine');
                        next;
                    }

                    # Spool from the second FH through the compression engine,
                    # into the intended FH.
                    $buf = '';
                    my $out;
                    while (read($fh2, $buf, 4096))
                    {
                        unless (defined($out = $com_engine->deflate(\$buf)))
                        {
                            $conn->send_error(RC_INTERNAL_SERVER_ERROR,
                                              "$me: Compression failure in " .
                                              'deflate()');
                            next;
                        }
                        print $resp_fh $out;
                    }
                    # Make sure we have all that's left
                    unless (defined($out = $com_engine->flush))
                    {
                        $conn->send_error(RC_INTERNAL_SERVER_ERROR,
                                          "$me: Compression flush failure in" .
                                          ' deflate()');
                        next;
                    }
                    print $resp_fh $out;

                    # Close the secondary FH. Rewinding the primary is done
                    # later.
                    close($fh2);
                }
                else
                {
                    $respxml->serialize($resp_fh);
                }
                seek($resp_fh, 0, 0);

                $resp->content_length(-s $resp_fh);
                $resp->content(sub {
                                   my $b = '';
                                   return undef unless
                                       defined(read($resp_fh, $b, 4096));
                                   $b;
                               });
            }
            else
            {
                # Treat the content strictly in-memory
                $buf = $respxml->as_string;
                $buf = Compress::Zlib::compress($buf) if $do_compress;
                $resp->content($buf);
                $resp->content_length($respxml->length);
            }

            $conn->send_response($resp);
            undef $resp;
        }
        else
        {
            $conn->send_error(RC_FORBIDDEN);
        }
    }

    return;
}

# end of RPC::XML::Server::process_request
1;
