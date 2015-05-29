# dialog_add.py.in - dialog to add a new repository
#  
#  Copyright (c) 2006 FSF Europe
#              
#  Authors: 
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
import threading
import string
import re
from random import randint

import dialogs
from softwareproperties.MirrorTest import MirrorTest

testing = threading.Event()

(COLUMN_PROTO, COLUMN_DIR) = range(2)
(COLUMN_URI, COLUMN_SEPARATOR, COLUMN_CUSTOM, COLUMN_MIRROR) = range(4)

from softwareproperties.CountryInformation import CountryInformation

def threaded(f):
    ''' Thanks to Ross Burton for this piece of code '''
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=f, args=args, kwargs=kwargs)
        t.setDaemon(True)
        t.start()
    wrapper.__name__ = f.__name__
    return wrapper

def sort_mirrors(model, iter1, iter2, data=None):
      ''' sort function for the mirror list:
           - at first show all custom urls
           - secondly the separator
           - third the official mirrors. if available
             sort the countries '''
      #FIXME: cmp seems to prefer ASCI chars
      (url1, sep1, custom1) = model.get(iter1, 0,1,2)
      (url2, sep2, custom2) = model.get(iter2, 0,1,2)
      if custom1 and custom2:
          return cmp(url1,url2)
      elif custom1:
          return -1
      elif custom2:
          return 1
      if sep1:
          return -1
      elif sep2:
          return 1
      return cmp(url1,url2)

class DialogMirror:
  def __init__(self, parent, datadir, distro, custom_mirrors):
    """
    Initialize the dialog that allows to choose a custom or official mirror
    """
    def is_separator(model, iter, data=None):
        return model.get_value(iter, COLUMN_SEPARATOR)

    self.custom_mirrors = custom_mirrors

    self.country_info = CountryInformation()

    self.gladexml = gtk.glade.XML("%s/glade/dialogs.glade" %\
                                  datadir)
    self.gladexml.signal_autoconnect(self)
    self.dialog = self.gladexml.get_widget("dialog_mirror")
    self.dialog.set_transient_for(parent)
    self.dialog_test = self.gladexml.get_widget("dialog_mirror_test")
    self.dialog_test.set_transient_for(self.dialog)
    self.distro = distro
    self.treeview = self.gladexml.get_widget("treeview_mirrors")
    self.button_edit = self.gladexml.get_widget("button_mirror_edit")
    self.button_remove = self.gladexml.get_widget("button_mirror_remove")
    self.button_choose = self.gladexml.get_widget("button_mirror_choose")
    self.button_cancel = self.gladexml.get_widget("button_test_cancel")
    self.label_test = self.gladexml.get_widget("label_test_mirror")
    self.progressbar_test = self.gladexml.get_widget("progressbar_test_mirror")
    self.combobox = self.gladexml.get_widget("combobox_mirror_proto")
    self.progress = self.gladexml.get_widget("progressbar_test_mirror")
    self.label_action = self.gladexml.get_widget("label_test_mirror")

    # store each proto and its dir
    model_proto = gtk.ListStore(gobject.TYPE_STRING,
                                gobject.TYPE_STRING)
    self.combobox.set_model(model_proto)

    self.model = gtk.TreeStore(gobject.TYPE_STRING,  # COLUMN_URI
                               gobject.TYPE_BOOLEAN, # COLUMN_SEPARATOR
                               gobject.TYPE_BOOLEAN, # COLUMN_CUSTOM
                               gobject.TYPE_PYOBJECT)# COLUMN_MIRROR
    self.treeview.set_row_separator_func(is_separator)
    self.model_sort = gtk.TreeModelSort(self.model)
    self.model_sort.set_default_sort_func(sort_mirrors)

    self.distro = distro

    self.treeview.set_model(self.model_sort)
    # the cell renderer for the mirror uri
    self.renderer_mirror = gtk.CellRendererText()
    self.renderer_mirror.connect('edited', 
                                 self.on_edited_custom_mirror, 
                                 self.model)
    # the visible column that holds the mirror uris
    self.column_mirror = gtk.TreeViewColumn("URI", 
                                            self.renderer_mirror, 
                                            text=COLUMN_URI)
    self.treeview.append_column(self.column_mirror)

    # used to find the corresponding iter of a location
    map_loc = {}
    patriot = None
    model = self.treeview.get_model().get_model()
    # at first add all custom mirrors and a separator
    if len(self.custom_mirrors) > 0:
        for mirror in self.custom_mirrors:
            model.append(None, [mirror, False, True, None])
            self.column_mirror.add_attribute(self.renderer_mirror, 
                                             "editable", 
                                             COLUMN_CUSTOM)
        model.append(None, [None, True, False, None])
    # secondly add all official mirrors
    for hostname in self.distro.source_template.mirror_set.keys():
        mirror = self.distro.source_template.mirror_set[hostname]
        if map_loc.has_key(mirror.location):
            model.append(map_loc[mirror.location],
                         [hostname, False, False, mirror])
        elif mirror.location != None:
            parent = model.append(None, 
                                  [self.country_info.get_country_name(mirror.location), False, False, None])
            if mirror.location == self.country_info.code and patriot == None:
                patriot = parent
            model.append(parent, [hostname, False, False, mirror]),
            map_loc[mirror.location] = parent
        else:
            model.append(None, [hostname, False, False, mirror])
    # Scroll to the local mirror set
    if patriot != None:
        path_sort = self.model_sort.get_path(self.model_sort.convert_child_iter_to_iter(None, patriot))
        self.treeview.expand_row(path_sort, False)
        self.treeview.set_cursor(path_sort)
        self.treeview.scroll_to_cell(path_sort, use_align=True, row_align=0.5)

  def on_edited_custom_mirror(self, cell, path, new_text, model):
    ''' Check if the new mirror uri is faild, if yes change it, if not
        remove the mirror from the list '''
    iter = model.get_iter(path)
    iter_next = model.iter_next(iter)
    if new_text != "":
        model.set_value(iter, COLUMN_URI, new_text)
        # Add a separator if the next mirror is a not a separator or 
        # a custom one
        if iter_next != None and not \
           (model.get_value(iter_next, COLUMN_SEPARATOR) or \
            model.get_value(iter_next, COLUMN_CUSTOM)):
            model.insert(1, [None, True, False])
        self.button_choose.set_sensitive(self.is_valid_mirror(new_text))
    else:
        model.remove(iter)
        # Remove the separator if this was the last custom mirror
        if model.get_value(model.get_iter_first(), COLUMN_SEPARATOR):
            model.remove(model.get_iter_first())
        self.treeview.set_cursor((0,))
    return

  def is_valid_mirror(self, uri):
    ''' Check if a given uri is a vaild one '''
    if uri == None:
        return False
    elif re.match("^((ftp)|(http)|(file)|(rsync)|(https))://([a-z]|[A-Z]|[0-9]|:|/|\.|~)+$", uri) == None:
        return False
    else:
        return True

  def on_treeview_mirrors_cursor_changed(self, treeview, data=None):
    ''' Check if the currently selected row in the mirror list
        contains a mirror and or is editable '''
    (row, column) = treeview.get_cursor()
    if row == None:
        self.button_remove.set_sensitive(False)
        self.button_edit.set_sensitive(False)
        self.button_choose.set_sensitive(False)
        return
    model = treeview.get_model()
    iter = model.get_iter(row)
    # Update the list of available protocolls
    mirror = model.get_value(iter, COLUMN_MIRROR)
    model_protos = self.combobox.get_model()
    model_protos.clear()
    if mirror != None:
        self.combobox.set_sensitive(True)
        seen_protos = []
        for repo in mirror.repositories:
            # Only add a repository for a protocoll once
            if repo.proto in seen_protos:
                continue
            seen_protos.append(repo.proto)
            model_protos.append(repo.get_info())
        self.combobox.set_active(0)
        self.button_choose.set_sensitive(True)
    else:
        # Allow to edit and remove custom mirrors
        self.button_remove.set_sensitive(model.get_value(iter, COLUMN_CUSTOM))
        self.button_edit.set_sensitive(model.get_value(iter, COLUMN_CUSTOM))
        self.button_choose.set_sensitive(self.is_valid_mirror(model.get_value(iter, COLUMN_URI)))
        self.combobox.set_sensitive(False)

  def on_button_mirror_remove_clicked(self, button, data=None):
    ''' Remove the currently selected mirror '''
    path, column = self.treeview.get_cursor()
    iter = self.treeview.get_model().get_iter(path)
    model = self.treeview.get_model().get_model()
    model.remove(iter)
    # Remove the separator if this was the last custom mirror
    if model.get_value(model.get_iter_first(), COLUMN_SEPARATOR):
        model.remove(model.get_iter_first())
    self.treeview.set_cursor((0,))

  def on_button_mirror_add_clicked(self, button, data=None):
    ''' Add a new mirror at the beginning of the list and start
        editing '''
    model = self.treeview.get_model().get_model()
    model.append(None, [_("New mirror"), False, True, None])
    self.treeview.grab_focus()
    self.treeview.set_cursor((0,),
                             focus_column=self.column_mirror, 
                             start_editing=True)

  def on_button_mirror_edit_clicked(self, button, data=None):
    ''' Grab the focus and start editing the currently selected mirror '''
    path, column = self.treeview.get_cursor()
    self.treeview.grab_focus()
    self.treeview.set_cursor(path, focus_column=column, start_editing=True)

  def on_dialog_mirror_test_delete_event(self, dialog, event, data=None):
    ''' If anybody wants to close the dialog, stop the test before '''
    self.on_button_cancel_test_clicked(None)
    return True

  def run(self):
    ''' Run the chooser dialog and return the chosen mirror or None '''
    res = self.dialog.run()
    self.dialog.hide()

    (row, column) = self.treeview.get_cursor()
    model = self.treeview.get_model()
    iter = model.get_iter(row)
    mirror = model.get_value(iter, COLUMN_MIRROR)

    # FIXME: we should also return the list of custom servers
    if res == gtk.RESPONSE_OK:
        if mirror == None:
            # Return the URL of the selected custom mirror
            return model.get_value(iter, COLUMN_URI)
        else:
            # Return an URL created from the hostname and the selected
            # repository
            model_proto = self.combobox.get_model()
            iter_proto = model_proto.get_iter(self.combobox.get_active())
            proto = model_proto.get_value(iter_proto, COLUMN_PROTO)
            dir = model_proto.get_value(iter_proto, COLUMN_DIR)
            return "%s://%s/%s" % (proto, mirror.hostname, dir)
    else:
        return None

  @threaded
  def on_button_test_clicked(self, button, data=None):
    ''' Perform a test to find the best mirror and select it 
        afterwards in the treeview '''
    class MirrorTestGtk(MirrorTest):
        def __init__(self, mirrors, test_file, running, progressbar, label):
            MirrorTest.__init__(self, mirrors, test_file, running)
            self.progress = progressbar
            self.label = label
        def report_action(self, text):
            gtk.gdk.threads_enter()
            self.label.set_label(str("<i>%s</i>" % text))
            gtk.gdk.threads_leave()
        def report_progress(self, current, max, borders=(0,1), mod=(0,0)):
            gtk.gdk.threads_enter()
            self.progress.set_text(_("Completed %s of %s tests") % \
                                   (current + mod[0], max + mod[1]))
            frac = borders[0] + (borders[1] - borders[0]) / max * current
            self.progress.set_fraction(frac)
            gtk.gdk.threads_leave()
        def run_full_test(self):
            # Determinate the 5 top ping servers
            results_ping = self.run_ping_test(max=5,
                                              borders=(0, 0.5),
                                              mod=(0,7))
            # Add two random mirrors to the download test
            size = len(self.mirrors)
	    if size > 2:
	            results_ping.append([0, 0, self.mirrors[randint(1,size-1)]])
        	    results_ping.append([0, 0, self.mirrors[randint(1,size-1)]])
            results = self.run_download_test(map(lambda r: r[2], results_ping),
                                             borders=(0.5, 1),
                                             mod=(MirrorTest.todo,
                                                  MirrorTest.todo))
            for (t, h) in results:
                print "mirror: %s - time: %s" % (h.hostname, t)
            if len(results) == 0:
                return None
            else:
                return results[0][1].hostname

    gtk.gdk.threads_enter()
    self.button_cancel.set_sensitive(True)
    self.dialog_test.show()
    gtk.gdk.threads_leave()
    self.running = threading.Event()
    self.running.set()
    pipe = os.popen("dpkg --print-architecture")
    arch = pipe.read().strip()
    test_file = "dists/%s/%s/binary-%s/Packages.gz" % \
                 (self.distro.source_template.name,
                  self.distro.source_template.components[0].name,
                  arch)
    test = MirrorTestGtk(self.distro.source_template.mirror_set.values(), 
                         test_file,
                         self.running,
                         self.progress,
                         self.label_action)
    test.start()
    rocker = test.run_full_test()
    gtk.gdk.threads_enter()
    testing.clear()
    self.dialog_test.hide()
    # Select the mirror in the list or show an error dialog
    if rocker != None:
        self.model_sort.foreach(self.select_mirror, rocker)
    else:
        dialogs.show_error_dialog(self.dialog, 
                                  _("No suitable download server was found"),
                                  _("Please check your Internet connection."))
    gtk.gdk.threads_leave()

  def select_mirror(self, model, path, iter, mirror):
    """Select and expand the path to a matching mirror in the list"""
    if model.get_value(iter, COLUMN_URI) == mirror:
        self.treeview.expand_to_path(path)
        self.treeview.set_cursor(path)
        self.treeview.scroll_to_cell(path, use_align=True, row_align=0.5)
        self.treeview.grab_focus()
        # breaks foreach
        return True

  def on_button_cancel_test_clicked(self, button):
    ''' Abort the mirror performance test '''
    self.running.clear()
    self.label_test.set_label("<i>%s</i>" % _("Canceling..."))
    self.button_cancel.set_sensitive(False)
    self.progressbar_test.set_fraction(1)
