from PySide2 import QtWidgets, QtCore

class CustomFileSystemModel(QtWidgets.QFileSystemModel):
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            if section == 0:
                return "Library"
        return super().headerData(section, orientation, role)

    def flags(self, index):
        default_flags = super().flags(index)
        if not index.isValid():
            return default_flags

        if index.column() == 0:
            return default_flags | QtCore.Qt.ItemIsEditable
        return default_flags
