#!/usr/bin/python
"""Example for gtk widgets"""
import pygtk
pygtk.require("2.0")
import gtk

import apt.gtk.widgets


def main():
    """Main function."""
    win = gtk.Window()
    win.connect("destroy", gtk.main_quit)
    progress = apt.gtk.widgets.GtkAptProgress()
    win.set_title("GtkAptProgress Demo")
    win.add(progress)
    progress.show()
    win.show()
    cache = apt.cache.Cache(progress.open)
    if cache["xterm"].isInstalled:
        cache["xterm"].markDelete()
    else:
        cache["xterm"].markInstall()
    progress.show_terminal(expanded=True)
    cache.commit(progress.fetch, progress.install)
    gtk.main()

if __name__ == "__main__":
    main()
