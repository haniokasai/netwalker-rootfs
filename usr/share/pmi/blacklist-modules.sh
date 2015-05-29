#!/bin/bash

# Walk a directory, assembling a list of modules that need to be blacklisted
# Then check which modules are loaded, and return those as a string

. /etc/default/pmi

if [ ! -d $BLACKLISTDIR ]; then
        echo "No such directory $BLACKLISTDIR, exiting" >&2
        exit 1
fi

for file in $(find $BLACKLISTDIR -type f -print "%p "); do
        MODSLIST="$MODSLIST "$(<$file);
done

MODSLOADED=$(lsmod|awk '!/Module/ {print $1}')

for mod in $MODSLIST; do
        if echo $MODSLOADED|grep -q -w "$mod"; then
                BLACKLIST="$BLACKLIST $mod"
        fi
done

echo $BLACKLIST
