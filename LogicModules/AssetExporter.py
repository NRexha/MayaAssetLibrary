import os
from maya import cmds
from PySide2 import QtWidgets

class AssetExport:

    @staticmethod
    def export_selected_mesh(parent, export_dir):
        selection = cmds.ls(selection=True, dag=True, type='mesh')
        if not selection:
            QtWidgets.QMessageBox.warning(parent, "No Mesh", "Please select a mesh in Maya.")
            return None, None

        mesh_transform = cmds.listRelatives(selection[0], parent=True, fullPath=True)[0]

        dialog = QtWidgets.QDialog(parent)
        dialog.setWindowTitle("Export Selected Mesh")
        layout = QtWidgets.QFormLayout(dialog)

        name_input = QtWidgets.QLineEdit(dialog)
        format_combo = QtWidgets.QComboBox(dialog)
        format_combo.addItems([".fbx", ".obj"])

        layout.addRow("File Name:", name_input)
        layout.addRow("Format:", format_combo)

        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec_():
            name = name_input.text().strip()
            ext = format_combo.currentText()

            if not os.path.isdir(export_dir):
                os.makedirs(export_dir)

            export_path = os.path.join(export_dir, f"{name}{ext}")

            cmds.select(mesh_transform, r=True)
            if ext == ".fbx":
                cmds.file(export_path, force=True, options="v=0;", type="FBX export", pr=True, es=True)
            else:
                cmds.file(export_path, force=True, options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1", type="OBJexport", pr=True, es=True)

            thumbnail_path = os.path.join(export_dir, f"{name}.png")
            AssetExport.generate_thumbnail(mesh_transform, thumbnail_path)

            return export_path, thumbnail_path
        return None, None

    @staticmethod
    def generate_thumbnail(object_name, save_path):
        camera = cmds.camera(name="ThumbnailCam")[0]
        cmds.select(object_name, r=True)
        cmds.lookThru(camera)
        cmds.viewFit(camera, all=False)

        cmds.playblast(
            completeFilename=save_path,
            format='image',
            frame=cmds.currentTime(query=True),
            width=128,
            height=128,
            showOrnaments=False,
            viewer=False,
            percent=100,
            offScreen=True
        )

        cmds.delete(camera)
