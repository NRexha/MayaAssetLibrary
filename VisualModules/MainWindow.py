from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from VisualModules.ToolBar import ToolBar
from VisualModules.FolderTreeView import FolderTreeView
from VisualModules.GridView import GridView
from VisualModules.Dialogs.ConfigureDialog import ConfigureDialog
from VisualModules.Categories import Categories
from LogicModules.Configuration import Configuration
from LogicModules.AssetExporter import AssetExport
import os

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)

class MainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    toolName = 'AssetsLibraryWindow'

    def __init__(self, parent=get_maya_main_window()):
        self.delete_instances()
        super(MainWindow, self).__init__(parent)
        self.setObjectName(self.toolName)
        self.setWindowTitle("Assets Library")
        self.setMinimumSize(800, 500)
        self.current_theme = "dark" 

        self.style_sheet = self.get_style_sheet()
        self.setStyleSheet(self.style_sheet)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.toolbar = ToolBar(parent=self)
        self.toolbar.setStyleSheet(self.style_sheet)
        self.toolbar.setFixedHeight(20)
        self.toolbar.theme_changed.connect(self.on_theme_changed)

        self.folder_tree = FolderTreeView(self)
        self.folder_tree.setStyleSheet(self.style_sheet)

        self.grid_view = GridView(self)
        self.grid_view.setStyleSheet(self.style_sheet)

        self.folder_tree.directory_selected.connect(self.on_directory_selected)

        saved_path = Configuration.get_asset_library_path()
        if saved_path and os.path.isdir(saved_path):
            self.folder_tree.set_directory(saved_path)

        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.toolbar)

        drop_btn = QtWidgets.QPushButton("Add Mesh To Library", self)
        drop_btn.clicked.connect(self.add_selected_mesh)

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(2)

        left_layout.addWidget(self.folder_tree)

        self.categories = Categories(self)
        self.categories.setStyleSheet(self.style_sheet)
        left_layout.addWidget(self.categories)

        splitter = QtWidgets.QSplitter()
        splitter.addWidget(left_widget)
        splitter.addWidget(self.grid_view)
        splitter.setSizes([225, 575])

        main_layout.addWidget(splitter)
        main_layout.addWidget(drop_btn)

        self.toolbar.configure_requested.connect(self.open_configure_dialog)

    def delete_instances(self):
        for widget in QtWidgets.QApplication.allWidgets():
            if widget.objectName() == self.toolName:
                widget.close()
                widget.deleteLater()

    def get_style_sheet(self, theme="dark"):
        file_name = "dark.qss" if theme == "dark" else "light.qss"
        self.style_path = os.path.join(os.path.dirname(__file__), f'Style/{file_name}')
        with open(self.style_path, 'r') as f:
            return f.read()

    def apply_style_sheet(self):
        self.setStyleSheet(self.style_sheet)
        self.toolbar.setStyleSheet(self.style_sheet)
        self.folder_tree.setStyleSheet(self.style_sheet)
        self.grid_view.setStyleSheet(self.style_sheet)

    def on_theme_changed(self, theme):
        self.current_theme = theme
        self.style_sheet = self.get_style_sheet(theme)
        self.apply_style_sheet()

    def add_selected_mesh(self):
        selected_folder = self.folder_tree.get_selected_directory()
        if not selected_folder or not os.path.isdir(selected_folder):
            QtWidgets.QMessageBox.warning(self, "No Folder Selected", "Please select a folder in the tree view.")
            return

        export_path, thumbnail_path = AssetExport.export_selected_mesh(self, selected_folder)
        if export_path:
            self.grid_view.populate([export_path])

    def on_directory_selected(self, path):
        if os.path.isdir(path):
            files = [os.path.join(path, f) for f in os.listdir(path)]
            self.grid_view.populate(files)

    def open_configure_dialog(self):
        dialog = ConfigureDialog(self)
        dialog.path_saved.connect(self.on_path_saved)
        dialog.exec_()

    def on_path_saved(self, new_path):
        if os.path.isdir(new_path):
            self.folder_tree.set_directory(new_path)


    def run(self):
        self.show(dockable=True)
