
from openalea.plantgl.gui.objloader import ObjLoader

from openalea.lpy.gui.abstractobjectmanager import *
from openalea.plantgl.gui.qt import QtGui, QtWidgets

from openalea.plantgl.all import Scene, Polyline

import openalea.plantgl.all as pgl
from openalea.plantgl.gui.qt.QtWidgets import QFileDialog
from openalea.plantgl.codec.obj import codec as obj_codec
from openalea.plantgl.codec.obj import Group


class MeshTriangleManager(AbstractPglObjectManager):
    """see the doc of the objectmanager abtsract class to undesrtand the implementation of the functions"""

    def __init__(self):
        AbstractPglObjectManager.__init__(self, "MeshTriangle")

    def displayThumbnail(self, obj, i, focus, objectthumbwidth):
        # raise NotImplementedError('displayThumbnail')
        return None

    # TODO: check if editor functions are relevant for this use case (is there a 3D editor in PlantGL for meshes? And should we use it?)
    def getEditor(self, parent_widget):
        """ ask for creation of editor. Should be reimplemented """
        # raise NotImplementedError('getEditor')
        return ObjLoader(parent_widget)

    def fillEditorMenu(self, menubar, editor):
        """ Function call to fill the menu of the editor """
        menu = QtWidgets.QMenu('File', menubar)
        menu.addAction('Load .obj', lambda: self.loadObj(editor))
        menubar.addMenu(menu)

    def loadObj(self, editor):
        fname = QFileDialog.getOpenFileName(editor, 'Open file',
            '~',"Obj files (*.obj)")
        print(fname)
        fname = fname[0]
        scene = obj_codec.read(fname)
        scene.name = ""
        self.setObjectToEditor(editor, scene)

    def setObjectToEditor(self, editor, obj):
        """ ask for edition of obj with editor. Should be reimplemented """
        # raise NotImplementedError('setObjectToEditor')
        editor.display(obj)

    def retrieveObjectFromEditor(self, editor):
        """ ask for current value of object being edited """
        # raise NotImplementedError('startObjectEdition')
        return editor.scene

    def defaultObjectTypes(self):
        """ ask for type of object managed by this manager. Several are possible. None means that typename should be used. """
        return None

    def createDefaultObject(self, subtype=None):
        import math
        scene = pgl.Scene()
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
        s = Group('').shape(vertices=vertices, normals=connectivity, textures=[])
        scene.add(s)
        # FIXME: this doesn't work, I don't know why yet
        return scene

    def writeObject(self, obj, indentation):
        raise NotImplementedError('writeObject')

    def writeObjectToLsysContext(self, obj):
        itemName = "" # find a name somehow, could be random
        code = f'''
points{itemName} = {self.pointsToPython(obj)}\n
index{itemName} = {self.indexToPython(obj)}\n
{itemName} = pgl.TriangleSet(points{itemName}, index{itemName})\n
                '''
        return code

    def canImportData(self, fname):
        from os.path import splitext
        ext = splitext(fname)[1]
        return ext == '.obj'

    def importData(self, fname):
        from openalea.plantgl.codec.obj import codec
        if self.canImportData(fname):
            return codec.read(fname)

    def completeContextMenu(self, menu, obj, widget):
        pass

    def managePrimitive(self):
        return False

    def getTheme(self):
        """ get the color theme currently used """
        return {}

    def setTheme(self, theme):
        """ get the color theme according to the theme dict """
        pass


    ### private functions

    def pointsToPython(self, meshTriangle: pgl.TriangleSet) -> str:
        if not isinstance(meshTriangle, pgl.TriangleSet):
            raise TypeError
        return self.listToPython(meshTriangle.pointList)

    def indexToPython(self, meshTriangle: pgl.TriangleSet) -> str:
        if not isinstance(meshTriangle, pgl.TriangleSet):
            raise TypeError
        return self.listToPython(meshTriangle.indexList)

    def listToPython(self, l: list) -> str:
        listOfPython = []
        for i in l:
            item = f'({",".join(map(str, i))})'
            listOfPython.append(item)
        res = ",".join(listOfPython)
        res = f'[{res}]'
        return res


def get_managers():
    return MeshTriangleManager()
