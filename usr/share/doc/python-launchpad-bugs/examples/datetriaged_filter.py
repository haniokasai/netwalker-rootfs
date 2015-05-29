#!/usr/bin/env python
#
# This script will find package, argv[1], bugs that have been triaged
# since the date specified, argv[2], by reviewing the date-triaged
# field for a bug task.

from launchpadbugs.connector import ConnectBug, ConnectBugList
from launchpadbugs.basebuglistfilter import URLBugListFilter
from launchpadbugs.lptime import LPTime
import sys

BugList = ConnectBugList("text")
Bug = ConnectBug("text")

package = sys.argv[1]
since = sys.argv[2]

url = "https://bugs.launchpad.net/ubuntu/+source/%s/+bugs" % package

bug_filter = URLBugListFilter()

bug_filter.add_option("status", ("Triaged"))

l = BugList(bug_filter(url))

# convert elements into Bug objects
l = map(Bug, l)

date = LPTime(since)
def filter_datetriaged(bug):
    # check if there is a package task which was confirmed after 'date'
    for task in bug.infotable:
        if task.affects.longname == package + ' (Ubuntu)':
            d = task.date_triaged
            if d is None:
                continue
            if d > date:
                return bug
            return False
        return False
    
for bug in filter(filter_datetriaged, l):
    print 'http://launchpad.net/bugs/%s' % bug.bugnumber
