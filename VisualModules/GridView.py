from PySide2 import QtWidgets, QtGui, QtCore
import os
from Utilities.FlowLayout import FlowLayout 
from LogicModules.AssetSpawner import AssetSpawner

class GridItem(QtWidgets.QFrame):
    clicked = QtCore.Signal(str)
    def __init__(self, file_path=None, style_sheet="", parent=None):
        super().__init__(parent)
        self.setObjectName("gridItem") 
        self.setAttribute(QtCore.Qt.WA_Hover, True)  
        self.setProperty("hovered", False) 
        self.file_path = file_path

        self.setFixedSize(100, 100)
        #self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        if style_sheet:
            self.setStyleSheet(style_sheet)

        self.thumbnail = None
        if self.file_path:
            base, _ = os.path.splitext(file_path)
            thumbnail_path = base + ".png"
            if os.path.exists(thumbnail_path):
                pixmap = QtGui.QPixmap(thumbnail_path)
                if not pixmap.isNull():
                    zoom_factor = 0.8  
                    target_width = int(self.width() * zoom_factor)
                    target_height = int(self.height() * zoom_factor)
                    self.thumbnail = pixmap.scaled(
                    target_width, target_height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("gridItemLabel") 
        self.label.setText(os.path.splitext(os.path.basename(file_path))[0] if file_path else "")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setFixedHeight(20)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        layout.addStretch()
        layout.addWidget(self.label)

    def enterEvent(self, event):
        self.setProperty("hovered", True)
        self.setStyle(self.styleSheet())  # reapply style to trigger change
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setProperty("hovered", False)
        self.setStyle(self.styleSheet())
        super().leaveEvent(event)

    def setStyle(self, style):
        self.setStyleSheet(style)
        for child in self.findChildren(QtWidgets.QWidget):
            child.setStyleSheet(style)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.thumbnail:
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)

            x = (self.width() - self.thumbnail.width()) // 2
            y = (self.height() - self.thumbnail.height()) // 2 - 10  
            painter.drawPixmap(x, y, self.thumbnail)
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.file_path:
            self.clicked.emit(self.file_path)
        super().mousePressEvent(event)




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
            item.clicked.connect(AssetSpawner.spawn_asset)  
            self.flow_layout.addWidget(item)

