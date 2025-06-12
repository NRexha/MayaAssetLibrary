from PySide2 import QtWidgets, QtCore
import os
import json
import maya.cmds as cmds
import datetime
from LogicModules.Configuration import Configuration as config

CATEGORIES_JSON_PATH = config.get_categories_json_path()

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
        self.category_combo = QtWidgets.QComboBox()
        layout.addWidget(QtWidgets.QLabel("Category:"))
        layout.addWidget(self.category_combo)
        file_path = file_path.replace('\\', '/')
        layout.addWidget(QtWidgets.QLabel(f"File Path: {file_path}"))
        layout.addWidget(QtWidgets.QLabel(f"Created: {self._get_creation_date()}"))
        layout.addWidget(QtWidgets.QLabel(f"Size: {self._get_size()}"))
        layout.addWidget(QtWidgets.QLabel(f"Triangles: {self._get_triangle_count()}"))

        self._load_categories()
        self._load_assigned_category()

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
        except Exception:
            return "N/A"

    def _load_categories(self):
        self.category_combo.setEditable(False)
        self.category_combo.clear()

        placeholder = "— No category selected —"
        self.category_combo.addItem(placeholder)
        self.category_combo.model().item(0).setEnabled(False) 

        if not os.path.exists(CATEGORIES_JSON_PATH):
            return

        with open(CATEGORIES_JSON_PATH, "r") as f:
            data = json.load(f)

        for cat in data.get("categories", []):
            self.category_combo.addItem(cat)

        self.category_combo.setCurrentIndex(0)



    def _load_assigned_category(self):
        try:
            from LogicModules.Configuration import Configuration
            assignments = Configuration.load_assignments()
            assigned = assignments.get(self.base_name, "")
            index = self.category_combo.findText(assigned)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
        except Exception as e:
            print(f"Failed to load assigned category: {e}")

    def _apply_changes(self):
        new_name = self.name_field.text().strip()
        new_path = os.path.join(self.dir_path, new_name + self.ext)
        new_png_path = os.path.join(self.dir_path, new_name + ".png")

        selected_category = self.category_combo.currentText()

        try:
            from LogicModules.Configuration import Configuration  
            assignments = Configuration.load_assignments()

            old_base_name = os.path.splitext(os.path.basename(self.original_path))[0]
            if old_base_name in assignments:
                del assignments[old_base_name]

            assignments[new_name] = selected_category

            Configuration.save_assignments(assignments)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Category Save Error", str(e))

        try:
            if new_name and new_name != self.base_name:
                os.rename(self.original_path, new_path)
                if os.path.exists(self.png_path):
                    os.rename(self.png_path, new_png_path)
                self.fileRenamed.emit(self.original_path, new_path)
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Rename Error", str(e))


