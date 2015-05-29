#!/usr/bin/env python
#
# This script creates a list of bug numbers reported by lp-users listed
# in the ubuntu-bugcontrol-members.txt file, then a report is made of
# those bug numbers, statuses, importances and summaries
# TODO:
# Fix bugs being listed multiple times if they are targetted to a
# release - it happens with linux if not more

from launchpadbugs.connector import ConnectBug, ConnectBugList
from launchpadbugs.basebuglistfilter import URLBugListFilter
import sys

BugList = ConnectBugList("text")
Bug = ConnectBug("text")

package = sys.argv[1]

reporter_file = "ubuntu-bugcontrol-members.txt"

url = "https://bugs.launchpad.net/ubuntu/+source/%s/+bugs" % package

bug_numbers = [ ]

for line in open(reporter_file):
    team_member = line.strip('\n')

    bug_filter = URLBugListFilter()
    bug_filter.add_option("reporter", (team_member,))

    buglist = BugList(bug_filter(url))
    for item in buglist:
        bug_numbers.append(item.bugnumber)

bug_numbers.sort(reverse=True)

print "<html><body><table>"
for number in bug_numbers:
    bug = Bug('%s' % number)
    for task in bug.infotable:
	if task.affects.longname == package + ' (Ubuntu)': 
            # bug.reporter could be more the lp display name which might be more
            # informative
    	    print '<tr><td><a href="http://launchpad.net/bugs/%s">Bug %s</a></td><td>%s</td><td>%s, %s</td><td>%s</td></tr>' % (number, number, bug.reporter, task.status, task.importance, bug.summary)
print '</table></body></html>'
