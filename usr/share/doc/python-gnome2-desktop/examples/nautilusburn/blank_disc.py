import sys
sys.path.append ('..')
import nautilusburn
import gtk
import gobject

r = nautilusburn.Recorder()
drives = nautilusburn.get_drives_list(True)
d = drives[0]
print r.blank_disc (d, nautilusburn.RECORDER_BLANK_FAST, False)
print "done"
