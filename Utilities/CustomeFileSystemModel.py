from PySide2 import QtWidgets, QtCore

class CustomFileSystemModel(QtWidgets.QFileSystemModel):
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            if section == 0:
                return "Library"
        return super().headerData(section, orientation, role)
