#!/usr/bin/env python3
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
#Libraries used
import time
import scipy.io as scio
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.pyplot import figure
import numpy as np
import matplotlib as mpl
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import mpld3
from mpld3 import utils
from mpld3._server import serve
from mpld3 import fig_to_html, plugins
# Time controls
t1 = time.time()
# Import data
mat = scio.loadmat('interfaces.mat')
# print all info in interfaces.mat
#print(mat)
# print only the 'simulation_data'
#print(mat['simulation_data'])
# print only the 'measured_data'
#print(mat['measured_data'])
# Data settings
simData = np.array(mat['simulation_data'])
measData = np.array(mat['measured_data'])
# Normalize data by factor 1/0.2
resolution = 5
# Figure configuration
fig = plt.figure(num=1, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_subplot(111, projection='3d')
# Get data resolution
x, y, z = simData.nonzero()
# Scale by factor
X, Y, Z = x/resolution , y/resolution, z/resolution
# Scatter
ax.scatter(X, Y, Z, zdir='z', c= 'red', marker='s')
# Customize the axis format
ax.set_xlabel('---X---')
ax.set_ylabel('---Y---')
ax.set_zlabel('---Z---')
ax.set_zlim(0, 3)
ax.set_ylim(0, 3)
ax.set_xlim(0, 4)
# To specify the number of ticks on both or any single axes
# pyplot.locator_params(axis='y', nbins=6)
# pyplot.locator_params(axis='x', nbins=10)
# Hide grid lines
ax.grid(False)
# Hide axes ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
# Time controls 2
t2 = time.time()
print(t2-t1)
# Set figure settings
plt.show()
#CODE FOR PLUG PLOT IN WEB
# create html for both graphs 

