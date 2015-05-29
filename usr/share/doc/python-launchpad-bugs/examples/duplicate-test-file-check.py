#!/usr/bin/env python
#
# This script will check a bug report's duplicates for attachments
# and print the name of the attachment and the bug that the 
# attachment is attached to.  It's useful for finding files for
# testing apport crash reports.
#
# Copyright 2008 Canonical, Ltd
# Author: Brian Murray <brian@canonical.com>
# Licensed under the GNU General Public License, version 3.

from launchpadbugs.connector import ConnectBug
import sys
import os

Bug = ConnectBug('text')
Bug.authentication= os.path.expanduser('~/.lpcookie.txt')

# don't list the following attachments
apport_attachments = [ 'Dependencies.txt', 'Disassembly.txt', 'ProcMaps.txt', 'ProcStatus.txt', 'Registers.txt', 'Stacktrace.txt', 'ThreadStacktrace.txt', 'CoreDump.gz', 'Traceback.txt' ]

def getattachments(number):
    bug = Bug(number)

    for dup in bug.duplicates:
        getattachments(dup)
    
    if bug.attachments:
        for attachment in bug.attachments:
            if attachment.lp_filename not in apport_attachments:
                print 'http://launchpad.net/bugs/%s: %s' % (bug.bugnumber, attachment.lp_filename)

master_bug = sys.argv[1]
            
getattachments(master_bug)
