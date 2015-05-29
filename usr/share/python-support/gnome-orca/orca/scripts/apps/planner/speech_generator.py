# Orca
#
# Copyright 2006-2008 Sun Microsystems Inc.
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

"""Custom script for planner."""

__id__        = "$Id: speech_generator.py 4221 2008-09-15 08:11:23Z wwalker $"
__version__   = "$Revision: 4221 $"
__date__      = "$Date: 2008-09-15 04:11:23 -0400 (Mon, 15 Sep 2008) $"
__copyright__ = "Copyright (c) 2006-2008 Sun Microsystems Inc."
__license__   = "LGPL"

import orca.speechgenerator as speechgenerator
import pyatspi

from orca.orca_i18n import _ # for gettext support

class SpeechGenerator(speechgenerator.SpeechGenerator):

    def __init__(self, script):
        speechgenerator.SpeechGenerator.__init__(self, script)

    # We make this to appropiately present ribbon's toggle button in a
    # toolbar used to display in a menu those options that doesn fill
    # in toolbar when the application is resized.
    #
    # Also for each one of the grphics buttons in the main window
    #
    def _getSpeechForToggleButton(self, obj, already_focused):
        utterances = []
        tmp = []

        # Application should implement an accessible name in this
        # component, but until this is made We speech/braille "display
        # more options" when the focus is in one of these toggle
        # buttons.
        #

        roleList = [pyatspi.ROLE_TOGGLE_BUTTON, \
                    pyatspi.ROLE_TOOL_BAR]

        if self._script.isDesiredFocusedItem(obj, roleList) and not obj.name:
            if not already_focused:
                tmp.append(_("Display more options"))
                tmp.extend(self._getDefaultSpeech(obj, already_focused))

                if obj.getState().contains(pyatspi.STATE_CHECKED):
                    tmp.append(_("pressed"))
                else:
                    tmp.append(_("not pressed"))

                utterances.extend(tmp)
                utterances.extend(self._getSpeechForObjectAvailability(obj))
            else:
                if obj.getState().contains(pyatspi.STATE_CHECKED):
                    utterances.append(_("pressed"))
                else:
                    utterances.append(_("not pressed"))

            return utterances

        return self._getSpeechForLabel(obj, already_focused)
