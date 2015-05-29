#!/usr/bin/perl -w

use warnings;
use strict;

use Net::DBus;
use Net::DBus::Reactor;

use Carp qw(confess cluck);

#$SIG{__WARN__} = sub { cluck $_[0] };
#$SIG{__DIE__} = sub { confess $_[0] };

my $bus = Net::DBus->session();

my $service = $bus->get_service("org.designfu.TestService");
my $object  = $service->get_object("/org/designfu/TestService/object",
				   "org.designfu.TestService");

sub hello_signal_handler {
    my $greeting = shift;
    print "Received hello signal with greeting '$greeting'\n";
}

$object->connect_to_signal("HelloSignal", \&hello_signal_handler);

my $reactor = Net::DBus::Reactor->main();

my $ticks = 0;
$reactor->add_timeout(1000, Net::DBus::Callback->new(method => sub {
    $object->emitHelloSignal();
    if ($ticks++ == 10) {
      $reactor->shutdown();
    }
}));

$reactor->run();
