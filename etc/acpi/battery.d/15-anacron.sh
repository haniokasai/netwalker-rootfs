#! /bin/sh

# This script makes anacron jobs stop to run when the machine is
# unplugged from AC power, or suspended.

/usr/sbin/invoke-rc.d anacron stop >/dev/null   
