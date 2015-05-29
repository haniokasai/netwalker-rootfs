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

"""Displays a GUI for the Orca main window."""

__id__        = "$Id: orca_gui_main.py 4666 2009-04-07 15:50:52Z wwalker $"
__version__   = "$Revision: 4666 $"
__date__      = "$Date: 2009-04-07 11:50:52 -0400 (Tue, 07 Apr 2009) $"
__copyright__ = "Copyright (c) 2005-2008 Sun Microsystems Inc."
__license__   = "LGPL"

import os
import sys
import gtk
import locale

import orca
import orca_glade
import platform

OS = None

class OrcaMainGUI(orca_glade.GladeWrapper):

    def init(self):
        pass

    def showGUI(self):
        """Show the Orca main window GUI. This assumes that the GUI has 
        already been created.
        """

        mainWindow = self.get_widget("mainWindow")
        self.set_orca_icon(mainWindow)

        accelGroup = gtk.AccelGroup()
        mainWindow.add_accel_group(accelGroup)
        helpButton = self.get_widget("helpButton")
        (keyVal, modifierMask) = gtk.accelerator_parse("F1")
        helpButton.add_accelerator("clicked",
                                   accelGroup,
                                   keyVal,
                                   modifierMask,
                                   0)

        mainWindow.show()

    def hideGUI(self):
        """Hide the Orca main window GUI. This assumes that the GUI has
        already been created.
        """

        self.get_widget("mainWindow").hide()

    def helpButtonClicked(self, widget):
        """Signal handler for the "clicked" signal for the helpButton
           GtkButton widget. The user has clicked the Help button.
           Call the method to bring up the Orca help window.

        Arguments:
        - widget: the component that generated the signal.
        """

        orca.helpForOrca()

    def quitButtonClicked(self, widget):
        """Signal handler for the "clicked" signal for the quitButton
           GtkButton widget. The user has clicked the Quit button.
           Call the method to bring up the Quit dialog.

        Arguments:
        - widget: the component that generated the signal.
        """

        orca.quitOrca()

    def preferencesButtonClicked(self, widget):
        """Signal handler for the "clicked" signal for the preferencesButton
           GtkButton widget. The user has clicked the Preferences button.
           Call the method to bring up the Preferences dialog.

        Arguments:
        - widget: the component that generated the signal.
        """

        orca.showPreferencesGUI()

    def mainWindowDestroyed(self, widget):
        """Signal handler for the "destroyed" signal for the mainWindow
           GtkWindow widget. Reset OS to None, then call the method to 
           bring up the quit dialog.

        Arguments:
        - widget: the component that generated the signal.
        """

        global OS

        OS = None
        orca.quitOrca()

def showMainUI():
    global OS

    if not OS:
        gladeFile = os.path.join(platform.prefix,
                                 platform.datadirname,
                                 platform.package,
                                 "glade",
                                 "orca-mainwin.glade")
        OS = OrcaMainGUI(gladeFile, "mainWindow")
        OS.init()

    OS.showGUI()

def hideMainUI():
    if OS:
        OS.hideGUI()

def main():
    locale.setlocale(locale.LC_ALL, '')

    showMainUI()

    gtk.main()
    sys.exit(0)

if __name__ == "__main__":
    main()
