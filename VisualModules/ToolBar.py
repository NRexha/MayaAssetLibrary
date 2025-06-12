from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Signal
import webbrowser

class ToolBar(QtWidgets.QMenuBar):
    configure_requested = QtCore.Signal()
    theme_changed = Signal(str)  

    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)

        self.configure_menu = self.addMenu("Configure")
        configure_action = QtWidgets.QAction("Set Library Path", self)
        configure_action.triggered.connect(self.configure_requested.emit)
        self.configure_menu.addAction(configure_action)

        preferences_menu = self.addMenu("Preferences")
        light_action = QtWidgets.QAction("Light Theme", self)
        dark_action = QtWidgets.QAction("Dark Theme", self)
        preferences_menu.addAction(light_action)
        preferences_menu.addAction(dark_action)
        light_action.triggered.connect(lambda: self.theme_changed.emit("light"))
        dark_action.triggered.connect(lambda: self.theme_changed.emit("dark"))

        self.help_menu = self.addMenu("Help")

        help_action = QtWidgets.QAction("Open Documentation", self)
        help_action.triggered.connect(lambda: webbrowser.open("https://github.com/NRexha/MayaAssetLibrary"))
        self.help_menu.addAction(help_action)


