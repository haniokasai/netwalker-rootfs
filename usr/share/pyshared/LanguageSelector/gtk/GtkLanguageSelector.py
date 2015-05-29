# (c) 2005 Canonical
# Author: Michael Vogt <michael.vogt@ubuntu.com>
#
# Released under the GPL
#

import pygtk
pygtk.require('2.0')
import gtk
import gtk.gdk
import gtk.glade
import pango
import gobject
import os.path
import string
import warnings
warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)
import apt
import apt_pkg
import os.path
import shutil
import subprocess
import thread
import time
import gettext
import sys
import tempfile
import pwd
import grp
import os

from gettext import gettext as _

 
(LIST_LANG,                     # language (i18n/human-readable)
 LIST_LANG_INFO                 # the short country code (e.g. de, pt_BR)
 ) = range(2)

(COMBO_LANGUAGE,
 COMBO_CODE) = range(2)



from LanguageSelector.gtk.SimpleGladeApp import SimpleGladeApp
from LanguageSelector.LocaleInfo import LocaleInfo
from LanguageSelector.LanguageSelector import *
from LanguageSelector.ImSwitch import ImSwitch


def xor(a,b):
    " helper to simplify the reading "
    return a ^ b

def blockSignals(f):
    " decorator to ensure that the signals are blocked "
    def wrapper(*args, **kwargs):
        args[0]._blockSignals = True
        res = f(*args, **kwargs)
        args[0]._blockSignals = False
        return res
    return wrapper

def honorBlockedSignals(f):
    " decorator to ensure that the signals are blocked "
    def wrapper(*args, **kwargs):
        if args[0]._blockSignals:
            return
        res = f(*args, **kwargs)
        return res
    return wrapper

def insensitive(f):
    """
    decorator to ensure that a given function is run insensitive
    warning: this will not stack well so don't use it for nested
    stuff (a @insensitive func calling a @insensitve one)
    """
    def wrapper(*args, **kwargs):
        args[0].setSensitive(False)
        res = f(*args, **kwargs)
        args[0].setSensitive(True)
    return wrapper



# intervals of the start up progress
# 3x caching and menu creation
STEPS_UPDATE_CACHE = [33, 66, 100]

class GtkProgress(apt.OpProgress):
    def __init__(self, host_window, progressbar, parent,
                 steps=STEPS_UPDATE_CACHE):
        # used for the "one run progressbar"
        self.steps = steps[:]
        self.base = 0
        self.old = 0
        self.next = int(self.steps.pop(0))

        self._parent = parent
        self._window = host_window
        self._progressbar = progressbar
        self._window.realize()
        host_window.window.set_functions(gtk.gdk.FUNC_MOVE)
        self._window.set_transient_for(parent)
    def update(self, percent):
        #print percent
        #print self.Op
        #print self.SubOp
        self._window.show()
        self._parent.set_sensitive(False)
        # if the old percent was higher, a new progress was started
        if self.old > percent:
            # set the borders to the next interval
            self.base = self.next
            try:
                self.next = int(self.steps.pop(0))
            except:
                pass
        progress = self.base + percent/100 * (self.next - self.base)
        self.old = percent
        self._progressbar.set_fraction(progress/100.0)
        while gtk.events_pending():
            gtk.main_iteration()
    def done(self):
        self._parent.set_sensitive(True)
    def hide(self):
        self._window.hide()

class GtkLanguageSelector(LanguageSelectorBase,  SimpleGladeApp):

    def __init__(self, datadir, options):
        LanguageSelectorBase.__init__(self, datadir)
        SimpleGladeApp.__init__(self,
                                datadir+"/data/LanguageSelector.glade",
                                domain="language-selector")

        self.is_admin = grp.getgrnam("admin")[2] in os.getgroups()
        # see if we have any other human users on this system
        self.has_other_users = False
        num = 0
        for l in pwd.getpwall():
            if l.pw_uid >= 500 and l.pw_uid < 65534:
                num += 1
            if num >= 2:
                self.has_other_users = True
                break
        
        #build the comboboxes (with model)
        combo = self.combobox_system_language
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', COMBO_LANGUAGE)
        combo.set_model(model)
        self.combo_syslang_dirty = False

        combo = self.combobox_user_language
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', COMBO_LANGUAGE)
        combo.set_model(model)
        self.combo_userlang_dirty = False
        self.imSwitch = ImSwitch()
        self.options = options
        self._blockSignals = False

        # build the treeview
        self.setupTreeView()
        self.updateLanguageView()
        self.updateUserDefaultCombo()
        self.updateSystemDefaultCombo()
        self.check_input_methods()
        self.updateSyncButton()
        
        # apply button
        self.button_apply.set_sensitive(False)

        # show it
        self.window_main.show()
        self.setSensitive(False)

        # check if the package list is up-to-date
        if not self._cache.havePackageLists:
            d = gtk.MessageDialog(parent=self.window_main,
                                  flags=gtk.DIALOG_MODAL,
                                  type=gtk.MESSAGE_INFO,
                                  buttons=gtk.BUTTONS_CANCEL)
            d.set_markup("<big><b>%s</b></big>\n\n%s" % (
                _("No language information available"),
                _("The system does not have information about the "
                  "available languages yet. Do you want to perform "
                  "a network update to get them now? ")))
            d.set_title=("")
            d.add_button(_("_Update"), gtk.RESPONSE_YES)
            res = d.run()
            d.destroy()
            if res == gtk.RESPONSE_YES:
                self.setSensitive(False)
                self.update()
                self.updateLanguageView()
                self.setSensitive(True)

        # see if something is missing
        if self.options.verify_installed:
            self.verifyInstalledLangPacks()

        if not self.imSwitch.available():
            self.checkbutton_enable_input_methods.set_sensitive(False)
        self.setSensitive(True)

    def setSensitive(self, value):
        if value:
            self.window_main.set_sensitive(True)
            self.window_main.window.set_cursor(None)
        else:
            self.window_main.set_sensitive(False)
            self.window_main.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending():
            gtk.main_iteration()

    def runAsRoot(self, userCmd):
        " run the given command as root using gksu "
        cmd = ["/usr/bin/gksu", 
               "--desktop", 
               "/usr/share/applications/language-selector.desktop", 
               "--"]
        ret = subprocess.call(cmd+userCmd)
        return (ret == 0)

    @blockSignals
    def updateSyncButton(self):
        " check if the sync languages button should be enabled or not "
        button = self.checkbutton_sync_languages
        combo = self.combobox_system_language
        # no admin user, gray out
        if self.is_admin == False:
            button.set_active(False)
            button.set_sensitive(False)
            combo.set_sensitive(False)
            return
        # admin user, check stuff
        button.set_sensitive(True)
        combo.set_sensitive(True)
        # do not enable the keep the same button if the system has other
        # users or if the language settings are inconsistent already
        userlang = self.combobox_user_language.get_active()
        systemlang = self.combobox_system_language.get_active()
        if (not self.has_other_users and userlang == systemlang):
            button.set_active(True)
        else:
            button.set_active(False)

    def setupTreeView(self):
        """ do all the treeview setup here """
        def toggle_cell_func(column, cell, model, iter):
            langInfo = model.get_value(iter, LIST_LANG_INFO)

            # check for active and inconsitent 
            inconsistent = langInfo.inconsistent
            #if inconsistent:
            #    print "%s is inconsistent" % langInfo.language

            cell.set_property("active", langInfo.fullInstalled)
            cell.set_property("inconsistent", inconsistent)
            
        def lang_view_func(cell_layout, renderer, model, iter):
            langInfo = model.get_value(iter, LIST_LANG_INFO)
            inconsistent = langInfo.inconsistent
            if (langInfo.changes) :
                markup = "<b>%s</b>" % langInfo.language
            else:
                markup = "%s" % langInfo.language
            renderer.set_property("markup", markup)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Language"), renderer, text=LIST_LANG)
        column.set_property("expand", True)
        column.set_cell_data_func (renderer, lang_view_func)
        self.treeview_languages.append_column(column)

        renderer= gtk.CellRendererToggle()
        renderer.connect("toggled", self.on_toggled)
        column = gtk.TreeViewColumn(_("Installed"), renderer)
        column.set_cell_data_func (renderer, toggle_cell_func)
        self.treeview_languages.append_column(column)
        # build the store
        self._langlist = gtk.ListStore(str, gobject.TYPE_PYOBJECT)
        self.treeview_languages.set_model(self._langlist)

    def _get_langinfo_on_cursor(self):
        (path, column) = self.treeview_languages.get_cursor ()
        if not path:
            return None
        iter = self._langlist.get_iter(path)
        langInfo = self._langlist.get_value(iter, LIST_LANG_INFO)
        return langInfo

    # details checkboxes
    def on_checkbutton_fonts_clicked(self, button):
        if self.block_toggle: return
        langInfo = self._get_langinfo_on_cursor()
        langInfo.languagePkgList["languageSupportFonts"].doChange = not langInfo.languagePkgList["languageSupportFonts"].doChange
        self.check_status()
        self.treeview_languages.queue_draw()
        #self.debug_pkg_status()
    def on_checkbutton_input_methods_clicked(self, button):
        if self.block_toggle: return
        langInfo = self._get_langinfo_on_cursor()
        langInfo.languagePkgList["languageSupportInputMethods"].doChange = not langInfo.languagePkgList["languageSupportInputMethods"].doChange
        self.check_status()
        self.treeview_languages.queue_draw()
        #self.debug_pkg_status()
    def on_checkbutton_writing_aids_clicked(self, button):
        if self.block_toggle: return
        langInfo = self._get_langinfo_on_cursor()
        langInfo.languagePkgList["languageSupportWritingAids"].doChange = not langInfo.languagePkgList["languageSupportWritingAids"].doChange
        self.check_status()
        self.treeview_languages.queue_draw()
        #self.debug_pkg_status()
    def on_checkbutton_basic_translations_clicked(self, button):
        if self.block_toggle: return
        langInfo = self._get_langinfo_on_cursor()
        langInfo.languagePkgList["languagePack"].doChange = not langInfo.languagePkgList["languagePack"].doChange
        self.check_status()
        self.treeview_languages.queue_draw()
        #self.debug_pkg_status()
    def on_checkbutton_extra_translations_clicked(self, button):
        if self.block_toggle: return
        langInfo = self._get_langinfo_on_cursor()
        langInfo.languagePkgList["languageSupportTranslations"].doChange = not langInfo.languagePkgList["languageSupportTranslations"].doChange
        self.check_status()
        self.treeview_languages.queue_draw()
        #self.debug_pkg_status()
    def on_checkbutton_extra_clicked(self, button):
        if self.block_toggle: return
        langInfo = self._get_langinfo_on_cursor()
        langInfo.languagePkgList["languageSupportExtra"].doChange = not langInfo.languagePkgList["languageSupportExtra"].doChange
        self.check_status()
        self.treeview_languages.queue_draw()
        #self.debug_pkg_status()

    # the global toggle
    def on_toggled(self, renderer, path_string):
        """ called when on install toggle """
        iter = self._langlist.get_iter_from_string(path_string)
        langInfo = self._langlist.get_value(iter, LIST_LANG_INFO)

        # special handling for inconsistent state
        if langInfo.inconsistent :
            for pkg in langInfo.languagePkgList.values() :
                if (pkg.available and not pkg.installed) : 
                    pkg.doChange = True
        elif langInfo.fullInstalled :
            for pkg in langInfo.languagePkgList.values() :
                if (pkg.available) :
                    if (not pkg.installed and pkg.doChange) :
                        pkg.doChange = False
                    elif (pkg.installed and not pkg.doChange) :
                        pkg.doChange = True
        else :
            for pkg in langInfo.languagePkgList.values() :
                if (pkg.available) :
                    if (pkg.installed and pkg.doChange) :
                        pkg.doChange = False
                    elif (not pkg.installed and not pkg.doChange) :
                        pkg.doChange = True

        self.check_status()
        self.treeview_languages.queue_draw()
        #self.debug_pkg_status()

    def on_treeview_languages_cursor_changed(self, treeview):
        #print "on_treeview_languages_cursor_changed()"
        langInfo = self._get_langinfo_on_cursor()
        for (button, attr) in ( 
              ("checkbutton_basic_translations", langInfo.languagePkgList["languagePack"]),
              ("checkbutton_extra_translations", langInfo.languagePkgList["languageSupportTranslations"]),
              ("checkbutton_writing_aids", langInfo.languagePkgList["languageSupportWritingAids"]),
              ("checkbutton_input_methods", langInfo.languagePkgList["languageSupportInputMethods"]),
              ("checkbutton_extra", langInfo.languagePkgList["languageSupportExtra"]),
              ("checkbutton_fonts", langInfo.languagePkgList["languageSupportFonts"])  ):
            self.block_toggle = True
            if ((attr.installed and not attr.doChange) or (not attr.installed and attr.doChange)) :
                getattr(self, button).set_active(True)
            else :
                getattr(self, button).set_active(False)
            getattr(self, button).set_sensitive(attr.available)
            self.block_toggle = False
            #self.debug_pkg_status()

    def on_button_install_remove_languages_clicked(self, widget):
        self.window_installer.show()

    def debug_pkg_status(self):
        langInfo = self._get_langinfo_on_cursor()
        for pkg in langInfo.languagePkgList.items() :
            print ("%s, available: %s, installed: %s, doChange: %s" % (pkg[0], pkg[1].available, pkg[1].installed, pkg[1].doChange))
        print ("inconsistent? : %s" % langInfo.inconsistent)

    def check_status(self):
        changed = False
        countInstall = 0
        countRemove = 0
        for (lang, langInfo) in self._langlist:
            if langInfo.changes:
                changed = True
                for item in langInfo.languagePkgList.values():
                    if item.doChange:
                        if item.installed:
                            countRemove = countRemove + 1
                        else:
                            countInstall = countInstall + 1
        #print "%d to install, %d to remove" % (countInstall, countRemove)
        textInstall = gettext.ngettext("%d to install", "%d to install", countInstall) % countInstall
        textRemove = gettext.ngettext("%d to remove", "%d to remove", countRemove) % countRemove
        if countRemove == 0 and countInstall == 0: 
            self.label_install_remove.set_text("")
        elif countRemove == 0: 
            self.label_install_remove.set_text(textInstall)
        elif countInstall == 0: 
            self.label_install_remove.set_text(textRemove)
        # Translators: this string will concatenate the "%n to install" and "%n to remove" strings, you can replace the comma if you need to.
        else: 
            self.label_install_remove.set_text(_("%s, %s") % (textInstall, textRemove))
        
        if changed:
            self.button_apply.set_sensitive(True)
        else:
            self.button_apply.set_sensitive(False)

    @honorBlockedSignals
    @insensitive
    def on_combobox_system_language_changed(self, widget):
        #print "on_combobox_system_language_changed()"
        if self.writeSystemDefaultLang():
            # queue a restart of gdm (if it is runing) to make the new
            # locales usable
            gdmscript = "/etc/init.d/gdm"
            if os.path.exists("/var/run/gdm.pid") and os.path.exists(gdmscript):
                self.runAsRoot(["invoke-rc.d","gdm","reload"])
        self.updateSystemDefaultCombo()
        if self.checkbutton_sync_languages.get_active() == True:
            self.combobox_user_language.set_active(self.combobox_system_language.get_active())
            self.updateUserDefaultCombo()

    @honorBlockedSignals
    @insensitive
    def on_combobox_user_language_changed(self, widget):
        #print "on_combobox_user_language_changed()"
        self.check_input_methods()
        self.writeUserDefaultLang()
        self.updateUserDefaultCombo()
        if self.checkbutton_sync_languages.get_active() == True:
            self.combobox_system_language.set_active(self.combobox_user_language.get_active())
            self.updateSystemDefaultCombo()

    @blockSignals
    def check_input_methods(self):
        """ check if the selected langauge has input method support
            and set checkbutton_enable_input_methods accordingly
        """
        if not self.imSwitch.available():
            return
        # get current selected default language
        combo = self.combobox_user_language
        model = combo.get_model()
        if combo.get_active() < 0:
            return
        (lang, code) = model[combo.get_active()]
        # check if that has a im-switch config
        active = self.imSwitch.enabledForLocale(code)
        self.checkbutton_enable_input_methods.set_active(active)

    def writeInputMethodConfig(self):
        """ 
        write new input method defaults - currently we only support all_ALL
        """
        combo = self.combobox_user_language
        model = combo.get_model()
        if combo.get_active() < 0:
            return
        (lang, code) = model[combo.get_active()]
        # check if we need to do something
        new_value = self.checkbutton_enable_input_methods.get_active()
        if self.imSwitch.enabledForLocale(code) != new_value:
            if new_value:
                self.imSwitch.enable(code)
            else:
                self.imSwitch.disable(code)
            #self.showRebootRequired()
            #self.checkReloginNotification()

    @honorBlockedSignals
    def on_checkbutton_enable_input_methods_toggled(self, widget):
        #print "on_checkbutton_enable_input_methods_toggled()"
        active = self.checkbutton_enable_input_methods.get_active()
        self.combo_userlang_dirty = True
        self.setSensitive(False)
        self.writeInputMethodConfig()
        self.setSensitive(True)

    @honorBlockedSignals
    def on_checkbutton_sync_languages_toggled(self, widget):
        #print "on_checkbutton_sync_languages_toggled()"
        if self.checkbutton_sync_languages.get_active() == True:
            self.combobox_user_language.set_active(self.combobox_system_language.get_active())
            self.updateSystemDefaultCombo()
        
    def build_commit_lists(self):
        for (lang, langInfo) in self._langlist:
            self._cache.tryChangeDetails(langInfo)
        (to_inst, to_rm) = self._cache.getChangesList()
        #print "inst: %s" % to_inst
        #print "rm: %s" % to_rm
        return (to_inst, to_rm)

    def verify_commit_lists(self, inst_list, rm_list):
        """ verify if the selected package can actually be installed """
        res = True
        try:
            for pkg in inst_list:
                if self._cache.has_key(pkg):
                    self._cache[pkg].markInstall()
            for pkg in rm_list:
                if self._cache.has_key(pkg):
                    self._cache[pkg].markDelete()
        except SystemError:
            res = False

        # undo the selections
        self._cache.clear()
        if self._cache._depcache.BrokenCount != 0:
            # undoing the selections was impossible, 
            d = gtk.MessageDialog(parent=self.window_main,
                                  flags=gtk.DIALOG_MODAL,
                                  type=gtk.MESSAGE_ERROR,
                                  buttons=gtk.BUTTONS_CLOSE)
            d.set_markup("<big><b>%s</b></big>\n\n%s" % (
                _("Could not install the selected language support"),
                _("This is perhaps a bug of this application. Please "
                  "file a bug report at "
                  "https://launchpad.net/bugs/bugs/+package/ against "
                  "the 'language-selector' product.")))
            d.set_title=("")
            res = d.run()
            d.destroy()
            # something went pretty bad, re-get a cache
            progress = GtkProgress(self.dialog_progress,
                                   self.progressbar_cache,
                                   self.window_main)
            self._cache = apt.Cache(self._localeinfo, progress)
            progress.hide()
            res = False
        return res

    def commitAllChanges(self):
        """ 
        commit helper, builds the commit lists, verifies it
        
        returns the number of install/removed packages
        """
        self.setSensitive(False)
        # install the new packages (if any)
        (inst_list, rm_list) = self.build_commit_lists()
        if not self.verify_commit_lists(inst_list, rm_list):
            d = gtk.MessageDialog(parent=self.window_main,
                                  flags=gtk.DIALOG_MODAL,
                                  type=gtk.MESSAGE_ERROR,
                                  buttons=gtk.BUTTONS_CLOSE)
            d.set_markup("<big><b>%s</b></big>\n\n%s" % (
                _("Could not install the full language support"),
                _("Usually this is related to an error in your "
                  "software archive or software manager. Check your "
                  "software preferences in the menu \"Adminstration\".")))
            d.set_title("")
            d.run()
            d.destroy()
            self.setSensitive(True)
            return 0
        #print "inst_list: %s " % inst_list
        #print "rm_list: %s " % rm_list
        self.commit(inst_list, rm_list)

        # write input method config
        #self.writeInputMethodConfig()

        # write the system default language
        if self.writeSystemDefaultLang():
            # queue a restart of gdm (if it is runing) to make the new
            # locales usable
            gdmscript = "/etc/init.d/gdm"
            if os.path.exists("/var/run/gdm.pid") and os.path.exists(gdmscript):
                self.runAsRoot(["invoke-rc.d","gdm","reload"])
        self.setSensitive(True)
        return len(inst_list)+len(rm_list)

    # obsolete
    def on_button_ok_clicked(self, widget):
        self.commitAllChanges()
        gtk.main_quit()

    def on_button_apply_clicked(self, widget):
        self.window_installer.hide()
        if self.commitAllChanges() > 0:
            self.updateLanguageView()
        self.updateUserDefaultCombo()
        self.updateSystemDefaultCombo()

    def _run_synaptic(self, lock, inst, rm, id):
        # FIXME: use self.runAsRoot() here
        msg = _("The list of available languages on the "
                "system has been updated.")
        msg = msg.replace("'","\\'")
        cmd = ["gksu", 
               "--desktop", "/usr/share/applications/language-selector.desktop", 
               "--",
               "/usr/sbin/synaptic", "--hide-main-window",
               "--non-interactive", 
               "--parent-window-id", "%s" % (id),
               "--finish-str", msg
               ]
        f = tempfile.NamedTemporaryFile()        
        cmd.append("--set-selections-file")
        cmd.append(f.name)
        for s in inst:
            f.write("%s\tinstall\n" % s)
        for s in rm:
            f.write("%s\tdeinstall\n" % s)
        f.flush()
        subprocess.call(cmd)
        lock.release()

    def _run_synaptic_update(self, lock, id):
        cmd = ["gksu", 
               "--desktop", "/usr/share/applications/language-selector.desktop", 
               "--",
               "/usr/sbin/synaptic", "--hide-main-window",
               "--parent-window-id", "%s" % (id),
               "--non-interactive", "--update-at-startup"
               ]
        subprocess.call(cmd)
        lock.release()

    def update(self):
        " update the package lists via synaptic "
        lock = thread.allocate_lock()
        lock.acquire()
        t = thread.start_new_thread(self._run_synaptic_update,(lock, self.window_main.window.xid))
        while lock.locked():
            while gtk.events_pending():
                gtk.main_iteration()
            time.sleep(0.05)

    def commit(self, inst, rm):
        # unlock here to make sure that lock/unlock are always run
        # pair-wise (and don't explode on errors)
        if len(inst) == 0 and len(rm) == 0:
            return
        lock = thread.allocate_lock()
        lock.acquire()
        t = thread.start_new_thread(self._run_synaptic,(lock,inst,rm, self.window_main.window.xid))
        while lock.locked():
            while gtk.events_pending():
                gtk.main_iteration()
            time.sleep(0.05)

    def on_button_cancel_clicked(self, widget):
        #print "button_cancel"
        self.window_installer.hide()

    def on_delete_event(self, event, data):
        if self.window_main.get_property("sensitive") is False:
            return True
        else:
            gtk.main_quit()

    def verifyInstalledLangPacks(self):
        """ called at the start to inform about possible missing
            langpacks (e.g. gnome/kde langpack transition)
        """
        #print "verifyInstalledLangPacks"
        missing = self.getMissingLangPacks()

        #print "Missing: %s " % missing
        if len(missing) > 0:
            # FIXME: add "details"
            d = gtk.MessageDialog(parent=self.window_main,
                                  flags=gtk.DIALOG_MODAL,
                                  type=gtk.MESSAGE_QUESTION)
            d.set_markup("<big><b>%s</b></big>\n\n%s" % (
                _("The language support is not installed completely"),
                _("Some translations or writing aids available for your "
                  "chosen languages are not installed yet. Do you want "
                  "to install them now?")))
            d.add_buttons(_("_Remind Me Later"), gtk.RESPONSE_NO,
                          _("_Install"), gtk.RESPONSE_YES)
            d.set_default_response(gtk.RESPONSE_YES)
            d.set_title("")
            expander = gtk.Expander(_("Details"))
            scroll = gtk.ScrolledWindow()
            scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            textview = gtk.TextView()
            textview.set_cursor_visible(False)
            textview.set_editable(False)
            buf = textview.get_buffer()
            pkgs = ""
            for pkg in missing:
                pkgs += "%s\n" % pkg
            buf.set_text(pkgs)
            buf.place_cursor(buf.get_start_iter())
            expander.add(scroll)
            scroll.add(textview)
            d.vbox.pack_start(expander)
            expander.show_all()
            res = d.run()
            d.destroy()
            if res == gtk.RESPONSE_YES:
                self.setSensitive(False)
                self.commit(missing, [])
                self.updateLanguageView()
                self.setSensitive(True)

    def updateLanguageView(self):
        #print "updateLanguageView()"
        self._langlist.clear()

        progress = GtkProgress(self.dialog_progress, self.progressbar_cache,
                               self.window_main)
        try:
            self.openCache(progress)
            progress.hide()
        except ExceptionPkgCacheBroken:
            d = gtk.MessageDialog(parent=self.window_main,
                                  flags=gtk.DIALOG_MODAL,
                                  type=gtk.MESSAGE_ERROR,
                                  buttons=gtk.BUTTONS_CLOSE)
            d.set_markup("<big><b>%s</b></big>\n\n%s" % (
                _("Software database is broken"),
                _("It is impossible to install or remove any software. "
                  "Please use the package manager \"Synaptic\" or run "
                  "\"sudo apt-get install -f\" in a terminal to fix "
                  "this issue at first.")))
            d.set_title("")
            d.run()
            d.destroy()
            sys.exit(1)

        languageList = self._cache.getLanguageInformation()
        #print "ll size: ", len(languageList)
        #print "ll type: ", type(languageList)
        for lang in languageList:
            #print "langInfo: %s" % lang
            inconsistent = lang.inconsistent
            #if inconsistent:
            #    print "inconsistent", lang.language
            installed = lang.fullInstalled
            self._langlist.append([_(lang.language), lang])
        self._langlist.set_sort_column_id(LIST_LANG, gtk.SORT_ASCENDING)
        for button in ( 
              "checkbutton_basic_translations",
              "checkbutton_extra_translations",
              "checkbutton_writing_aids",
              "checkbutton_input_methods",
              "checkbutton_extra",
              "checkbutton_fonts"):
            self.block_toggle = True
            getattr(self, button).set_active(False)
            getattr(self, button).set_sensitive(False)
            self.block_toggle = False

    def writeSystemDefaultLang(self):
        combo = self.combobox_system_language
        model = combo.get_model()
        if combo.get_active() < 0:
            return
        (lang, code) = model[combo.get_active()]
        old_code = self._localeinfo.getDefaultLanguage()
        # no changes, nothing to do
        if old_code == code:
            return False
        self.setSystemDefaultLanguage(code)
        return True

    def writeUserDefaultLang(self):
        combo = self.combobox_user_language
        model = combo.get_model()
        if combo.get_active() < 0:
            return
        (lang, code) = model[combo.get_active()]
        temp = self.getUserDefaultLanguage()
        if temp == None:
            old_code = self._localeinfo.getDefaultLanguage()
        else:
            old_code = temp.split("\.")[0]
        # no changes, nothing to do
        if old_code == code:
            return False
        self.setUserDefaultLanguage(code)
        return True

    @blockSignals
    def updateSystemDefaultCombo(self):
        #print "updateSystemDefault()"
        combo = self.combobox_system_language
        cell = combo.get_child().get_cell_renderers()[0]
        # FIXME: use something else than a hardcoded value here
        cell.set_property("wrap-width",300)
        cell.set_property("wrap-mode",pango.WRAP_WORD)
        model = combo.get_model()
        model.clear()

        # find the default
        defaultLangName = None
        defaultLangCode = self.getSystemDefaultLanguage()
        if defaultLangCode:
            defaultLangName = self._localeinfo.translate(defaultLangCode)

        # find out about the other options        
        for (i, locale) in enumerate(self._localeinfo.generated_locales()):
            iter = model.append()
            model.set(iter,
                      COMBO_LANGUAGE,self._localeinfo.translate(locale),
                      COMBO_CODE, locale)
            if (defaultLangName and
                   self._localeinfo.translate(locale) == defaultLangName):
                combo.set_active(i)

        # reset the state of the apply button
        self.combo_syslang_dirty = False
        self.check_status()

    # FIXME: updateUserDefaultCombo and updateSystemDefaultCombo
    #        duplicate too much code
    @blockSignals
    def updateUserDefaultCombo(self):
        #print "updateUserDefault()"
        combo = self.combobox_user_language
        cell = combo.get_child().get_cell_renderers()[0]
        # FIXME: use something else than a hardcoded value here
        cell.set_property("wrap-width",300)
        cell.set_property("wrap-mode",pango.WRAP_WORD)
        model = combo.get_model()
        model.clear()

        # find the default
        defaultLangName = None
        defaultLangCode = self.getUserDefaultLanguage()
        if defaultLangCode == None:
            defaultLangCode = self.getSystemDefaultLanguage()
        if defaultLangCode:
            defaultLangName = self._localeinfo.translate(defaultLangCode)

        # find out about the other options        
        for (i, locale) in enumerate(self._localeinfo.generated_locales()):
            iter = model.append()
            model.set(iter,
                      COMBO_LANGUAGE,self._localeinfo.translate(locale),
                      COMBO_CODE, locale)
            if (defaultLangName and 
                   self._localeinfo.translate(locale) == defaultLangName):
                combo.set_active(i)
            
        # reset the state of the apply button
        self.combo_userlang_dirty = False
        self.check_status()
    
    def on_treeview_languages_row_activated(self, treeview, path, view_column):
        self.on_toggled(None,str(path[0]))
