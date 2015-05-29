# ReleaseNotesViewer.py
#  
#  Copyright (c) 2006 Sebastian Heinlein
#                2007 Canonical
#  
#  Author: Sebastian Heinlein <sebastian.heinlein@web.de>
#          Michael Vogt <michael.vogt@ubuntu.com>
#
#  This modul provides an inheritance of the gtk.TextView that is 
#  aware of http URLs and allows to open them in a browser.
#  It is based on the pygtk-demo "hypertext".
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
import gtk
import pango
import subprocess
import os
from gettext import gettext as _

class ChangelogViewer(gtk.TextView):
    def __init__(self, changelog=None):
        """Init the ChangelogViewer as an Inheritance of the gtk.TextView"""
        # init the parent
        gtk.TextView.__init__(self)
        # global hovering over link state
        self.hovering = False
        self.first = True
        # setup the buffer and signals
        self.set_property("editable", False)
        self.set_cursor_visible(False)
        # set some margin
        self.set_right_margin(4)
        self.set_left_margin(4)
        self.set_pixels_above_lines(4)
        self.buffer = gtk.TextBuffer()
        self.set_buffer(self.buffer)
        self.connect("button-press-event", self.button_press_event)
        self.connect("motion-notify-event", self.motion_notify_event)
        self.connect("visibility-notify-event", self.visibility_notify_event)
        #self.buffer.connect("changed", self.search_links)
        self.buffer.connect_after("insert-text", self.on_insert_text)
        # search for links in the changelog and make them clickable
        if changelog != None:
            self.buffer.set_text(changelog)
            
    def create_context_menu(self, url):
        """Create the context menu to be displayed when links are right clicked"""
        self.menu = gtk.Menu()
        
        # create menu items
        item_grey_link = gtk.MenuItem(url)
        item_grey_link.connect("activate", self.handle_context_menu, "open", url)
        item_seperator = gtk.MenuItem()
        item_open_link = gtk.MenuItem(_("Open Link in Browser"))
        item_open_link.connect("activate", self.handle_context_menu, "open", url)
        item_copy_link = gtk.MenuItem(_("Copy Link to Clipboard"))
        item_copy_link.connect("activate", self.handle_context_menu, "copy", url)
        
        # add menu items
        self.menu.add(item_grey_link)
        self.menu.add(item_seperator)
        self.menu.add(item_open_link)
        self.menu.add(item_copy_link)
        self.menu.show_all()
    
    def handle_context_menu(self, menuitem, action, url):
        """Handle activate event for the links' context menu"""
        if action == "open":
            self.open_url(url)
        if action == "copy":
            cb = gtk.Clipboard()
            cb.set_text(url)
            cb.store()

    def tag_link(self, start, end, url):
        """Apply the tag that marks links to the specified buffer selection"""
        tagged = False
        tags = start.get_tags()
        for tag in tags:
            url = tag.get_data("url")
            if url != "":
                return
        tag = self.buffer.create_tag(None, foreground="blue",
                                     underline=pango.UNDERLINE_SINGLE)
        tag.set_data("url", url)
        self.buffer.apply_tag(tag , start, end)

    def on_insert_text(self, buffer, iter_end, text, *args):
        """Search for http URLs in newly inserted text  
           and tag them accordingly"""

        # some convenient urls
        MALONE = "https://launchpad.net/bugs/"
        DEBIAN = "http://bugs.debian.org/"
        CVE = "http://cve.mitre.org/cgi-bin/cvename.cgi?name="
        # some convinient end-markers
        ws = [" ","\t","\n"]
        brak = [")","]",">"]
        punct = [",","!",":"]
        dot = ["."]+punct
        # search items are start-str, list-of-end-strs, url-prefix
        # a lot of this search is "TEH SUCK"(tm) because of limitations
        # in iter.forward_search()
        # - i.e. no insensitive searching, no regexp
        search_items = [ ("http://", ws+brak+punct, "http://"),
                         ("LP#", ws+brak+dot, MALONE),
                         ("LP: #", ws+brak+dot, MALONE),
                         ("lp: #", ws+brak+dot, MALONE),
                         ("LP:#",  ws+brak+dot, MALONE),
                         ("Malone: #", ws+brak+dot, MALONE),
                         ("Malone:#", ws+brak+dot, MALONE),
                         ("Ubuntu: #", ws+brak+dot, MALONE),
                         ("Ubuntu:#", ws+brak+dot, MALONE),
                         ("Closes: #",ws+brak+dot, DEBIAN),
                         ("Closes:#",ws+brak+dot, DEBIAN),
                         ("closes:#",ws+brak+dot, DEBIAN),
                         ("closes: #",ws+brak+dot, DEBIAN),
                         ("CVE-", ws+brak+dot, CVE),
                       ]
        # init
        iter = buffer.get_iter_at_offset(iter_end.get_offset() - len(text))
        iter_real_end = buffer.get_end_iter()

        # search for the next match in the buffer
        for (start_str, end_list, url_prefix) in search_items:
            while True:
                ret = iter.forward_search(start_str,
                                          gtk.TEXT_SEARCH_VISIBLE_ONLY,
                                          iter_end)
                # if we reach the end break the loop
                if not ret:
                    break
                # get the position of the protocol prefix
                (match_start, match_end) = ret
                match_suffix = match_end.copy()
                match_tmp = match_end.copy()
                while True:
                    # extend the selection to the complete search item
                    if match_tmp.forward_char():
                        text =  match_end.get_text(match_tmp)
                        if text in end_list:
                            break
                    else:
                        break
                    match_end = match_tmp.copy()

                # call the tagging method for the complete URL
                url = url_prefix + match_suffix.get_text(match_end)

                self.tag_link(match_start, match_end, url)
                # set the starting point for the next search
                iter = match_end

    def button_press_event(self, text_view, event):
        """callback for mouse click events"""
        # we only react on left or right mouse clicks
        if event.button != 1 and event.button != 3:
            return False

        # try to get a selection
        try:
            (start, end) = self.buffer.get_selection_bounds()
        except ValueError:
            pass
        else:
            if start.get_offset() != end.get_offset():
                return False

        # get the iter at the mouse position
        (x, y) = self.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET,
                                              int(event.x), int(event.y))
        iter = self.get_iter_at_location(x, y)
        
        # call open_url or menu.popup if an URL is assigned to the iter
        tags = iter.get_tags()
        for tag in tags:
            url = tag.get_data("url")
            if url != None:
                if event.button == 1: 
                    self.open_url(url)
                    break
                if event.button == 3:
                    self.create_context_menu(url)
                    self.menu.popup(None, None, None, event.button, event.time)
                    return True

    def open_url(self, url):
        """Open the specified URL in a browser"""
        # Find an appropiate browser
        if os.path.exists("/usr/bin/exo-open"):
            command = ["exo-open", url]
        elif os.path.exists('/usr/bin/gnome-open'):
            command = ['gnome-open', url]
        else:
            command = ['x-www-browser', url]

        # Avoid to run the browser as user root
        if os.getuid() == 0 and os.environ.has_key('SUDO_USER'):
            command = ['sudo', '-u', os.environ['SUDO_USER']] + command

        subprocess.Popen(command)

    def motion_notify_event(self, text_view, event):
        """callback for the mouse movement event, that calls the
           check_hovering method with the mouse postition coordiantes"""
        x, y = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET,
                                                 int(event.x), int(event.y))
        self.check_hovering(x, y)
        self.window.get_pointer()
        return False
    
    def visibility_notify_event(self, text_view, event):
        """callback if the widgets gets visible (e.g. moves to the foreground)
           that calls the check_hovering method with the mouse position
           coordinates"""
        (wx, wy, mod) = text_view.window.get_pointer()
        (bx, by) = text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET, wx,
                                                     wy)
        self.check_hovering(bx, by)
        return False

    def check_hovering(self, x, y):
        """Check if the mouse is above a tagged link and if yes show
           a hand cursor"""
        _hovering = False
        # get the iter at the mouse position
        iter = self.get_iter_at_location(x, y)
        
        # set _hovering if the iter has the tag "url"
        tags = iter.get_tags()
        for tag in tags:
            url = tag.get_data("url")
            if url != None:
                _hovering = True
                break

        # change the global hovering state
        if _hovering != self.hovering or self.first == True:
            self.first = False
            self.hovering = _hovering
            # Set the appropriate cursur icon
            if self.hovering:
                self.get_window(gtk.TEXT_WINDOW_TEXT).\
                        set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
            else:
                self.get_window(gtk.TEXT_WINDOW_TEXT).\
                        set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
