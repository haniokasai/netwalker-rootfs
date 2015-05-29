#!/usr/bin/perl

$command=$ARGV[0];
open(IN, "/bin/ps aunx |");
while (<IN>) {
    &search_totem($_);
}
close(IN);

sub search_totem {
    $line = @_[0];
    if ($line =~ /^ *(\d*).* totem\n/) {
	&exec_pause($1);
    } elsif ($line =~ /^ *(\d*).* totem /) {
	&exec_pause($1);
    }
}

sub exec_pause {
    $userId = @_[0];
    print "find totem(user:" . $userId . ")\n";
    $execommand = "sudo -u #" . $userId . " totem " . $command . " --display=:0";
    print($execommand . "\n");
    system($execommand);
    sleep 1
}
