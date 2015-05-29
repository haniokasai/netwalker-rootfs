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

import os

def getInstallableCodecsUbuntu():
  import warnings
  warnings.filterwarnings("ignore", "apt API not stable yet", FutureWarning)
  import apt

  codecs = []

  try:
    apt_cache = apt.Cache()
  except:
    gst.warning('Failed to read APT cache')
    return []

  #import time
  #now = time.time()
  for pkg in apt_cache:
    # check only packages that are releated to gstreamer
    # this is a performance hack that brings this code from 30s
    # to 1s on cold cache
    if (not "gstreamer" in pkg.name or 
        pkg.isInstalled or 
        not pkg.candidateDownloadable):
      continue
    record = pkg.candidateRecord
    if not record:
      continue
    if not record.has_key("Gstreamer-Version"):
      continue
    if record.has_key("Gstreamer-Decoders"):
      codec_list = record["Gstreamer-Decoders"].split(";")
      codecs.extend([item.split(",")[0].strip() for item in codec_list])
  #print time.time() - now
    
  return codecs


def getInstallableCodecs():
  codecs = []
  if os.access('/var/cache/app-install/gai-codec-map.gdbm', os.R_OK):
    codecs = getInstallableCodecsUbuntu()
  return codecs


if __name__ == "__main__":
  codecs = getInstallableCodecs()
  if len(codecs) > 0:
    for codec in codecs:
      print "installable: %s" % (codec)
  else:
    print 'No codecs known to be installable'


