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

"""A script to do nothing.  This is for self-voicing apps."""

__id__        = "$Id: self_voicing.py 3882 2008-05-07 18:22:10Z richb $"
__version__   = "$Revision: 3882 $"
__date__      = "$Date: 2008-05-07 14:22:10 -0400 (Wed, 07 May 2008) $"
__copyright__ = "Copyright (c) 2005-2008 Sun Microsystems Inc."
__license__   = "LGPL"

import orca.default as default

class Script(default.Script):
    """A script to do nothing.  This is for self-voicing apps."""
    
    def __init__(self, app):
        """Creates a script for the given application, if necessary.
        This method should not be called by anyone except the
        focus_tracking_presenter.

        Arguments:
        - app: the Python Accessible application to create a script for
        """

        default.Script.__init__(self, app)

    def getBrailleGenerator(self):
        """Returns the braille generator for this script.
        """
        return None

    def getSpeechGenerator(self):
        """Returns the speech generator for this script.
        """
        return None

    def processObjectEvent(self, event):
        """Does nothing.

        Arguments:
        - event: the Event
        """
        pass

    def processKeyboardEvent(self, keyboardEvent):
        """Does nothing.

        Arguments:
        - keyboardEvent: an instance of input_event.KeyboardEvent

        Returns False to indicate the event was not consumed.
        """
        return False

    def processBrailleEvent(self, brailleEvent):
        """Does nothing.

        Arguments:
        - brailleEvent: an instance of input_event.BrailleEvent

        Returns False to indicate the event was not consumed.
        """
        return False
