# Orca
#
# Copyright 2005-2008 Sun Microsystems Inc.
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

"""Custom script for Evolution."""

__id__        = "$Id: speech_generator.py 4221 2008-09-15 08:11:23Z wwalker $"
__version__   = "$Revision: 4221 $"
__date__      = "$Date: 2008-09-15 04:11:23 -0400 (Mon, 15 Sep 2008) $"
__copyright__ = "Copyright (c) 2005-2008 Sun Microsystems Inc."
__license__   = "LGPL"

import pyatspi

import orca.speechgenerator as speechgenerator

class SpeechGenerator(speechgenerator.SpeechGenerator):
    """Overrides _getSpeechForTableCell so that, if this is an expanded 
       table cell,  we can strip off the "0 items".
    """

    def __init__(self, script):
        speechgenerator.SpeechGenerator.__init__(self, script)

    def _getSpeechForTableCell(self, obj, already_focused):
        """Get the speech utterances for a single table cell

        Arguments:
        - obj: the table
        - already_focused: False if object just received focus

        Returns a list of utterances to be spoken for the object.
        """

        utterances = speechgenerator.SpeechGenerator.\
                      _getSpeechForTableCell(self, obj, already_focused)

        # Check that we are in a table cell in the mail message header list.
        # If we are and this table cell has an expanded state, and the first
        # token of the last utterances is "0", then strip off that last 
        # utterance ("0 items"). See bug #432308 for more details.
        #
        rolesList = [pyatspi.ROLE_TABLE_CELL, \
                     pyatspi.ROLE_TREE_TABLE, \
                     pyatspi.ROLE_UNKNOWN]
        if self._script.isDesiredFocusedItem(obj, rolesList):
            state = obj.getState()
            if state and state.contains(pyatspi.STATE_EXPANDABLE):
                if state.contains(pyatspi.STATE_EXPANDED):
                    tokens = utterances[-1].split()
                    if tokens[0] == "0":
                        utterances = utterances[0:-1]

        return utterances
