# -*- coding: utf-8 -*-
# Copyright (C) 2012, Almar Klein
#
# Visvis is distributed under the terms of the (new) BSD License.
# The full license can be found in 'license.txt'.

""" Module freezeHelp

Helps freezing apps made using visvis.


"""

import visvis as vv
import os, shutil, sys

backendAliases = {'qt4': 'pyqt4'}


def copyResources(destPath):   
    """ copyResources(destinationPath)
    
    Copy the visvis resource dir to the specified folder 
    (The folder containing the frozen executable).
    
    """
    # create folder (if required)
    destPath = os.path.join(destPath, 'visvisResources')
    if not os.path.isdir(destPath):
        os.makedirs(destPath)
    # copy files
    path = vv.misc.getResourceDir()
    for file in os.listdir(path):
        if file.startswith('.') or file.startswith('_'):
            continue
        shutil.copy(os.path.join(path,file), os.path.join(destPath,file))
    # copy FreeType library to resource dir
    try:
        ft_filename = vv.text.freetype.FT.filename
    except Exception:
        ft_filename = None
    if ft_filename:
        fname = os.path.split(ft_filename)[1]
        shutil.copy(ft_filename, os.path.join(destPath,fname))

def getIncludes(backendName):
    """ getIncludes(backendName)
    
    Get a list of includes to extend the 'includes' list
    with of py2exe or bbfreeze. The list contains:
      * the module of the specified backend 
      * all the functionnames, which are dynamically loaded and therefore
        not included by default.
      * opengl stuff
    
    """
    # init
    includes = []
    backendName = backendAliases.get(backendName, backendName)
    
    # backend
    backendModule = 'visvis.backends.backend_'+ backendName
    includes.append(backendModule)
    if backendName == 'pyqt4':
        includes.extend(["sip", "PyQt4.QtCore", "PyQt4.QtGui", "PyQt4.QtOpenGL"])
    elif backendName == 'pyside':
        includes.extend(["PySide.QtCore", "PySide.QtGui", "PySide.QtOpenGL"])
    
    # functions
    for funcName in vv.functions._functionNames:
        includes.append('visvis.functions.'+funcName)
    
    # processing functions
    for funcName in vv.processing._functionNames:
        includes.append('visvis.processing.'+funcName)
    
    # opengl stuff
    arrayModules = ["nones", "strings","lists","numbers","ctypesarrays",
        "ctypesparameters", "ctypespointers", "numpymodule", 
        "formathandler"]
    GLUModules = ["glustruct"]
    for name in arrayModules:
        name = 'OpenGL.arrays.'+name
        if name in sys.modules:        
            includes.append(name)
    for name in GLUModules:
        name = 'OpenGL.GLU.'+name
        if name in sys.modules:        
            includes.append(name)
    if sys.platform.startswith('win'):
        includes.append("OpenGL.platform.win32")
    
    # done
    return includes

def getExcludes(backendName):
    """ getExcludes(backendName)
    
    Get a list of excludes. If using the 'wx' backend, you don't
    want all the qt4 libaries.
    
    backendName is the name of the backend which you do want to use.
    
    """
    
    # init
    excludes = []
    backendName = backendAliases.get(backendName, backendName)
    
    # Neglect pyqt4
    if 'pyqt4' != backendName:
        excludes.extend(["sip", "PyQt4", "PyQt4.QtCore", "PyQt4.QtGui"])
    
    # Neglect PySide
    if 'pyside' != backendName:
        excludes.extend(["PySide", "PySide.QtCore", "PySide.QtGui"])
    
    # Neglect wx
    if 'wx' != backendName:
        excludes.extend(["wx"])
    
    # done
    return excludes