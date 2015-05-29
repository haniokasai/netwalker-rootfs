#!/usr/bin/env python
#
# A very simple program that monitors a single key for changes.
#

import gtk
import gconf

def key_changed_callback (client, cnxn_id, entry, label):
    if not entry.value:
	label.set ('<unset>')
    else:
	if entry.value.type == gconf.VALUE_STRING:
	    label.set_text (entry.value.to_string ())
	else:
	    label.set ('<wrong type>')

client = gconf.client_get_default ()

window = gtk.Window ()
window.set_default_size (120, 80)
window.connect ('destroy', lambda w: gtk.main_quit ())

s = client.get_string ("/testing/directory/key")

label = gtk.Label (s or '<unset>')
window.add (label)

client.add_dir ('/testing/directory',
                gconf.CLIENT_PRELOAD_NONE)

client.notify_add ("/testing/directory/key",
                   key_changed_callback, label)

window.show_all ()
gtk.main ()
