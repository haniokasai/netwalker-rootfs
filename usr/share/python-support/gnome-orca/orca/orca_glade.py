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

"""Displays a GUI for the user to quit Orca."""

__id__        = "$Id: orca_glade.py 4617 2009-03-02 00:20:24Z wwalker $"
__version__   = "$Revision: 4617 $"
__date__      = "$Date: 2009-03-01 19:20:24 -0500 (Sun, 01 Mar 2009) $"
__copyright__ = "Copyright (c) 2005-2008 Sun Microsystems Inc."
__license__   = "LGPL"

import gettext
import gtk

class GladeWrapper:
    """
    Superclass for glade based applications. Just derive from this
    and your subclass should create methods whose names correspond to
    the signal handlers defined in the glade file. Any other attributes
    in your class will be safely ignored.

    This class will give you the ability to do:
        subclass_instance.GtkWindow.method(...)
        subclass_instance.widget_name...
    """

    def __init__(self, fileName, windowName):
        # Load glade file.
        self.widgets = gtk.glade.XML(fileName, windowName, gettext.textdomain())
        self.gtkWindow = getattr(self, windowName)

        instance_attributes = {}
        for attribute in dir(self.__class__):
            instance_attributes[attribute] = getattr(self, attribute)
        self.widgets.signal_autoconnect(instance_attributes)

    def set_orca_icon(self, window):
        """Set the "orca.png" icon as the icon for the Orca configuration
        window."""

        icon_theme = gtk.icon_theme_get_default()
        try:
            icon = icon_theme.load_icon("orca", 48, 0)
        except:
            return
        else:
            window.set_icon(icon)

    def get_widget(self, attribute):
        """Return the requested widget. This routine has been introduced
        (and calls to it made by the Orca Glade sub-classes), to prevent
        "No class attribute" pychecker errors caused when using __getattr__.

        Arguments:
        - attribute: name of the widget to return.
        """

        widget = self.widgets.get_widget(attribute)
        if widget is None:
            raise AttributeError("Widget [" + attribute + "] not found")

        return widget

    def __getattr__(self, attribute):   # Called when no attribute in __dict__
        widget = self.widgets.get_widget(attribute)
        if widget is None:
            raise AttributeError("Widget [" + attribute + "] not found")
        self.__dict__[attribute] = widget   # Add reference to cache.

        return widget
