#!/usr/bin/python
# -*- indent-tabs-mode: nil; tab-width: 4 -*-

import pygtk
import gtk
import gtk.glade
import gobject
import gnome
import gnome.ui
import gettext
import locale
import sys
import os
import re

locale.setlocale(locale.LC_ALL, '')
gtk.glade.bindtextdomain('language-installer', '/usr/share/locale')
gtk.glade.textdomain('language-installer')
gettext.install('language-installer', '/usr/share/locale')

tmpdir = "/tmp/language-installer"

class GUI():

    def __init__(self, install, visible):
        gnome.init('language-installer', '1.0')
        self.install = install
        self.visible = visible

        self.glade_file = "/usr/share/language-installer/ui/language-installer.glade"
        self.wTree = gtk.glade.XML(self.glade_file)

        self.window = self.wTree.get_widget('window')
        self.window.connect('delete-event', self.ignore)
        self.window.connect('response', self.response)

        self.label_please_wait = self.wTree.get_widget("label_please_wait")
        self.button_OK = self.wTree.get_widget("button_OK")

    def ignore(self, widget, event):
        return True

    def response(self, dlg, resp_id):
        # Only respect clicks from the OK button, else ignore it.
        if resp_id == 0:
            self.quit()

    def install_pkgs_done(self, pid, condition):
        # if not installing, don't quit immediately because user needs to
        # read the message and click OK to quit
        if self.install or not self.visible:
            self.quit()
        else:
            self.label_please_wait.set_text (_("The selected language is not completely installed. Please use Language tools later to complete the installation. "))
            self.button_OK.show()
            if self.window.window:
                self.window.window.set_cursor(None)

    def install_pkgs(self):
        try:
            (pid, sin, sout, serr) = gobject.spawn_async(
                                         ["install-langs", tmpdir],
                                         flags=gobject.SPAWN_SEARCH_PATH |
                                               gobject.SPAWN_DO_NOT_REAP_CHILD)
            gobject.child_watch_add(pid, self.install_pkgs_done)
            if self.window.window:
                self.window.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        except gobject.GError:
            self.install = False
            install_pkgs_done(self, None, None)

    def run(self):
        if self.visible:
            self.window.show()
        self.install_pkgs()
        gtk.main()

    def quit(self):
        gtk.main_quit()

if __name__ == "__main__":
    os.system('install-langs-setup %s' % tmpdir)

    # These files are set in install-lang-setup
    install = os.system('[ "$(cat %s/lang-present)" != "" ]' % tmpdir) == 0
    visible = os.system('[ "$(cat %s/pkgs)" != "" ]' % tmpdir) == 0

    app = GUI(install, visible)
    app.run()
    
    sys.exit()
