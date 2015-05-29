import sys
sys.path.append ('..')
import nautilusburn
import gtk
import gobject

if len(sys.argv) != 2:
	print "Usage: write_iso <iso>"
	print "Writes an ISO in maximum speed in simulation mode."
	sys.exit (1)

def on_progress_changed (recorder, fract):
	print "%d%%" % (fract * 100)
	
r = nautilusburn.Recorder()
drives = nautilusburn.get_drives_list(True)
d = drives[0]
t = nautilusburn.DataTrack()
t.filename = sys.argv[1]
r.connect ('progress-changed', on_progress_changed)
print r.write_tracks (d, [t], d.get_max_speed_write(), nautilusburn.RECORDER_WRITE_DUMMY_WRITE | nautilusburn.RECORDER_WRITE_EJECT)
print "done"
