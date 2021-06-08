#try:
#    from openalea.plantgl.gui.curve2deditor import Curve2DEditor, FuncConstraint
#except ImportError as e:
#    Curve2DEditor = None

from openalea.lpy.gui.abstractobjectmanager import *
from openalea.plantgl.gui.qt import QtGui, QtWidgets

import openalea.plantgl.all as pgl


class MeshTriangleManager(AbstractPglObjectManager):
    """see the doc of the objectmanager abtsract class to undesrtand the implementation of the functions"""

    def __init__(self):
        AbstractPglObjectManager.__init__(self, "MeshTriangle")

    def displayThumbnail(self, obj, i, focus, objectthumbwidth):
        raise NotImplementedError('displayThumbnail')
        # displayLineAsThumbnail(self, obj, i, objectthumbwidth, (1, 0, 1, 1))

    def createDefaultObject(self, subtype=None):
        import math
        # list of points
        points = [(1, 0, -1 / math.sqrt(2)),
                  (-1, 0, -1 / math.sqrt(2)),
                  (0, 1, 1 / math.sqrt(2)),
                  (0, -1, 1 / math.sqrt(2))]

        # list of indices to make the faces
        connectivity = [(0, 1, 2),
                        (0, 1, 3),
                        (1, 2, 3),
                        (0, 2, 3)]  #
        tetra = pgl.TriangleSet(points, connectivity)
        return tetra

    # TODO: check if editor functions are relevant for this use case (is there a 3D editor in PlantGL for meshes? And should we use it?)
    """
    def getEditor(self, parent):
        return None #no given editor for TriangleSet.

    def setObjectToEditor(self, editor, obj):
        # ask for edition of obj with editor
        from copy import deepcopy
        editor.setCurve(deepcopy(obj))

    def retrieveObjectFromEditor(self, editor):
        # ask for current value of object being edited
        return editor.getCurve()
    """
    def writeObjectToLsysContext(self, obj):
        itemName = "" # find a name somehow, could be random
        code = f'''
import openalea.plantgl.all as pgl\n

points{itemName} = {self.pointsToPython(obj)}\n
index{itemName} = {self.indexToPython(obj)}\n
{itemName} = pgl.TriangleSet(points{itemName}, index{itemName})\n
                '''
        return code

    def canImportData(self, fname):
        ## TODO: rewrite this to load some 3D object file (I'll see what's easy to load)
        """
        from os.path import splitext
        ext = splitext(fname)[1]
        return ext == '.fset' or ext == '.func'
        """

    def importData(self, fname):
        ## TODO: rewrite this to load some 3D object file (I'll see what's easy to load)
        """
        from openalea.lpy.gui.lpfg_data_import import import_functions, import_function
        from os.path import splitext
        ext = splitext(fname)[1]
        if ext == '.fset':
            return import_functions(fname)
        else:
            return import_function(fname)
        """

    def fillEditorMenu(self, menubar, editor):
        """ Function call to fill the menu of the editor """
        menu = QtWidgets.QMenu('Theme', menubar)
        menu.addAction('Black', lambda: editor.applyTheme(editor.BLACK_THEME))
        menu.addAction('White', lambda: editor.applyTheme(editor.WHITE_THEME))
        menubar.addMenu(menu)

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
