#!/usr/bin/python
# coding=UTF-8
#
# Copyright (C) 2008 Tim-Philipp Müller <tim.muller@collabora.co.uk>
# Copyright (C) 2008 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA.
#
# The Totem project hereby grant permission for non-gpl compatible GStreamer
# plugins to be used and distributed together with GStreamer and Totem. This
# permission are above and beyond the permissions granted by the GPL license
# Totem is covered by.
#
# See license_change file for details.

import gobject
gobject.threads_init()
import pygst
pygst.require ("0.10")
import gst

import totem
import gtk
import gconf
import time
import os
from contentview import ContentView

class BBCViewer(totem.Plugin):
	def __init__ (self):
		totem.Plugin.__init__ (self)
		self.loaded_content = False

	def mapped (self, contentview):
		gst.log('mapped')
		if not self.loaded_content:
		  self.view.load()
		  self.loaded_content = True

	def activate (self, totem_object):
		self.gconf_client = gconf.client_get_default ()
		self.totem = totem_object
                self.view = ContentView()
		self.view.connect('play-episode', self.playEpisode)
		vbox = gtk.VBox()
                scrollwin = gtk.ScrolledWindow()
                scrollwin.add(self.view)
                scrollwin.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
                scrollwin.set_shadow_type(gtk.SHADOW_ETCHED_IN)
                vbox.pack_start(scrollwin, True, True)
		vbox.show_all ()
		totem_object.add_sidebar_page ("bbc", _("BBC"), vbox)
		# connect to 'map' only after adding the sidebar page
		self.view.connect('map', self.mapped)
		gst.log('activated')

	def deactivate (self, totem_object):
		totem_object.remove_sidebar_page ("bbc")
		self.loaded_content = False

	def getConnectionSpeed(self):
		speed_map = [ 14400, 19200, 28800, 33600, 34400,
		              56000, 112000, 256000, 384000, 512000,
		              1536000, 10752000 ]
		speed_enum = self.gconf_client.get_int("/apps/totem/connection_speed")
		if speed_enum >= 0 and speed_enum < len(speed_map):
		  speed_kbps = speed_map[speed_enum] / 1000
		else:
		  speed_kbps = 0
		gst.log('Configured connection speed #%d: %d kbit/s' % (speed_enum, speed_kbps))
		return speed_kbps

	def playEpisode (self, view, episode):
		gst.info('Playing episode ' + episode.title)
		mrl = episode.getUri(self.getConnectionSpeed())
		if mrl:
		  gst.log('Playing uri ' + mrl)
		  self.totem.action_set_mrl_and_play(mrl, None)
		  #self.totem.action_remote(totem.REMOTE_COMMAND_ENQUEUE, mrl)
		  #self.totem.action_remote(totem.REMOTE_COMMAND_PLAY, mrl)
		else:
		  gst.error('No uri for episode ' + episode.title)

