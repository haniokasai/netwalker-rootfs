# Orca
#
# Copyright 2005-2006 Sun Microsystems Inc.
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
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

"""Custom script for Ubuiquity."""

__id__        = "$Id: Ubiquity.py,v 1.63 2006/07/28 17:33:18 wwalker Exp $"
__version__   = "$Revision: 1.63 $"
__date__      = "$Date: 2006/07/28 17:33:18 $"
__copyright__ = "Copyright (c) 2005-2006 Sun Microsystems Inc."
__license__   = "LGPL"

import orca.default as default
import orca.rolenames as rolenames
import orca.speech as speech
import orca.util as util

########################################################################
#                                                                      #
# The Ubiquity script class.                                           #
#                                                                      #
########################################################################

class Script(default.Script):

    def __init__(self, app):
        """Creates a new script for the given application.

        Arguments:
        - app: the application to create a script for.
        """

        default.Script.__init__(self, app)

        self.setupLabels = {}
        self.currentTab = None

    def onWindowActivated(self, event):
        if self.currentTab:                 #Speak current open tab
            obj = self.currentTab.child(0)            
            for n in range(obj.childCount):                    
                if  util.getDisplayedText(obj.child(n)):                
                    speech.speak(util.getDisplayedText(obj.child(n)))
        
        default.Script.onWindowActivated(self, event)

    def onSelectionChanged(self, event):        
        
        if event.source.name:#for location selection.
            panel = event.source.parent
            
            allLabels = util.findByRole(panel, rolenames.ROLE_LABEL)
            
            speech.speak(util.getDisplayedText(allLabels[6]))
            speech.speak(util.getDisplayedText(event.source))
            speech.speak(util.getDisplayedText(allLabels[3]))
            speech.speak(util.getDisplayedText(allLabels[0]))
            speech.speak(util.getDisplayedText(allLabels[5]))
            speech.speak(util.getDisplayedText(allLabels[2]))
            speech.speak(util.getDisplayedText(allLabels[4]))
            speech.speak(util.getDisplayedText(allLabels[1]))
        return

    def onStateChanged(self, event):                        
        if event.detail1 == 1 and event.type.endswith("showing"):    
            # for text box on last page.
            if event.source.role == rolenames.ROLE_VIEWPORT and \
               event.source.child(0).role == rolenames.ROLE_TEXT:
                speech.speak(util.getDisplayedText(event.source.child(0)))

            obj = event.source
            # To read the headers and instruction labels not associated
            # with an input widget.
            #
            while not obj.role == rolenames.ROLE_FRAME:
                if obj.parent.role == rolenames.ROLE_PAGE_TAB and \
                   not self.currentTab == obj.parent:
                    self.currentTab = obj.parent
                    
                    for n in range(obj.childCount):                    
                        if  util.getDisplayedText(obj.child(n)):                
                            speech.speak(util.getDisplayedText(obj.child(n)))
                        
                    return
                else:
                    obj = obj.parent            
