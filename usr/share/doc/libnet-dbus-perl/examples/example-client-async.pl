#/usr/bin/perl

use warnings;
use strict;

use Net::DBus;
use Net::DBus::Reactor;
use Net::DBus::Callback;
use Net::DBus::Annotation qw(:call);

my $bus = Net::DBus->session();

my $service = $bus->get_service("org.designfu.SampleService");
my $object = $service->get_object("/SomeObject");

print "Doing async call\n";
my $reply = $object->HelloWorld(dbus_call_async, "Hello from example-client.pl!");

my $r = Net::DBus::Reactor->main;

sub all_done {
    my $reply = shift;
    my $list = $reply->get_result;
    print "[", join(", ", map { "'$_'" } @{$list}), "]\n";

    $r->shutdown;
}

print "Setting notify\n";
$reply->set_notify(\&all_done);

sub tick {
    print "Tick-tock\n";
}


print "Adding timer\n";
$r->add_timeout(500, Net::DBus::Callback->new(method => \&tick));

print "Entering main loop\n";
$r->run;
