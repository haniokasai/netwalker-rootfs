#  GTK+ based frontend to software-properties
#
#  Copyright (c) 2004-2007 Canonical Ltd.
#                2004-2005 Michiel Sikkes
#
#  Author: Michiel Sikkes <michiel@eyesopened.nl>
#          Michael Vogt <mvo@debian.org>
#          Sebastian Heinlein <glatzor@ubuntu.com>
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

import apt
import apt_pkg
import tempfile
from gettext import gettext as _
import os
import re
from xml.sax.saxutils import escape

import gtk
import gtk.glade
import gobject

from SimpleGladeApp import SimpleGladeApp
from aptsources.sourceslist import SourceEntry
from DialogAdd import DialogAdd
from DialogMirror import DialogMirror
from DialogEdit import DialogEdit
from DialogCacheOutdated import DialogCacheOutdated
from DialogAddSourcesList import DialogAddSourcesList
from CdromProgress import CdromProgress

import softwareproperties
import softwareproperties.distro
from softwareproperties.SoftwareProperties import SoftwareProperties
import softwareproperties.SoftwareProperties

(LIST_MARKUP, LIST_ENABLED, LIST_ENTRY_OBJ) = range(3)

(
    COLUMN_ACTIVE,
    COLUMN_DESC
) = range(2)

RESPONSE_REPLACE = 1
RESPONSE_ADD = 2

# columns of the source_store
(
    STORE_ACTIVE, 
    STORE_DESCRIPTION, 
    STORE_SOURCE, 
    STORE_SEPARATOR,
    STORE_VISIBLE
) = range(5)

class SoftwarePropertiesGtk(SoftwareProperties,SimpleGladeApp):
  def __init__(self, datadir=None, options=None, file=None, parent=None):
    """ Provide a GTK based graphical user interface to configure
        the used software repositories, corresponding authentication keys
        and update automation """
    SoftwareProperties.__init__(self, options=options, datadir=datadir)
    gtk.window_set_default_icon_name("software-properties")

    SimpleGladeApp.__init__(self, datadir+"glade/main.glade",
                            None, domain="software-properties")

    if parent:
      self.window_main.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
      self.window_main.show()
      self.window_main.set_transient_for(parent)

    # If externally called, reparent to external application.
    self.options = options
    if options and options.toplevel != None:
      self.window_main.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
      self.window_main.show()
      toplevel = gtk.gdk.window_foreign_new(int(options.toplevel))
      if (toplevel):
      	self.window_main.window.set_transient_for(toplevel)
    if options and options.open_tab:
      self.notebook_main.set_current_page(int(options.open_tab))

    # Show what we have early
    self.window_main.show()

    # used to store the handlers of callbacks
    self.handlers = []

    # Put some life into the user interface:
    self.init_auto_update()
    self.show_auto_update_level()
    # Setup the key list
    self.init_keys()
    self.show_keys()
    # Setup the ISV sources list
    self.init_isv_sources()
    self.show_isv_sources()
    # Setup and show the distro elements
    self.show_distro()

    # Show the import/replace sources.list dialog if a file different
    # to the default sources.list was specified 
    # NOTE: If the file path points to the default sources.list the user
    #       perhaps assumed that s-p would act like a normal editor.
    #       We have got some bug reports from users calling
    #       "sudo software-properties-gtk /etc/apt/sources.list" from the
    #       command line.
    if file != None and \
       os.path.abspath(file) !=  "%s%s" % (apt_pkg.Config.FindDir("Dir::Etc"),
                                           apt_pkg.Config.Find("Dir::Etc::sourcelist")):
        self.open_file(file)

  def init_auto_update(self):
    """ Set up the widgets that allow to configure the update automation """
    # this maps the key (combo-box-index) to the auto-update-interval value
    # where (-1) means, no key
    self.combobox_interval_mapping = { 0 : 1,
                                       1 : 2,
                                       2 : 7,
                                       3 : 14 }
    self.combobox_update_interval.set_active(0)

    #update_days = apt_pkg.Config.FindI(softwareproperties.CONF_MAP["autoupdate"])

    self.combobox_update_interval.append_text(_("Daily"))
    self.combobox_update_interval.append_text(_("Every two days"))
    self.combobox_update_interval.append_text(_("Weekly"))
    self.combobox_update_interval.append_text(_("Every two weeks"))

    model_check_interval = gtk.ListStore(gobject.TYPE_STRING,
                                         gobject.TYPE_INT)
    update_days = self.get_update_interval()

    # If a custom period is defined add a corresponding entry
    if not update_days in self.combobox_interval_mapping.values():
        if update_days > 0:
            self.combobox_update_interval.append_text(_("Every %s days") 
                                                      % update_days)
            self.combobox_interval_mapping[4] = update_days
    
    for key in self.combobox_interval_mapping:
      if self.combobox_interval_mapping[key] == update_days:
        self.combobox_update_interval.set_active(key)
        break

    if update_days >= 1:
      self.checkbutton_auto_update.set_active(True)
      self.combobox_update_interval.set_sensitive(True)
      self.vbox_auto_updates.set_sensitive(True)
    else:
      self.checkbutton_auto_update.set_active(False)
      self.combobox_update_interval.set_sensitive(False)
      self.vbox_auto_updates.set_sensitive(False)

    self.handlers.append(
        (self.checkbutton_auto_update,
         self.checkbutton_auto_update.connect("toggled", 
                                     self.on_auto_update_toggled)))
    self.handlers.append(
        (self.combobox_update_interval,
         self.combobox_update_interval.connect("changed", 
                                     self.on_combobox_update_interval_changed)))
    self.handlers.append(
        (self.radiobutton_updates_download,
         self.radiobutton_updates_download.connect("toggled", 
                                     self.set_update_automation_level,
                                     softwareproperties.UPDATE_DOWNLOAD)))
    self.handlers.append(
        (self.radiobutton_updates_notify,
         self.radiobutton_updates_notify.connect("toggled", 
                                     self.set_update_automation_level,
                                     softwareproperties.UPDATE_NOTIFY)))

  def show_auto_update_level(self):
    """Represent the level of update automation in the user interface"""
    level = self.get_update_automation_level()
    self.block_handlers()
    if level == None or level == softwareproperties.UPDATE_INST_SEC:
        self.radiobutton_updates_download.set_inconsistent(True)
        self.radiobutton_updates_notify.set_inconsistent(True)
    else:
        self.radiobutton_updates_download.set_inconsistent(False)
        self.radiobutton_updates_notify.set_inconsistent(False)
    if level == softwareproperties.UPDATE_MANUAL or \
       level == softwareproperties.UPDATE_NOTIFY:
        self.radiobutton_updates_notify.set_active(True)
    elif level == softwareproperties.UPDATE_DOWNLOAD:
        self.radiobutton_updates_download.set_active(True)
    # Unblock the toggle handlers
    self.unblock_handlers()

  def block_handlers(self):
    for (widget, handler) in self.handlers:
        widget.handler_block(handler)
 
  def unblock_handlers(self):
    for (widget, handler) in self.handlers:
        widget.handler_unblock(handler)

  def show_distro(self):
    """Fill the distro user interface with life"""
    # Output a lot of debug stuff
    if self.options.debug == True or self.options.massive_debug == True:
        print "ENABLED COMPS: %s" % self.distro.enabled_comps
        print "INTERNET COMPS: %s" % self.distro.download_comps
        print "MAIN SOURCES"
        for source in self.distro.main_sources:
            self.print_source_entry(source)
        print "CHILD SOURCES"
        for source in self.distro.child_sources:
            self.print_source_entry(source)
        print "CDROM SOURCES"
        for source in self.distro.cdrom_sources:
            self.print_source_entry(source)
        print "SOURCE CODE SOURCES"
        for source in self.distro.source_code_sources:
            self.print_source_entry(source)
        print "DISABLED SOURCES"
        for source in self.distro.disabled_sources:
            self.print_source_entry(source)
        print "ISV"
        for source in self.sourceslist_visible:
            self.print_source_entry(source)

  def set_update_automation_level(self, widget, state):
    '''Call the backend to set the update automation level to the given 
       value'''
    if widget.get_active() == True:
        self.vbox_auto_updates.foreach(lambda b: b.set_inconsistent(False))
        SoftwareProperties.set_update_automation_level(self, state)
    self.set_modified_config()

  def is_row_separator(self, model, iter, column=0):
    ''' Check if a given row is a separator '''
    return model.get_value(iter, column)

  def on_combobox_release_upgrades_changed(self, combobox):
    """ set the release upgrades policy """
    #print "on_combobox_release_upgrades_changed()"
    i = combobox.get_active()
    self.set_release_upgrades_policy(i)

  def on_combobox_server_changed(self, combobox):
    """
    Replace the servers used by the main and update sources with
    the selected one
    """
    if combobox.get_active() == self.active_server:
        return
    server_store = combobox.get_model()
    iter = combobox.get_active_iter()
    uri = server_store.get_value(iter, 1)
    name = server_store.get_value(iter, 0)
    if name == _("Other..."):
        dialog = DialogMirror(self.window_main, 
                              self.datadir,
                              self.distro,
                              self.custom_mirrors)
        res = dialog.run()
        if res != None:
            self.distro.change_server(res)
            self.set_modified_sourceslist()
        else:
            combobox.set_active(self.active_server)
    elif uri != None and len(self.distro.used_servers) > 0:
        self.active_server = combobox.get_active()
        self.distro.change_server(uri)
        self.distro.default_server = uri
        self.set_modified_sourceslist()
    else:
        self.distro.default_server = uri

  def on_component_toggled(self, checkbutton, comp):
    """
    Sync the components of all main sources (excluding cdroms),
    child sources and source code sources
    """
    if checkbutton.get_active() == True:
        self.enable_component(comp)
    else:
        self.disable_component(comp)
    self.set_modified_sourceslist()

  def on_checkbutton_child_toggled(self, checkbutton, template):
    """
    Enable or disable a child repo of the distribution main repository
    """
    if checkbutton.get_active() == False:
        self.disable_child_source(template)
    else:
        self.enable_child_source(template)
          
  def on_checkbutton_source_code_toggled(self, checkbutton):
    """ Disable or enable the source code for all sources """
    if checkbutton.get_active() == True:
        self.enable_source_code_sources()
    else:
        self.disable_source_code_sources()

  def on_checkbutton_popcon_toggled(self, widget):
    """ The user clicked on the popcon paritipcation button """
    self.set_popcon_pariticipation(widget.get_active())

  def open_file(self, file):
    """Show a confirmation for adding the channels of the specified file"""
    dialog = DialogAddSourcesList(self.window_main,
                                  self.sourceslist,
                                  self.render_source,
                                  self.get_comparable,
                                  self.datadir,
                                  file)
    (res, new_sources) = dialog.run()
    if res == RESPONSE_REPLACE:
        self.sourceslist.list = []
    if res in (RESPONSE_ADD, RESPONSE_REPLACE):
        for source in new_sources:
            self.sourceslist.add(source.type,
                                 source.uri,
                                 source.dist,
                                 source.comps,
                                 source.comment)
        self.set_modified_sourceslist()

  def on_sources_drag_data_received(self, widget, context, x, y,
                                     selection, target_type, timestamp):
      """Extract the dropped file pathes and open the first file, only"""
      uri = selection.data.strip()
      uri_splitted = uri.split()
      if len(uri_splitted)>0:
          self.open_file(uri_splitted[0])

  def hide(self):
    self.window_main.hide()
    
  def init_isv_sources(self):
    """
    Read all valid sources into our ListStore
    """
    # STORE_ACTIVE - is the source enabled or disabled
    # STORE_DESCRIPTION - description of the source entry
    # STORE_SOURCE - the source entry object
    # STORE_SEPARATOR - if the entry is a separator
    # STORE_VISIBLE - if the entry is shown or hidden
    self.source_store = gtk.ListStore(gobject.TYPE_BOOLEAN, 
                                      gobject.TYPE_STRING,
                                      gobject.TYPE_PYOBJECT,
                                      gobject.TYPE_BOOLEAN,
                                      gobject.TYPE_BOOLEAN)
    self.treeview_sources.set_model(self.source_store)
    self.treeview_sources.set_row_separator_func(self.is_separator,
                                                 STORE_SEPARATOR)

    cell_desc = gtk.CellRendererText()
    cell_desc.set_property("xpad", 2)
    cell_desc.set_property("ypad", 2)
    col_desc = gtk.TreeViewColumn(_("Software Sources"), cell_desc,
                                  markup=COLUMN_DESC)
    col_desc.set_max_width(1000)

    cell_toggle = gtk.CellRendererToggle()
    cell_toggle.set_property("xpad", 2)
    cell_toggle.set_property("ypad", 2)
    self.handlers.append([cell_toggle,
                          cell_toggle.connect('toggled', 
                                              self.on_isv_source_toggled, 
                                              self.source_store)])
    col_active = gtk.TreeViewColumn(_("Active"), cell_toggle,
                                    active=COLUMN_ACTIVE)

    self.treeview_sources.append_column(col_active)
    self.treeview_sources.append_column(col_desc)
    # drag and drop support for sources.list
    self.treeview_sources.drag_dest_set(gtk.DEST_DEFAULT_ALL, \
                                        [('text/uri-list',0, 0)], \
                                        gtk.gdk.ACTION_COPY)
    self.treeview_sources.connect("drag_data_received",\
                                  self.on_sources_drag_data_received)

  def on_isv_source_activate(self, treeview, path, column):
    """Open the edit dialog if a channel was double clicked"""
    self.on_edit_clicked(treeview)

  def on_treeview_sources_cursor_changed(self, treeview):
    """Enable the buttons remove and edit if a channel is selected"""
    sel = self.treeview_sources.get_selection()
    (model, iter) = sel.get_selected()
    if iter:
        self.button_edit.set_sensitive(True)
        self.button_remove.set_sensitive(True)
    else:
        self.button_edit.set_sensitive(False)
        self.button_remove.set_sensitive(False)
  
  def on_isv_source_toggled(self, cell_toggle, path, store):
    """Enable or disable the selected channel"""
    #FIXME cdroms need to disable the comps in the childs and sources
    iter = store.get_iter((int(path),))
    source_entry = store.get_value(iter, STORE_SOURCE) 
    self.toggle_source_use(source_entry)

  def init_keys(self):
    """Setup the user interface parts needed for the key handling"""
    self.keys_store = gtk.ListStore(str)
    self.treeview2.set_model(self.keys_store)
    tr = gtk.CellRendererText()
    keys_col = gtk.TreeViewColumn("Key", tr, text=0)
    self.treeview2.append_column(keys_col)

  #FIXME revert automation settings too
  def on_button_revert_clicked(self, button):
    """Restore the source list from the startup of the dialog"""
    SoftwareProperties.revert(self)
    self.set_modified_sourceslist()
    self.show_auto_update_level()
    self.button_revert.set_sensitive(False)
    self.modified_sourceslist = False

  def set_modified_config(self):
    """The config was changed and now needs to be saved and reloaded"""
    SoftwareProperties.set_modified_config(self)
    self.button_revert.set_sensitive(True)

  def set_modified_sourceslist(self):
    """The sources list was changed and now needs to be saved and reloaded"""
    SoftwareProperties.set_modified_sourceslist(self)
    self.show_distro()
    self.show_isv_sources()
    self.button_revert.set_sensitive(True)

  def show_isv_sources(self):
    """ Show the repositories of independent software vendors in the
        third-party software tree view """
    self.source_store.clear()

    for source in self.get_isv_sources():
        contents = self.render_source(source)
        self.source_store.append([not source.disabled, contents,
                                  source, False, True])

    (path_x, path_y) = self.treeview_sources.get_cursor()
    if len(self.source_store) < 1 or path_x <0:
        self.button_remove.set_sensitive(False)
        self.button_edit.set_sensitive(False)

  def is_separator(self, model, iter, column):
    """ Return true if the selected row is a separator """
    try:
      return model.get_value(iter, column)
    except Exception, e:
      print "is_seperator returned '%s' " % e
      return False
      
  def show_keys(self):
    self.keys_store.clear()
    for key in self.apt_key.list():
      self.keys_store.append([key])

  def on_combobox_update_interval_changed(self, widget):
    """Set the update automation interval to the chosen one"""
    i = self.combobox_update_interval.get_active()
    if i != -1:
        value = self.combobox_interval_mapping[i]
        self.set_update_interval(value)

  def on_auto_update_toggled(self, widget):
    """Enable or disable automatic updates and modify the user interface
       accordingly"""
    if self.checkbutton_auto_update.get_active():
      self.combobox_update_interval.set_sensitive(True)
      self.vbox_auto_updates.set_sensitive(True)
      # if no frequency was specified use daily
      i = self.combobox_update_interval.get_active()
      if i == -1:
          i = 0
          self.combobox_update_interval.set_active(i)
      value = self.combobox_interval_mapping[i]
      # A little hack to re-set the former selected update automation level
      self.vbox_auto_updates.foreach(lambda b: b.toggled())
    else:
      self.combobox_update_interval.set_sensitive(False)
      self.vbox_auto_updates.set_sensitive(False)
      SoftwareProperties.set_update_automation_level(self, None)
      value = 0
    self.set_update_interval(str(value))

  def on_add_clicked(self, widget):
    """Show a dialog that allows to enter the apt line of a to be used repo"""
    dialog = DialogAdd(self.window_main, self.sourceslist,
                       self.datadir, self.distro)
    line = dialog.run()
    if line != None:
      self.add_source_from_line(line)
      self.set_modified_sourceslist()
      
  def on_edit_clicked(self, widget):
    """Show a dialog to edit an ISV source"""
    sel = self.treeview_sources.get_selection()
    (model, iter) = sel.get_selected()
    if not iter:
      return
    source_entry = model.get_value(iter, LIST_ENTRY_OBJ)
    dialog = DialogEdit(self.window_main, self.sourceslist,
                        source_entry, self.datadir)
    if dialog.run() == gtk.RESPONSE_OK:
        self.set_modified_sourceslist()

  # FIXME:outstanding from merge
  def on_isv_source_activated(self, treeview, path, column):
     """Open the edit dialog if a channel was double clicked"""
     # check if the channel can be edited
     if self.button_edit.get_property("sensitive") == True:
         self.on_edit_clicked(treeview)

  # FIXME:outstanding from merge
  def on_treeview_sources_cursor_changed(self, treeview):
    """set the sensitiveness of the edit and remove button
       corresponding to the selected channel"""
    sel = self.treeview_sources.get_selection()
    (model, iter) = sel.get_selected()
    if not iter:
        # No channel is selected, so disable edit and remove
        self.button_edit.set_sensitive(False)
        self.button_remove.set_sensitive(False)
        return
    # allow to remove the selected channel
    self.button_remove.set_sensitive(True)
    # disable editing of cdrom sources
    source_entry = model.get_value(iter, LIST_ENTRY_OBJ)
    if source_entry.uri.startswith("cdrom:"):
        self.button_edit.set_sensitive(False)
    else:
        self.button_edit.set_sensitive(True)

  def on_remove_clicked(self, widget):
    """Remove the selected source"""
    model = self.treeview_sources.get_model()
    (path, column) = self.treeview_sources.get_cursor()
    iter = model.get_iter(path)
    if iter:
      self.remove_source(model.get_value(iter, LIST_ENTRY_OBJ))
      self.set_modified_sourceslist()

  def add_key_clicked(self, widget):
    """Provide a file chooser that allows to add the gnupg of a trusted
       software vendor"""
    chooser = gtk.FileChooserDialog(title=_("Import key"),
                                    parent=self.window_main,
                                    buttons=(gtk.STOCK_CANCEL,
                                             gtk.RESPONSE_REJECT,
                                             gtk.STOCK_OK,gtk.RESPONSE_ACCEPT))
    res = chooser.run()
    chooser.hide()
    if res == gtk.RESPONSE_ACCEPT:
      if not self.add_key(chooser.get_filename()):
        error(self.window_main,
              _("Error importing selected file"),
              _("The selected file may not be a GPG key file " \
                "or it might be corrupt."))
      self.show_keys()

  def remove_key_clicked(self, widget):
    """Remove a trusted software vendor key"""
    selection = self.treeview2.get_selection()
    (model,a_iter) = selection.get_selected()
    if a_iter == None:
        return
    key = model.get_value(a_iter,0)
    if not self.remove_key(key[:8]):
      error(self.main,
        _("Error removing the key"),
        _("The key you selected could not be removed. "
          "Please report this as a bug."))
    self.show_keys()

  def on_restore_clicked(self, widget):
    """Restore the original keys"""
    self.apt_key.update()
    self.show_keys()

  def on_delete_event(self, widget, args):
    """Close the window if requested"""
    self.on_close_button(widget)

  def on_close_button(self, widget):
    """Show a dialog that a reload of the channel information is required
       only if there is no parent defined"""
    if (self.modified_sourceslist == True and
        self.options.no_update == False):
        d = DialogCacheOutdated(self.window_main,
                                self.datadir)
        res = d.run()
    self.quit()

  def on_button_add_cdrom_clicked(self, widget):
    '''Show a dialog that allows to add a repository located on a CDROM
       or DVD'''
    # testing
    #apt_pkg.Config.Set("APT::CDROM::Rename","true")

    saved_entry = apt_pkg.Config.Find("Dir::Etc::sourcelist")
    tmp = tempfile.NamedTemporaryFile()
    apt_pkg.Config.Set("Dir::Etc::sourcelist",tmp.name)
    progress = CdromProgress(self.datadir,self.window_main)
    cdrom = apt_pkg.GetCdrom()
    # if nothing was found just return
    try:
      res = cdrom.Add(progress)
    except SystemError, msg:
      #print "aiiiieeee, exception from cdrom.Add() [%s]" % msg
      progress.close()
      dialog = gtk.MessageDialog(parent=self.window_main,
                                 flags=gtk.DIALOG_MODAL,
                                 type=gtk.MESSAGE_ERROR,
                                 buttons=gtk.BUTTONS_OK,
                                 message_format=None)
      dialog.set_markup(_("<big><b>Error scanning the CD</b></big>\n\n%s")%msg)
      res = dialog.run()
      dialog.destroy()
      return
    apt_pkg.Config.Set("Dir::Etc::sourcelist",saved_entry)
    if res == False:
      progress.close()
      return
    # read tmp file with source name (read only last line)
    line = ""
    for x in open(tmp.name):
      line = x
    if line != "":
      full_path = "%s%s" % (apt_pkg.Config.FindDir("Dir::Etc"),saved_entry)
      self.sourceslist.list.append(SourceEntry(line,full_path))
      self.set_modified_sourceslist()
