
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import gobject

import subprocess 
import gettext
from gettext import gettext as _
from tempfile import NamedTemporaryFile

import os
import os.path

import time
import thread
import apt_pkg


from AptUrl.UI import AbstractUI
from AptUrl import Helpers


class GtkUI(AbstractUI):
    def __init__(self):
        gtk.init_check()
        # create empty dialog
        self.dia_xml = gtk.glade.XML('/usr/share/apturl/apturl.glade', 
                                     'confirmation_dialog', 
                                     "apturl")
        self.dia = self.dia_xml.get_widget('confirmation_dialog')
        self.dia.realize()

    # generic dialogs
    def _get_dialog(self, dialog_type, summary, msg="", buttons=gtk.BUTTONS_CLOSE):
        " internal helper for dialog construction "
        d = gtk.MessageDialog(parent=self.dia,
                              flags=gtk.DIALOG_MODAL,
                              type=dialog_type,
                              buttons=buttons)
        d.set_title("")
        d.set_markup("<big><b>%s</b></big>\n\n%s" % (summary, msg))
        d.set_icon(gtk.icon_theme_get_default().load_icon('deb', 16, False))
        d.set_keep_above(True)
        d.realize()
        d.window.set_functions(gtk.gdk.FUNC_MOVE)
        return d
        
    def error(self, summary, msg=""):
        d = self._get_dialog(gtk.MESSAGE_ERROR, summary, msg)
        d.run()
        d.destroy()
        return False

    def message(self, summary, msg="", title=""):
        d = self._get_dialog(gtk.MESSAGE_INFO, summary, msg)
        d.set_title(title)
        d.run()
        d.destroy()
        return True

    def yesNoQuestion(self, summary, msg, title="", default='no'):
        d = self._get_dialog(gtk.MESSAGE_QUESTION, summary, msg,
                             buttons=gtk.BUTTONS_YES_NO)
        d.add_buttons
        d.set_title(title)
        res = d.run()
        d.destroy()
        if res != gtk.RESPONSE_YES:
            return False
        return True
    
    # specific dialogs
    def doEnableSection(self, sections):
        cmd = ["gksu", "--desktop",
               "/usr/share/applications/gnome-app-install.desktop",
               "--",
               "gnome-app-install-helper",
               "-e", "%s" % ' '.join(sections)]
        try:
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        except OSError, e:
            print >>sys.stderr, "Execution failed:", e
            return True
        #FIXME: Very ugly, but gksu doesn't return the correct exit states
        if not output.startswith("Enabled the "):
            return False
        return True

    
    def doEnableChannel(self, channelpath, channelkey):
        cmd = ["gksu",
               "--desktop", "/usr/share/applications/gnome-app-install.desktop",
               "--",
               "install", "--mode=644","--owner=0",channelpath,
               apt_pkg.Config.FindDir("Dir::Etc::sourceparts")]
        res=subprocess.call(cmd)
        if not res == 0:
            return False
        # install the key as well
        if os.path.exists(channelkey):
            cmd = ["gksu",
                   "--desktop",
                   "/usr/share/applications/gnome-app-install.desktop",
                   "--",
                   "apt-key", "add",channelkey]
            res=subprocess.call(cmd)
            if not res == 0:
                return False
        return True

    def askInstallPackage(self, package, summary, description, homepage):
        # populate the dialog
        dia = self.dia
        dia_xml = self.dia_xml
        header = _("Install additional software?")
        body = _("Do you want to install package '%s'?") % package
        dia.set_keep_above(True)
        dia.set_title('')
        header_label = dia_xml.get_widget('header_label')
        header_label.set_markup("<b><big>%s</big></b>" % header)
        body_label = dia_xml.get_widget('body_label')
        body_label.set_label(body)
        description_text_view = dia_xml.get_widget('description_text_view')
        tbuf = gtk.TextBuffer()
        desc = "%s\n\n%s" % (summary, Helpers.format_description(description))
        tbuf.set_text(desc)
        description_text_view.set_buffer(tbuf)
        dia.set_icon(gtk.icon_theme_get_default().load_icon('deb', 16, False))
        
        # check if another package manager is already running
        # FIXME: just checking for the existance of the file is
        #        not sufficient, it need to be tested if it can
        #        be locked via apt_pkg.GetLock() 
        #        - but that needs to run as root 
        #        - a dbus helper might be the best answer here
        #args = (update_button_status, dia_xml.get_widget("yes_button"),
        #    dia_xml.get_widget("infolabel"))
        #args[0](*args[1:])
        #timer_id = gobject.timeout_add(750, *args )
        
        # show the dialog
        res = dia.run()
        #gobject.source_remove(timer_id)
        if res != gtk.RESPONSE_YES:
            dia.hide()
            return False
        
        # don't set on-top while installing
        dia.set_keep_above(False)
        return True

#    def _update_button_status(button, label):
#        if os.path.isfile("/var/lib/dpkg/lock"):
#            button.set_sensitive(False)
#            label.set_markup("<b>Another package manager is already running...</b>")
#        else:
#            button.set_sensitive(True)
#            label.set_text("")
#        return True

    # progress etc
    def doUpdate(self):
        p = subprocess.Popen(['gksu',
                              '--desktop',
                              '/usr/share/applications/synaptic.desktop',
                              '--',
                              '/usr/sbin/synaptic',
                              '--hide-main-window',
                              '--non-interactive',
                              '--parent-window-id', str(self.dia.window.xid),
                              '--update-at-startup',
                              ])
        self._wait_for_synaptic(p)

    def doInstall(self, apturl):
        # run synaptic
        temp = NamedTemporaryFile()
        temp.write("%s\t install\n" % apturl.package)
        temp.flush()
        p = subprocess.Popen(['gksu',
                              '--desktop',
                              '/usr/share/applications/synaptic.desktop',
                              '--',
                              '/usr/sbin/synaptic',
                              '--hide-main-window',
                              '--non-interactive',
                              '--parent-window-id', str(self.dia.window.xid),
                              '--set-selections-file', temp.name
                              ])
        self._wait_for_synaptic(p)
        temp.close()    

    # helpers
    def _wait_for_p(self, p, lock):
        " helper for the thread to wait for process p to finish "
        p.wait()
        lock.release()

    def _wait_for_synaptic(self, p):
        # wait for synaptic
        lock = thread.allocate_lock()
        lock.acquire()
        thread.start_new_thread(self._wait_for_p, (p, lock))

        self.dia.set_sensitive(False)
        while lock.locked():
            while gtk.events_pending():
                gtk.main_iteration()
            time.sleep(0.01)
        self.dia.set_sensitive(True)
        return True


if __name__ == "__main__":
    ui = GtkUI()
    ui.error("foo","bar")
