
from PyQt5.QtWidgets import QDialog
from openalea.lpy.gui.catalog.catalog import Catalog, CatalogDock

from openalea.lpy.gui.abstractobjectmanager import *
from openalea.lpy.gui.catalog.meshloader import MeshLoader
from openalea.plantgl.gui.qt import QtGui, QtWidgets

from openalea.plantgl.all import Scene, Polyline

import openalea.plantgl.all as pgl
from openalea.plantgl.gui.qt.QtWidgets import QFileDialog, QAction
from openalea.plantgl.codec.obj import codec as obj_codec
import os.path


class MeshTriangleManager(AbstractPglObjectManager):
    """see the doc of the objectmanager abtsract class to undesrtand the implementation of the functions"""

    def __init__(self):
        AbstractPglObjectManager.__init__(self, "MeshTriangle")

    # TODO: check if editor functions are relevant for this use case (is there a 3D editor in PlantGL for meshes? And should we use it?)
    def getEditor(self, parent_widget):
        """ ask for creation of editor. Should be reimplemented """
        # raise NotImplementedError('getEditor')
        return MeshLoader(parent_widget)

    def fillEditorMenu(self, menubar, editor):
        """ Function call to fill the menu of the editor """
        menu = QtWidgets.QMenu('File', menubar)
        menu.addAction('Load .obj', lambda: self.loadObjFileDialog(editor))
        exampleObjMenu = QtWidgets.QMenu('Load example .obj', menu)
        c = Catalog()
        exampleObj = c.list_paths()
        for obj in exampleObj:
            exampleObjMenu.addAction(obj, lambda unit=obj: self.loadObj(exampleObj[unit], editor))
        menu.addMenu(exampleObjMenu)
        menubar.addMenu(menu)

    def loadObjFileDialog(self, editor):
        filesSelected = QFileDialog.getOpenFileName(editor, 'Open file',
            '~',"Obj files (*.obj)")
        fname = filesSelected[0]
        self.loadObj(fname, editor)

    def loadObj(self, fname, editor):
        if fname != None:
            scene = obj_codec.read(fname)
            scene.name = os.path.basename(fname)
            self.setObjectToEditor(editor, scene)
        else:
            import warnings
            warnings.warn(f'Can\'t load file {fname}.')

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
        s = pgl.TriangleSet(vertices, connectivity)
        scene.add(pgl.Shape(s))
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
