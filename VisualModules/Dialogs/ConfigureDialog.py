from PySide2 import QtWidgets, QtCore
import os
from LogicModules.Configuration import Configuration

class ConfigureDialog(QtWidgets.QDialog):
    path_saved = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Asset Library")
        self.setMinimumSize(400,50)
        self.resize(400,50)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.path_edit = QtWidgets.QLineEdit(self)
        self.browse_btn = QtWidgets.QPushButton("Browse", self)
        self.save_btn = QtWidgets.QPushButton("Save", self)

        self.layout.addWidget(self.path_edit)
        self.layout.addWidget(self.browse_btn)
        self.layout.addWidget(self.save_btn)

        self.path_edit.setText(Configuration.get_asset_library_path())

        self.browse_btn.clicked.connect(self.browse_folder)
        self.save_btn.clicked.connect(self.save_path)

    def browse_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Library Folder")
        if folder:
            self.path_edit.setText(folder)

    def save_path(self):
        path = self.path_edit.text()
        Configuration.set_asset_library_path(path)
        self.path_saved.emit(path) 
        self.accept()
