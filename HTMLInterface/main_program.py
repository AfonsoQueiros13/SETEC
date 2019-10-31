import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

import sys
sys.path.append('./gui/')

import xradio_viewer

viewer = xradio_viewer.MainGUI()
viewer.mainwin.show_all()
viewer.startUpdateTimer()

Gtk.main()
