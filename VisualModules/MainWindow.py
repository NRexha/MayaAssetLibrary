from PySide2 import QtWidgets
from VisualModules.ToolBar import ToolBar
from VisualModules.FolderTreeView import FolderTreeView
from VisualModules.GridView import GridView
from VisualModules.Dialogs.ConfigureDialog import ConfigureDialog
from LogicModules.Configuration import Configuration
import os

class MainWindow(QtWidgets.QDialog):
    toolName = 'Assets Library'

    def __init__(self, parent=None):
        self.delete_instances()
        super(MainWindow, self).__init__(parent)
        self.setObjectName(self.toolName)
        self.setWindowTitle(self.toolName)
        self.resize(800, 500)

        self.style_sheet = self.get_style_sheet()
        self.setStyleSheet(self.style_sheet)

        self.toolbar = ToolBar(parent=self)
        self.toolbar.setStyleSheet(self.style_sheet)
        self.toolbar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.toolbar.setFixedHeight(30)

        self.folder_tree = FolderTreeView(self)
        self.folder_tree.setStyleSheet(self.style_sheet)

        self.grid_view = GridView(self)
        self.grid_view.setStyleSheet(self.style_sheet)

        self.folder_tree.directory_selected.connect(self.on_directory_selected)

        saved_path = Configuration.get_asset_library_path()
        if saved_path and os.path.isdir(saved_path):
            self.folder_tree.set_directory(saved_path)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.toolbar)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(self.folder_tree)
        splitter.addWidget(self.grid_view)
        splitter.setSizes([225, 575])
        main_layout.addWidget(splitter)

        self.toolbar.configure_requested.connect(self.open_configure_dialog)

    def on_directory_selected(self, path):
        if os.path.isdir(path):
            files = [os.path.join(path, f) for f in os.listdir(path)]
            self.grid_view.populate(files)

    def get_style_sheet(self):
        self.style_path = os.path.join(os.path.dirname(__file__), 'Style/style.qss')
        with open(self.style_path, 'r') as f:
            return f.read()

    def open_configure_dialog(self):
        dialog = ConfigureDialog(self)
        dialog.path_saved.connect(self.on_path_saved)
        dialog.exec_()

    def on_path_saved(self, new_path):
        if os.path.isdir(new_path):
            self.folder_tree.set_directory(new_path)

    def delete_instances(self):
        for widget in QtWidgets.QApplication.allWidgets():
            if widget.objectName() == self.toolName:
                widget.close()
                widget.deleteLater()

    def run(self):
        self.show()
