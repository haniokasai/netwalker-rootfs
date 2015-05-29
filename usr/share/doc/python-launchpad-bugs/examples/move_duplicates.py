#!/usr/bin/python

cookie="/home/k/.bughelper/lpcookie.txt"

import launchpadbugs.connector as Connector
import sys

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--also-move-masterbugs", dest="move_masterbugs",
	help="Also move the previous masterbugs of the given bugs. "
		"Usually results in more bugs being touched.", action="store_true")
parser.add_option("-m", "--new_masterbug", dest="masterbug", type="int")
parser.set_usage("usage: %prog -m NEWMASTER [--also-move-masterbugs] bug1 bug2 ...")

(options, args) = parser.parse_args()
if len(args) == 0:
	parser.error("need bugs to process")
if not options.masterbug:
	parser.error("use -m for setting the new masterbug")


def mass_change_duplicates(bugs, handled_list, new_dup, level=0, and_their_masters=False):
	if level == 0:	# first check if the new masterbug is not a duplicate
			# otherwise we can't assign duplicates to it
		lp_masterbug = Bug(new_dup)
		lp_masterbug.duplicate_of = None
		lp_masterbug.commit()
		handled_list.add(new_dup)
	for b in bugs:
		if b in handled_list or b == new_dup:
			# either we processed this bug already or it is the new masterbug
			continue
		bug = Bug(b)
		old_dup = bug.duplicate_of
		if old_dup != new_dup:
			print "%sHandling bug %d: %s" % ("\t"*level, b, bug.title)
			handled_list.add(b) # don't process it again

			# now process all duplicates of this bug, minus already handled ones.
			found = bug.duplicates - handled_list
			if len(found) > 0:
				print "\t"*level, "-> Found:", ', '.join([ str(x) for x in found])
				mass_change_duplicates(found, handled_list, new_dup, level+1)

			print "\t"*level,"setting duplicate:", old_dup,"->", new_dup

			bug.duplicate_of = new_dup
			bug.commit()

			if and_their_masters and old_dup and old_dup not in handled_list:
				print "\t"*level, "-> Found:", old_dup
				mass_change_duplicates(set([old_dup]), handled_list, new_dup, level+1)

Bug = Connector.ConnectBug()
Bug.authentication=cookie

dup_list = set()
start_list = set([ int(x) for x in args ])

mass_change_duplicates(start_list, dup_list, options.masterbug, and_their_masters=options.move_masterbugs)
