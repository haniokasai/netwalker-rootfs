# DistUpgradeFetcher.py 
#  
#  Copyright (c) 2006 Canonical
#  
#  Author: Michael Vogt <michael.vogt@ubuntu.com>
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

import pygtk
pygtk.require('2.0')
import gtk

from ReleaseNotesViewer import ReleaseNotesViewer
from Core.utils import *
from Core.DistUpgradeFetcherCore import DistUpgradeFetcherCore
from gettext import gettext as _
import urllib2
import dbus
import os
import socket


class DistUpgradeFetcherGtk(DistUpgradeFetcherCore):

    def __init__(self, new_dist, progress, parent):
        DistUpgradeFetcherCore.__init__(self,new_dist,progress)
        self.parent = parent
        self.window_main = parent.window_main

    def error(self, summary, message):
        return error(self.window_main, summary, message)

    def runDistUpgrader(self):
        inhibit_sleep()
        # now run it with sudo
        if os.getuid() != 0:
            os.execv("/usr/bin/gksu",["gksu",
                                      "--desktop","/usr/share/applications/update-manager.desktop",
                                      "--",
                                      self.script]+self.run_options)
        else:
            os.execv(self.script,[self.script]+self.run_options)
        # we shouldn't come to this point, but if we do, undo our
        # inhibit sleep
        allow_sleep()

    def showReleaseNotes(self):
      # FIXME: care about i18n! (append -$lang or something)
      if self.new_dist.releaseNotesURI != None:
          uri = self._expandUri(self.new_dist.releaseNotesURI)
          self.window_main.set_sensitive(False)
          self.window_main.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
          while gtk.events_pending():
              gtk.main_iteration()

          # download/display the release notes
          # FIXME: add some progress reporting here
          res = gtk.RESPONSE_CANCEL
          timeout = socket.getdefaulttimeout()
          try:
              socket.setdefaulttimeout(5)
              release_notes = urllib2.urlopen(uri)
              notes = release_notes.read()
              textview_release_notes = ReleaseNotesViewer(notes)
              textview_release_notes.show()
              self.parent.scrolled_notes.add(textview_release_notes)
              self.parent.dialog_release_notes.set_transient_for(self.window_main)
              res = self.parent.dialog_release_notes.run()
              self.parent.dialog_release_notes.hide()
          except urllib2.HTTPError:
              primary = "<span weight=\"bold\" size=\"larger\">%s</span>" % \
                        _("Could not find the release notes")
              secondary = _("The server may be overloaded. ")
              dialog = gtk.MessageDialog(self.window_main,gtk.DIALOG_MODAL,
                                         gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"")
              dialog.set_title("")
              dialog.set_markup(primary);
              dialog.format_secondary_text(secondary);
              dialog.run()
              dialog.destroy()
          except IOError:
              primary = "<span weight=\"bold\" size=\"larger\">%s</span>" % \
                        _("Could not download the release notes")
              secondary = _("Please check your internet connection.")
              dialog = gtk.MessageDialog(self.window_main,gtk.DIALOG_MODAL,
                                         gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"")
              dialog.set_title("")
              dialog.set_markup(primary);
              dialog.format_secondary_text(secondary);
              dialog.run()
              dialog.destroy()
          socket.setdefaulttimeout(timeout)              
          self.window_main.set_sensitive(True)
          self.window_main.window.set_cursor(None)
          # user clicked cancel
          if res == gtk.RESPONSE_OK:
              return True
      return False

if __name__ == "__main__":
    error(None, "summary","message")
    d = DistUpgradeFetcherGtk(None,None)
    print d.authenticate('/tmp/Release','/tmp/Release.gpg')

