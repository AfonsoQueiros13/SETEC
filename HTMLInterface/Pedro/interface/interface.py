#!/usr/bin/env python3

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import scipy.io as scio
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.pyplot import figure
import numpy as np
import time

# Resolution factor
res = 0.2

def defShape(o, size=(res, res, res)):
    C = [[[0, res, 0],   [0, 0, 0],     [res, 0, 0],     [res, res, 0]],
         [[0, 0, 0],     [0, 0, res],   [res, 0, res],   [res, 0, 0]],
         [[res, 0, res], [res, 0, 0],   [res, res, 0],   [res, res, res]],
         [[0, 0, res],   [0, 0, 0],     [0, res, 0],     [0, res, res]],
         [[0, res, 0],   [0, res, res], [res, res, res], [res, res, 0]],
         [[0, res, res], [0, 0, res],   [res, 0, res],   [res, res, res]]]
    C = np.array(C).astype(float)
    for i in range(3):
        C[:,:,i] *= size[i]
    C += np.array(o)
    return C

def plotShape(positions,sizes=None, alpha=None, colors=None, **kwargs):
    if not isinstance(colors,(list,np.ndarray)): colors=["C0"]*len(positions)
    if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
    print()
    g = []
    for p,s,c in zip(positions,sizes,colors):
        g.append( defShape(p, size=s) )
    #facecolors = np.repeat(colors,6, axis=0)
    return Poly3DCollection(np.concatenate(g), alpha=alpha,
                            facecolors=colors, **kwargs)

def plotSet(ax=None, **Kwargs):
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

    return 0


def poly3Dplot (simData, measData, res, gradScale, ax1, ax2, colorMap1, colorMap2, *args, **kwargs):

    # Time controls t1
    t1 = time.time()

    # Reset last frame method2
    #ax1.cla()
    #ax2.cla()
    #plotSet(ax1)
    #plotSet(ax2)

    # Get data non Zero sim data scaled by factor
    x, y, z = simData.nonzero()
    X, Y, Z = x*res , y*res, z*res

    # Get data measured scale by factor and divided by steps on Z value
    xx, yy, zz = [None]*gradScale, [None]*gradScale, [None]*gradScale
    XX, YY, ZZ = [None]*gradScale, [None]*gradScale, [None]*gradScale
    for i in range(0, gradScale):
        xx[i], yy[i], zz[i] = np.nonzero(np.logical_and(measData > (i/gradScale), measData <= ((i+1)/gradScale)))
        XX[i], YY[i], ZZ[i] = xx[i]*res, yy[i]*res, zz[i]*res

    # Positions and concatenation 
    positions = np.c_[X,Y,Z]
    # print("Positions detected sim: \n", positions, positions.size)

    # Pos and conconcatenation measured data
    posm = [None]*gradScale
    for i in range(0, gradScale):
        posm[i] = np.c_[XX[i], YY[i], ZZ[i]]
        #print("Positions measured: \n", posm[i], posm[i].size)

    # Color settings 
    # colorSimData= np.random.rand(len(positions),3)
    # RGB color scale [0, 1]
    colorSimData = np.full((len(positions),4), (colorMap1[0]/255, colorMap1[1]/255, colorMap1[2]/255, 0.3))
    # print("Colors selected: \n", colorSimData)
    gradSteps = colorMap1 - colorMap2
    colorsMeasData = [None]*gradScale
    for i in range(0, gradScale):
        colorsMeasData[i] = np.full((len(posm[0]),4), ((colorMap2[0]+((gradSteps[0]/gradScale)*(i+1)))/255,
                                                    (colorMap2[1]+((gradSteps[1]/gradScale)*(i+1)))/255, 
                                                    (colorMap2[2]+((gradSteps[2]/gradScale)*(i+1)))/255, np.power((i+1)/gradScale, 2)))
        # print("Colors selected: \n", colorsMeasData[i])

    # Scatter points plot
    # ax.scatter(X, Y, Z, zdir='z', c='black', marker='s')

    # Plot Poly3DCollection - Alpha color / colors settings / edgecolor
    pc = plotShape(positions, alpha = 0.3, colors=colorSimData, edgecolor='r')
    ax1.add_collection3d(pc)

    # Set minium treshol, ex tresholdMin = 1  --> z > tresholdMin/gradScale
    tresholdMin = 2 
    pcm = [None]*gradScale
    for i in range(tresholdMin, gradScale):
        pcm[i] = plotShape(posm[i], alpha = ((i+1)/gradScale), colors = colorsMeasData[i], edgecolor='none')
        ax2.add_collection3d(pcm[i])

    # Plot 3D settings / clear old data
    plt.draw()
    plt.pause(0.0001)

    ax1.collections.clear()
    ax2.collections.clear()
    # Time controls t2
    t2 = time.time()
    print("FPS: : {}".format(1/(t2-t1)))

    return 0

###############################################################################################################
# *********************************************************************************************************** #
# ******************************************* X-Radio 3D 2019/20 ******************************************** #
# *******************************************     Interfaces     ******************************************** #
# *********************************************************************************************************** #
###############################################################################################################

# Import data
mat = scio.loadmat('../data/interfaces.mat')

# print all info in interfaces.mat
#print(mat)

# print only the 'simulation_data'
# print("Simulation data: \n", mat['simulation_data'])
# print only the 'measured_data'
# print("Measured data: \n", mat['measured_data'])

# Data settings
simData = np.array(mat['simulation_data'])
measData = np.array(mat['measured_data'])
# print("Shape: \n", measData.shape)

# Figure and axis configuration
fig = plt.figure('X-Radio', figsize=(18, 6), dpi=80, facecolor='w', edgecolor='k')
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

# Configure sublot inv settings
plotSet(ax1)
plotSet(ax2)

# Plot set prop
# plt.ion()
# plt.show()

# Set gradScale to edit grandient/steps
gradScale = 10
# Starting RGB gradient
colorMap1 = np.array([220, 20, 60])
colorMap2 = np.array([73, 7, 190])

poly3Dplot(simData, measData, res, gradScale, ax1, ax2, colorMap1, colorMap2)

while 1:
    np.random.shuffle(simData)
    np.random.shuffle(measData)
    poly3Dplot(simData, measData, res, gradScale, ax1, ax2, colorMap1, colorMap2)


###############################################################################################################
# ******************************************* X-Radio 3D 2019/20 ******************************************** #
###############################################################################################################
