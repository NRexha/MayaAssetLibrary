from PySide2 import QtWidgets, QtCore
import os
from Utilities.CustomeFileSystemModel import CustomFileSystemModel as cm

class FolderTreeView(QtWidgets.QTreeView):
    directory_selected = QtCore.Signal(str)  

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = cm()
        self.model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
        self.setModel(self.model)
        self.setHeaderHidden(False)
        self.setAnimated(True)
        self.setIndentation(20)
        self.model.setRootPath('')
        self.clicked.connect(self.on_folder_selected)
        self.hideColumn(1)  
        self.hideColumn(2) 
        self.hideColumn(3)  
        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch) 


    def set_directory(self, path):
        if os.path.isdir(path):
            self.model.setRootPath(path)
            index = self.model.index(path)
            self.setRootIndex(index)

    def on_folder_selected(self, index):
        if self.model.isDir(index):
            path = self.model.filePath(index)
            self.directory_selected.emit(path)
