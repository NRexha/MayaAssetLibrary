from PySide2 import QtWidgets, QtCore
import os
import shutil
from Utilities.CustomeFileSystemModel import CustomFileSystemModel as cm

class FolderTreeView(QtWidgets.QTreeView):
    directory_selected = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.model = QtWidgets.QFileSystemModel()
        self.model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
        self.setModel(self.model)
        self.setHeaderHidden(True)
        self.setAnimated(True)
        self.setIndentation(20)
        self.model.setRootPath('')
        self.clicked.connect(self.on_folder_selected)

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)


        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def set_directory(self, path):
        if os.path.isdir(path):
            self.model.setRootPath(path)
            index = self.model.index(path)
            self.setRootIndex(index)

    def on_folder_selected(self, index):
        if self.model.isDir(index):
            path = self.model.filePath(index)
            self.directory_selected.emit(path)

    def get_selected_directory(self):
        index = self.currentIndex()
        if index.isValid():
            return self.model.filePath(index)
        return None


    def show_context_menu(self, point):
        index = self.indexAt(point)
        is_folder = index.isValid() and self.model.isDir(index)
        global_pos = self.viewport().mapToGlobal(point)

        menu = QtWidgets.QMenu()

        create_action = menu.addAction("Create Folder")
        rename_action = None
        delete_action = None

        if is_folder:
            rename_action = menu.addAction("Rename Folder")
            delete_action = menu.addAction("Delete Folder")

        selected_action = menu.exec_(global_pos)
        if selected_action is None:
            return

        if selected_action == create_action:
            parent_path = self.model.filePath(index) if is_folder else self.model.rootPath()
            self.create_folder_dialog(parent_path)

        elif rename_action and selected_action == rename_action:
            self.edit(index)

        elif delete_action and selected_action == delete_action:
            self.delete_folder(self.model.filePath(index))

    def create_folder_dialog(self, parent_path):
        name, ok = QtWidgets.QInputDialog.getText(self, "New Folder", "Enter folder name:")
        if ok and name:
            new_path = os.path.join(parent_path, name)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Folder already exists.")

    def delete_folder(self, folder_path):
        reply = QtWidgets.QMessageBox.question(self,"Delete Folder",f"Are you sure you want to delete:\n{folder_path}?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                shutil.rmtree(folder_path)
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Error", str(e))

    def keyPressEvent(self, event):
        index = self.currentIndex()
        if not index.isValid():
            return

        if event.key() == QtCore.Qt.Key_F2:
            self.edit(index)
        elif event.key() == QtCore.Qt.Key_Delete:
            path = self.model.filePath(index)
            self.delete_folder(path)
        else:
            super().keyPressEvent(event)
