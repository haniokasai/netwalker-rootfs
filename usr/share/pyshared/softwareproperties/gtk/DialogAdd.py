# dialog_add.py.in - dialog to add a new repository
#  
#  Copyright (c) 2004-2005 Canonical
#                2005 Michiel Sikkes
#              
#  Authors: 
#       Michael Vogt <mvo@debian.org>
#       Michiel Sikkes <michiels@gnome.org>
#       Sebastian Heinlein <glatzor@ubuntu.com>
#
#  This program is free software; you can redistribute it and/or 
#  modify it under the terms of the GNU General Public License as 
#  published by the Free Software Foundation; either version 2 of the
#  License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
#  USA

import os
import gobject
import gtk
import gtk.glade
from gettext import gettext as _

from aptsources.sourceslist import SourceEntry

class DialogAdd:
  def __init__(self, parent, sourceslist, datadir, distro):
    """
    Initialize the dialog that allows to add a new source entering the
    raw apt line
    """
    self.sourceslist = sourceslist
    self.parent = parent
    self.datadir = datadir
    # gtk stuff
    self.gladexml = gtk.glade.XML("%s/glade/dialogs.glade" % datadir)
    self.dialog = self.gladexml.get_widget("dialog_add_custom")
    self.dialog.set_transient_for(self.parent)
    self.entry = self.gladexml.get_widget("entry_source_line")
    self.button_add = self.gladexml.get_widget("button_add_source")
    self.entry.connect("changed", self.check_line)
    self.label_example_line = self.gladexml.get_widget("label_example_line")
    # Create an example deb line from the currently used distro
    if distro:
        example = "%s %s %s %s" % (distro.binary_type,
                                   distro.source_template.base_uri,
                                   distro.codename,
                                   distro.source_template.components[0].name)
    else:
        example = "deb http://ftp.debian.org sarge main"
    # L10N: the example is of the format: deb http://ftp.debian.org sarge main
    msg = _("The APT line includes the type, location and components of a "
            "repository, for example  '%s'.") % ("<i>%s</i>" % example)
    self.label_example_line.set_label(msg)

  def run(self):
    res = self.dialog.run()
    self.dialog.hide()
    if res == gtk.RESPONSE_OK:
        line = self.entry.get_text() + "\n"
    else:
        line = None
    return line

  def check_line(self, *args):
    """
    Check for a valid apt line and set the sensitiveness of the
    button 'add' accordingly
    """
    line = self.entry.get_text() + "\n"
    source_entry = SourceEntry(line)
    if source_entry.invalid == True or source_entry.disabled == True:
        self.button_add.set_sensitive(False)
    else:
        self.button_add.set_sensitive(True)

