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

"""Custom script for Mozilla.  NOT WORKING WELL AT THE MOMENT."""

__id__        = "$Id: Mozilla.py 4158 2008-09-06 10:05:13Z wwalker $"
__version__   = "$Revision: 4158 $"
__date__      = "$Date: 2008-09-06 06:05:13 -0400 (Sat, 06 Sep 2008) $"
__copyright__ = "Copyright (c) 2005-2008 Sun Microsystems Inc."
__license__   = "LGPL"

import orca.scripts.toolkits.Gecko as Gecko

class Script(Gecko.Script):
    def __init__(self, app):
        Gecko.Script.__init__(self, app)

        # By default, don't present if Mozilla is not the active application.
        #
        self.presentIfInactive = False
