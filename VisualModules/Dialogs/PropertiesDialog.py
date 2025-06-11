from PySide2 import QtWidgets, QtCore
import os
import maya.cmds as cmds
import datetime


class PropertiesDialog(QtWidgets.QDialog):
    fileRenamed = QtCore.Signal(str, str)  

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Asset Properties")
        self.setMinimumWidth(400)

        self.original_path = file_path
        self.dir_path = os.path.dirname(file_path)
        self.base_name, self.ext = os.path.splitext(os.path.basename(file_path))
        self.png_path = os.path.join(self.dir_path, self.base_name + ".png")

        layout = QtWidgets.QVBoxLayout(self)

        self.name_field = QtWidgets.QLineEdit(self.base_name)
        layout.addWidget(QtWidgets.QLabel("Asset Name:"))
        layout.addWidget(self.name_field)

        self.full_path_label = QtWidgets.QLabel(file_path)
        self.full_path_label.setWordWrap(True)
        layout.addWidget(QtWidgets.QLabel("File Path:"))
        layout.addWidget(self.full_path_label)

        file_info_layout = QtWidgets.QFormLayout()
        file_info_layout.addRow("Size:", QtWidgets.QLabel(self._get_size()))
        file_info_layout.addRow("Created:", QtWidgets.QLabel(self._get_creation_date()))
        file_info_layout.addRow("Triangles:", QtWidgets.QLabel(self._get_triangle_count()))
        layout.addLayout(file_info_layout)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self._apply_changes)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _get_size(self):
        size = os.path.getsize(self.original_path)
        return f"{round(size / 1024, 2)} KB"

    def _get_creation_date(self):
        ts = os.path.getctime(self.original_path)
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    def _get_triangle_count(self):
        if not os.path.exists(self.original_path):
            return "N/A"

        try:
            before = set(cmds.ls(assemblies=True))
            imported = cmds.file(self.original_path, i=True, returnNewNodes=True, type="OBJ" if self.original_path.lower().endswith(".obj") else "FBX")
            after = set(cmds.ls(assemblies=True))
            new_roots = list(after - before)

            all_meshes = []
            for root in new_roots:
                meshes = cmds.listRelatives(root, allDescendents=True, type="mesh", fullPath=True) or []
                all_meshes.extend(meshes)

            tris = sum(cmds.polyEvaluate(m, triangle=True) for m in all_meshes)

            cmds.delete(new_roots)

            return str(tris) if tris > 0 else "0"

        except Exception as e:
            return "N/A"


    def _apply_changes(self):
        new_name = self.name_field.text().strip()
        if not new_name or new_name == self.base_name:
            self.accept()
            return

        new_path = os.path.join(self.dir_path, new_name + self.ext)
        new_png_path = os.path.join(self.dir_path, new_name + ".png")

        try:
            os.rename(self.original_path, new_path)
            if os.path.exists(self.png_path):
                os.rename(self.png_path, new_png_path)
            self.fileRenamed.emit(self.original_path, new_path)
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Rename Error", str(e))
