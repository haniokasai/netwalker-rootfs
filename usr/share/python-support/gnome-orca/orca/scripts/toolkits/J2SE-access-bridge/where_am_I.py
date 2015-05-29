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

__id__        = "$Id: where_am_I.py 4221 2008-09-15 08:11:23Z wwalker $"
__version__   = "$Revision: 4221 $"
__date__      = "$Date: 2008-09-15 04:11:23 -0400 (Mon, 15 Sep 2008) $"
__copyright__ = "Copyright (c) 2005-2008 Sun Microsystems Inc."
__license__   = "LGPL"

import pyatspi

import orca.where_am_I as where_am_I

########################################################################
#                                                                      #
# Custom WhereAmI                                                      #
#                                                                      #
########################################################################

class WhereAmI(where_am_I.WhereAmI):
    def __init__(self, script):
        where_am_I.WhereAmI.__init__(self, script)

    def whereAmI(self, obj, basicOnly):
        """Calls the base class method for basic information and Java
        specific presentation methods for detailed/custom information.
        """

        # If we're in the text area of a spin button, then we'll do the
        # where am I for the spin button.
        #
        if obj and obj.getRole() == pyatspi.ROLE_TEXT:
            spinbox = self._script.getAncestor(obj,
                                               [pyatspi.ROLE_SPIN_BUTTON],
                                               None)
            if spinbox:
                obj = spinbox

        where_am_I.WhereAmI.whereAmI(self, obj, basicOnly)
