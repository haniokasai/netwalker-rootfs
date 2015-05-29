# Orca
#
# Copyright 2004-2008 Sun Microsystems Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

__id__        = "$Id: script_settings.py 4507 2009-02-08 19:37:37Z wwalker $"
__version__   = "$Revision: 4507 $"
__date__      = "$Date: 2009-02-08 14:37:37 -0500 (Sun, 08 Feb 2009) $"
__copyright__ = "Copyright (c) 2004-2008 Sun Microsystems Inc."
__license__   = "LGPL"

# If True, it tells us to take over caret navigation.  This is something
# that can be set in user-settings.py:
#
# import orca.Gecko
# orca.Gecko.controlCaretNavigation = True
#
controlCaretNavigation = True

# If True, it tells us to position the caret at the beginning of a
# line when arrowing up and down.  If False, we'll try to position the
# caret directly above or below the current caret position.
#
arrowToLineBeginning = True

# If True, it tells Orca to automatically perform a SayAll operation
# when a page is first loaded.
#
sayAllOnLoad = True

# Whether or not to use the structrual navigation commands (e.g. H
# for heading, T for table, and so on).
#
structuralNavigationEnabled = True

# Whether or not Orca should speak the changing location within the
# document frame *during* a find (i.e. while focus is still in the
# Find toolbar).
#
speakResultsDuringFind = True

# The minimum number of characters that must be matched during
# a find before Orca speaks the changed location, assuming that
# speakResultsDuringFind is True.
#
minimumFindLength = 4

# Whether or not to continue speaking the same line if the match
# has not changed with additional keystrokes.  This setting comes
# in handy for fast typists who might inadvertantly interrupt the
# speaking of the line that matches by continuing to type in the
# Find entry.  This is the equivalent of what we do in autocompletes
# throughout GNOME.  For power-users of the Find toolbar, however,
# that may be too verbose so it's configurable.
#
onlySpeakChangedLinesDuringFind = False
