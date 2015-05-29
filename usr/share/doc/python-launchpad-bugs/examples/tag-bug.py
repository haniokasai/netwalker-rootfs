#!/usr/bin/env python
#
# This script reads a list of bugs from a file and removes an existing bug
# tag and adds a new bug tag.  You should be able to easily modify the script
# to only add new tags or remove existing ones.
#
import os
import sys
import launchpadbugs.connector as Connector
import launchpadbugs.html_bug
import glob

cookie = os.path.expanduser('~/.lp_cookie')
try:
    if not os.path.exists(cookie):
        for name in glob.glob(os.path.expanduser('~/.mozilla/*/*/cookies.sqlite')):
            for line in file(name).readlines():
                if line.startswith('.launchpad.net\t') and '\tlp\t' in line:
                    print "%s not found, symlinking to %s" % (cookie,name)
                    os.symlink(name,cookie)
                    raise
except:
    pass

Bug = Connector.ConnectBug()
Bug.authentication = cookie

tag_old = 'cow'
tag_new = 'moo'
filename = './tag-bug.txt'
content = open(filename, 'r')
#url = 'https://bugs.launchpad.net/ubuntu/+bugs-text?field.tag=%s' % (tag_old)
#content = urllib.urlopen(url)
for i in content:
    num = i.rstrip('\n')
    print num
    bug = Bug(num)
    if tag_old in bug.tags:
        bug.tags.remove(tag_old)
    bug.tags.append(tag_new)
    bug.commit(force_changes=True, ignore_lp_errors=False)
content.close()
