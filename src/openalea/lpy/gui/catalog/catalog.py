

"""
from openalea.plantgl.gui.objloader import ObjLoader

from openalea.lpy.gui.abstractobjectmanager import *
from openalea.plantgl.gui.qt import QtGui, QtWidgets

from openalea.plantgl.all import Scene, Polyline

from openalea.plantgl.gui.qt.QtWidgets import QFileDialog
from openalea.plantgl.codec.obj import Group
"""
import openalea.plantgl.all as pgl
from openalea.plantgl.gui.qt import QtGui
from openalea.plantgl.gui.qt.QtGui import *
from openalea.plantgl.codec.obj import codec as obj_codec
from openalea.lpy.gui.objectpanel import LpyObjectPanelDock

import pkg_resources
import re

class Catalog():
    def __init__(self):
       return None

    def list(self):
        assets = pkg_resources.resource_listdir(__name__, "assets/")
        return assets

    def path(self, objname):
        resources = pkg_resources.resource_listdir(__name__, f"assets/{objname}")
        regex = re.compile(".*\.obj$")
        filename = [s for s in resources if regex.match(s) ]
        if len(filename) != 1: 
            return None
        path = pkg_resources.resource_filename(__name__, f"assets/{objname}/{filename[0]}")
        return path

    def list_paths(self):
        res = {}
        for obj in self.list():
            res[obj] = self.path(obj)
        return res

class CatalogDockWidget(QDockWidget):
    panelmanager : QWidget = None
    def __init__(self, parent, name, panelmanager: QWidget):
        QDockWidget.__init__(self,parent)
        self.setBaseSize(600, 400)
        self.setMinimumSize(300, 200)
        self.panelmanager = panelmanager
        self.setObjectName(name.replace(' ','_'))
        self.name = name

    


if __name__ == '__main__':
    qapp = QtGui.QApplication([])
    mv = CatalogDockWidget(parent=None, name="TestCatalogDockWidget", panelmanager=QWidget())
    mv.setEnabled(True)
    mv.show()
    qapp.exec_()
