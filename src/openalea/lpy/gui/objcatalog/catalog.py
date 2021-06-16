

"""
from openalea.plantgl.gui.objloader import ObjLoader

from openalea.lpy.gui.abstractobjectmanager import *
from openalea.plantgl.gui.qt import QtGui, QtWidgets

from openalea.plantgl.all import Scene, Polyline

import openalea.plantgl.all as pgl
from openalea.plantgl.gui.qt.QtWidgets import QFileDialog
from openalea.plantgl.codec.obj import Group
"""
from openalea.plantgl.codec.obj import codec as obj_codec
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



