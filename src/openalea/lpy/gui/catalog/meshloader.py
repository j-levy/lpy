from PyQGLViewer import *
from openalea.plantgl.scenegraph import *
from openalea.plantgl.algo import *
from openalea.plantgl.math import *
from OpenGL.GL import *
from openalea.plantgl.gui.qt import QtCore, QtGui
from openalea.plantgl.gui.qt.QtGui import QMenu, QAction
from openalea.plantgl.gui.qt.QtCore import Qt
import math

import openalea.plantgl.all as pgl
from openalea.plantgl.gui.qt.QtWidgets import QFileDialog
from openalea.plantgl.gui.pglviewer import PglViewer
from openalea.plantgl.codec.obj import codec as obj_codec

from openalea.lpy.gui.catalog.catalog import CatalogDockWidget

from openalea.plantgl.gui.qt.QtGui import QOpenGLWidget 
QGLParentClass = QOpenGLWidget 

class MeshLoader (PglViewer):
    BLACK_THEME = {'Curve' : (255,255,255), 'BackGround' : (51,51,51), 'Text' : (255,255,255), 'CtrlCurve' : (122,122,0), 'GridStrong' : (102,102,102), 'GridFade' : (51,51,51) , 'Points' : (250,30,30), 'FirstPoint' : (250,30,250), 'SelectedPoint' : (30,250,30), 'DisabledBackGround' : (150,150,150) }
    WHITE_THEME = {'Curve' : (255,0,0), 'BackGround' : (255,255,255), 'Text' : (0,0,0), 'CtrlCurve' : (25,0,25), 'GridStrong' : (102,102,102), 'GridFade' : (153,153,153) , 'Points' : (30,250,30), 'FirstPoint' : (250,30,250), 'SelectedPoint' : (30,250,30), 'DisabledBackGround' : (150,150,150)}
    valueChanged = QtCore.pyqtSignal()
    contextMenu : QMenu = None

    def __init__(self,parent):
        PglViewer.__init__(self,parent)
        self.createContextMenu()

    def createContextMenu(self):
        """ define the context menu """
        self.contextMenu = QMenu(self)
        self.contextMenu.addAction("Load from catalog...", lambda: self.loadFromCatalog())

    def loadFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
            '~',"Obj files (*.obj)")[0]
        scene = pgl.Scene()
        print(fname)
        scene = obj_codec.read(fname)
        self.display(scene)

    def loadFromCatalog(self):
        self.catalogDockWidget = CatalogDockWidget()
        CatalogDockWidget.show()

    def tetraScene(self) -> pgl.Scene:
        # list of points
        vertices = [(1, 0, -1 / math.sqrt(2)),
                    (-1, 0, -1 / math.sqrt(2)),
                    (0, 1, 1 / math.sqrt(2)),
                    (0, -1, 1 / math.sqrt(2))]

        # list of indices to make the faces
        connectivity = [(0, 1, 2),
                        (0, 1, 3),
                        (1, 2, 3),
                        (0, 2, 3)]  #
        s = pgl.TriangleSet(vertices, connectivity)
        scene = pgl.Scene()
        scene.add(s)
        return scene
    
    def mousePressEvent(self,event):
        """mousePressEvent: function handling mouse press events"""
        if event.button() == Qt.RightButton:
            self.contextMenu.exec_(event.globalPos())
        else:
            QGLParentClass.mousePressEvent(self,event)


if __name__ == '__main__':
    qapp = QtGui.QApplication([])
    mv = MeshLoader(parent=None)
    mv.setEnabled(True)
    mv.display(mv.tetraScene())
    # mv.loadFile()
    mv.show()
    qapp.exec_()
