from PySide2 import QtWidgets, QtCore
import os

class ToolBar(QtWidgets.QMenuBar):
    configure_requested = QtCore.Signal()

    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)

        self.configure_menu = self.addMenu("Configure")
        self.preferences_menu = self.addMenu("Preferences")

        configure_action = QtWidgets.QAction("Set Library Path", self)
        configure_action.triggered.connect(self.configure_requested.emit)
        self.configure_menu.addAction(configure_action)
