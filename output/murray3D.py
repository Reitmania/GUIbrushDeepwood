'''
Created on Mar 13, 2017

@author: Reiti
'''

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D #@UnresolvedImport
from matplotlib import cm, rcParams
import matplotlib.pyplot as plt
import numpy as np
from matplotlib._cm import _GnBu_data
from scipy.interpolate import griddata
from sklearn.preprocessing import MinMaxScaler
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

# Default Plot Font
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 16


def prePlotting3D(gui, guybrush):
    data = np.asarray(guybrush.sources[gui.comboBox_Source.currentIndex()][gui.comboBox_DS.currentIndex()])

    prePlotXYT(gui, guybrush, dataset)

def prePlotting3Dold(gui, guybrush):
    dataset = guybrush.getDataset()
    
    prePlotXYT(gui, guybrush, dataset)
    
    gui.figure = plt.figure()
    gui.canvas = FigureCanvas(gui.figure)
    gui.toolbar = NavigationToolbar(gui.canvas, gui)
    gui.tabWidget_Net.insertTab(0, gui.canvas, "Learning")
               
    ax = gui.figure.gca(projection='3d')
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
        #X = dataset[:,0]
        #Y = dataset[:,1]
        #Z = np.asarray(dataset[:,2])
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
        #Z = dataset[:,1]
        #surf = self.figure.add_subplot(111)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    surf = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1, cmap="plasma")
    
def prePlotXYT(gui, guybrush, dataset):

    gui.figure = plt.figure()
    gui.canvas = FigureCanvas(gui.figure)
    gui.toolbar = NavigationToolbar(gui.canvas, gui)
    gui.tabWidget_3.removeTab(0)
    gui.tabWidget_3.removeTab(0)
    gui.tabWidget_3.insertTab(0, gui.canvas, "PrePlot")
               
    ax = gui.figure.gca(projection='3d')
    #X = np.arange(-5, 5, 0.25)
    #Y = np.arange(-5, 5, 0.25)
    X = dataset[:,0]
    Y = dataset[:,3]
    Z = dataset[:,1]
    #R = np.sqrt(X**2 + Y**2)
    #Z = np.sin(R)
        #Z = dataset[:,1]
        #surf = self.figure.add_subplot(111)
    #ax.set_xlabel(guybrush.getLabels()[0])
    #ax.set_ylabel(guybrush.getLabels()[5])
    #ax.set_zlabel(guybrush.getLabels()[1])
    #surf = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1, cmap='plasma')


    x,y,z = X,Y,Z
    z = list(map(float, z))
    grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]
    grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')
    #fig = plt.figure()
    ax = gui.figure.gca(projection='3d')
    ax.plot_wireframe(grid_x, grid_y, grid_z, rstride=1, cstride=1, cmap=cm.Spectral, alpha=.5,lw=0.5)
    #ax.plot_surface(grid_x, grid_y, grid_z, cmap=plt.cm.Spectral)
    ax.set_xlabel(guybrush.getLabels()[0])
    ax.set_ylabel(guybrush.getLabels()[3])
    ax.set_zlabel(guybrush.getLabels()[1])

def GrandTour(gui, guybrush, nX, nY, nZ):
    #rcParams['font.family'] = 'serif'
    gui.figure = plt.figure()
    gui.canvas = FigureCanvas(gui.figure)
    gui.toolbar = NavigationToolbar(gui.canvas, gui)
    #gui.tabWidget_3.removeTab(0)
    #gui.tabWidget_3.removeTab(0)
    gui.tabWidget_3.insertTab(0, gui.canvas, "Dataset " + str(gui.comboBox_DS.currentIndex() + 1) + ", " + guybrush.mst_labels[nZ])

    #dataset = guybrush.getDataset()
    dataset = guybrush.sources[gui.comboBox_Source.currentIndex()][gui.comboBox_DS.currentIndex()]
    #dataset = guybrush.sources[gui.comboBox_Source.currentIndex()]
    #dataset = np.asarray(dataset)

    ax = gui.figure.gca(projection='3d')
    X = np.asarray(dataset[guybrush.mst_labels[nX]][:])
    Y = np.asarray(dataset[guybrush.mst_labels[nY]][:])
    Z = np.asarray(dataset[guybrush.mst_labels[nZ]][:])
    #R = np.sqrt(X**2 + Y**2)
    #Z = np.sin(R)
        #Z = dataset[:,1]
        #surf = self.figure.add_subplot(111)
    #ax.set_xlabel(guybrush.getLabels()[0])
    #ax.set_ylabel(guybrush.getLabels()[5])
    #ax.set_zlabel(guybrush.getLabels()[1])
    #surf = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1, cmap='plasma')

    x,y,z = X,Y,Z
    z = list(map(float, z))
    grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]
    grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')
    #fig = plt.figure()
    ax = gui.figure.gca(projection='3d')
    ax.dist = 8
    ax.view_init(elev=20., azim=225)
    #ax.plot_wireframe(grid_x, grid_y, grid_z, rstride=1, cstride=1, cmap=cm.Spectral, alpha=.5,lw=0.5)
    #ax.plot_surface(grid_x, grid_y, grid_z, cmap=cm.coolwarm, rstride=1, cstride=1, alpha=.5,
    #                   linewidth=0, antialiased=True)

    #ax.plot_trisurf(grid_x, grid_y, grid_z, rstride=1, cstride=1,
    #            cmap='viridis', edgecolor='none');

    ax.contour3D(grid_x, grid_y, grid_z, 100, cmap='binary')

    # Customize the z axis.
    #ax.set_zlim(-4.0, 6.0)
    #ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    ax.set_xlabel(guybrush.mst_labels[nX])
    ax.set_ylabel(guybrush.mst_labels[nY])
    ax.set_zlabel(guybrush.mst_labels[nZ])
    
    #gui.figure.colorbar(surf)
    #gui.figure.colorbar(surf, shrink=0.5, aspect=5)
    plt.tight_layout()
    plt.savefig("test.pdf", dpi=300)