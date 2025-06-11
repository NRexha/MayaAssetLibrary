from PySide2 import QtWidgets, QtGui, QtCore
import os
from Utilities.FlowLayout import FlowLayout 

class GridItem(QtWidgets.QFrame):
    def __init__(self, file_path=None, style_sheet="", parent=None):
        super().__init__(parent)
        self.setObjectName("gridItem") 

        self.setFixedSize(100, 100)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        if style_sheet:
            self.setStyleSheet(style_sheet)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addStretch()

        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("gridItemLabel") 
        self.label.setText(os.path.splitext(os.path.basename(file_path))[0] if file_path else "")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setFixedHeight(20)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        layout.addWidget(self.label)


class GridView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("gridView")

        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.inner_widget = QtWidgets.QWidget()
        self.inner_widget.setObjectName("gridInnerWidget")
        self.inner_widget.setContentsMargins(5, 5, 0, 0) 



        self.flow_layout = FlowLayout(self.inner_widget, spacing=10)
        self.flow_layout.setContentsMargins(50, 50, 50, 50)

        self.inner_widget.setLayout(self.flow_layout)
        self.scroll_area.setWidget(self.inner_widget)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scroll_area)

        self._style_sheet = ""

    def setStyleSheet(self, style):
        super().setStyleSheet(style)
        self._style_sheet = style

    def populate(self, file_paths):
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            if item:
                item.widget().deleteLater()

        files = [f for f in file_paths if f.lower().endswith(('.fbx', '.obj'))]
        for f in files:
            item = GridItem(f, style_sheet=self._style_sheet)
            self.flow_layout.addWidget(item)

