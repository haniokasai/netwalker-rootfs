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

__id__        = "$Id: script.py 3882 2008-05-07 18:22:10Z richb $"
__version__   = "$Revision: 3882 $"
__date__      = "$Date: 2008-05-07 14:22:10 -0400 (Wed, 07 May 2008) $"
__copyright__ = "Copyright (c) 2006-2008 Sun Microsystems Inc."
__license__   = "LGPL"

import orca.default as default

from speech_generator import SpeechGenerator
from braille_generator import BrailleGenerator

########################################################################
#                                                                      #
# The planner script class.                                            #
#                                                                      #
########################################################################

class Script(default.Script):

    def __init__(self, app):
        """Creates a new script for the given application.

        Arguments:
        - app: the application to create a script for.
        """
        default.Script.__init__(self, app)

    # This method tries to detect and handle the following cases:
    # 1) Toolbar: the last toggle button to show 'more options'
    # 2) Main window: one of the four graphic toggle buttons.
    #
    def getBrailleGenerator(self):
        return BrailleGenerator(self)

    def getSpeechGenerator(self):
        return SpeechGenerator(self)
