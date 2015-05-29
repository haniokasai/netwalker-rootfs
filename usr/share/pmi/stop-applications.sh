#!/bin/bash

# Walk a directory, assembling a list of services that need to be stopped
# Returns a string

. /etc/default/pmi

if [ ! -d $STOPDIR ]; then
        echo "No such directory $STOPTDIR, exiting" >&2
        exit 1
fi

for file in $(find $STOPDIR -type f -print "%p "); do
        STOPLIST="$STOPLIST "$(<$file);
done

echo $STOPLIST
