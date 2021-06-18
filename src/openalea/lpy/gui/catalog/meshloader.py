from PyQGLViewer import *
from openalea.plantgl.scenegraph import *
from openalea.plantgl.algo import *
from openalea.plantgl.math import *
from OpenGL.GL import *
from openalea.plantgl.gui.qt import QtCore, QtGui
import math

from openalea.plantgl.gui.qt.QtWidgets import QFileDialog

from openalea.plantgl.gui.pglviewer import PglViewer
import openalea.plantgl.scenegraph._pglsg as sg
from openalea.plantgl.codec.obj import codec as obj_codec

class MeshLoader (PglViewer):
    BLACK_THEME = {'Curve' : (255,255,255), 'BackGround' : (51,51,51), 'Text' : (255,255,255), 'CtrlCurve' : (122,122,0), 'GridStrong' : (102,102,102), 'GridFade' : (51,51,51) , 'Points' : (250,30,30), 'FirstPoint' : (250,30,250), 'SelectedPoint' : (30,250,30), 'DisabledBackGround' : (150,150,150) }
    WHITE_THEME = {'Curve' : (255,0,0), 'BackGround' : (255,255,255), 'Text' : (0,0,0), 'CtrlCurve' : (25,0,25), 'GridStrong' : (102,102,102), 'GridFade' : (153,153,153) , 'Points' : (30,250,30), 'FirstPoint' : (250,30,250), 'SelectedPoint' : (30,250,30), 'DisabledBackGround' : (150,150,150)}
    valueChanged = QtCore.pyqtSignal()

    def __init__(self,parent):
        PglViewer.__init__(self,parent)

    def loadFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
            '~',"Obj files (*.obj)")[0]
        scene = sg.Scene()
        print(fname)
        scene = obj_codec.read(fname)
        self.display(scene)


if __name__ == '__main__':
    qapp = QtGui.QApplication([])
    mv = MeshLoader(parent=None)
    mv.setEnabled(True)
    # mv.loadFile()

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
    from openalea.plantgl.all import TriangleShape, Shape
    s = TriangleShape(vertices=vertices, normals=connectivity)
    s = Shape(s)
    scene = sg.Scene()
    scene.add(s)
    # mv.loadFile()
    mv.display(scene)
    mv.loadFile()
    mv.show()
    qapp.exec_()
