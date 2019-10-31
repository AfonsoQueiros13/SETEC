import gi
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
import scipy.io as scio
from mpl_toolkits.mplot3d import Axes3D


class MainGUI():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("./gui/xradio_viewer.glade")
        self.mainwin = builder.get_object("mainWindow")
        self.plotwin = builder.get_object("plotWindow")
        self.mainwin.connect("delete-event", Gtk.main_quit)
        
        #connect_switch = builder.get_object("connect_switch")
        #connect_switch.connect("state-set", self.on_connect_switch)
        play_button = builder.get_object("playbtn1")
        play_button.connect("clicked", self.on_play_button)
        pause_button = builder.get_object("pausebtn1")
        pause_button.connect("clicked", self.on_pause_button)
        record_button = builder.get_object("record_btn1")
        record_button.connect("clicked", self.on_record_button)
        screenshot_button = builder.get_object("screenshot_btn1")
        screenshot_button.connect("clicked", self.on_screenshot_button)
        save_as_button = builder.get_object("save_btn1")
        save_as_button.connect("clicked", self.on_save_button)

        #load matrix
        mat = scio.loadmat('./gui/interfaces.mat',verify_compressed_data_integrity=False)
        self.simData = np.array(mat['simulation_data'])
        # Normalize data by factor 1/0.2
        resolution = 5
        # Get data resolution
        x, y, z = self.simData.nonzero()
        # Scale by factor
        self.X, self.Y, self.Z = x/resolution , y/resolution, z/resolution
        self.fig = Figure(figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
        self.ax = self.fig.add_subplot(111,projection='3d')
        self.ax.scatter(self.X, self.Y, self.Z, zdir='z', c= 'red', marker='s')
        self.ax.set_zlim(0, 3)
        self.ax.set_ylim(0, 3)
        self.ax.set_xlim(0, 4)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.show()
        self.plotwin.add(self.canvas)
        self.fig.canvas.draw()
        


    def update_graph(self):
        t1 = time.time()
        self.ax.cla()
        step = 0.5
        self.X, self.Y, self.Z = self.X, self.Y+step, self.Z
        self.ax.scatter(self.X, self.Y, self.Z, zdir='z', c= 'blue', marker='s')
        self.ax.set_zlim(0, 3)
        self.ax.set_ylim(0, 20)
        self.ax.set_xlim(0, 4)
        self.canvas.show()
        self.fig.canvas.draw()
        t2 = time.time()
        print(t2-t1)
        return True

    def startUpdateTimer(self):
        GObject.timeout_add(100, self.update_graph)
        
    def on_play_button(self, button):
        print("Play Button Pressed")
        return True
    
    def on_pause_button(self, button):
        print("Pause Button Pressed")
        return True
    
    def on_screenshot_button(self, button):
        print("Screenshot Button Pressed")
        return True
    
    def on_save_button(self, button):
        print("Save Button Pressed")
        return True
    
    def on_record_button(self, button):
        print("Record Button Pressed")
        return True
    
    def on_connect_switch(self, switch, state):
        print("Connect Switch Pressed")
        return True