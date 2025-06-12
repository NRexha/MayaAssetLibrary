from PySide2 import QtWidgets, QtGui, QtCore
import os
from Utilities.FlowLayout import FlowLayout 
from LogicModules.AssetSpawner import AssetSpawner
from VisualModules.Dialogs.PropertiesDialog import PropertiesDialog
import json
from LogicModules.Configuration import Configuration

class GridItem(QtWidgets.QFrame):
    clicked = QtCore.Signal(str)

    def __init__(self, file_path=None, style_sheet="", parent=None):
        super().__init__(parent)
        self.setObjectName("gridItem")
        self.setAttribute(QtCore.Qt.WA_Hover, True)
        self.setProperty("hovered", False)
        self.file_path = file_path

        self.setFixedSize(100, 100)
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
                        target_width, target_height,
                        QtCore.Qt.KeepAspectRatio,
                        QtCore.Qt.SmoothTransformation
                    )

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
        self.label.setAutoFillBackground(True)

        layout.addStretch()
        layout.addWidget(self.label)


    def enterEvent(self, event):
        self.setProperty("hovered", True)
        self.setStyle(self.styleSheet())
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
        elif event.button() == QtCore.Qt.RightButton and self.file_path:
            self._show_context_menu(event.globalPos())
        super().mousePressEvent(event)

    def _show_context_menu(self, global_pos):
        menu = QtWidgets.QMenu()
        delete_action = menu.addAction("Delete")
        properties_action = menu.addAction("Properties")

        action = menu.exec_(global_pos)
        if action == delete_action:
            self._confirm_deletion()
        elif action == properties_action:
            self._open_properties()

    def _confirm_deletion(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Delete Asset",
            f"Are you sure you want to delete '{os.path.basename(self.file_path)}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                if os.path.exists(self.file_path):
                    os.remove(self.file_path)

                thumbnail_path = os.path.splitext(self.file_path)[0] + ".png"
                if os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)

                assignments = Configuration.load_assignments()
                base_name = os.path.splitext(os.path.basename(self.file_path))[0]
                if base_name in assignments:
                    del assignments[base_name]
                    Configuration.save_assignments(assignments)

                self.deleteLater()

            except Exception as e:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    f"Failed to delete asset: {str(e)}"
                )


    def _open_properties(self):
        dialog = PropertiesDialog(self.file_path, self)
        dialog.fileRenamed.connect(self._on_file_renamed)
        dialog.exec_()

    def _on_file_renamed(self, old_path, new_path):
        self.file_path = new_path
        self.label.setText(os.path.splitext(os.path.basename(new_path))[0])





CATEGORIES_JSON_PATH = Configuration.get_categories_json_path()

class GridView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("gridView")
        self._style_sheet = ""
        self.all_file_paths = []

        self.category_filter = QtWidgets.QComboBox(self)
        self.category_filter.addItem("All")
        self.category_filter.currentTextChanged.connect(self.apply_filter)

        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.inner_widget = QtWidgets.QWidget()
        self.inner_widget.setObjectName("gridInnerWidget")
        self.inner_widget.setContentsMargins(5, 0, 0, 0)

        self.flow_layout = FlowLayout(self.inner_widget, spacing=10)
        self.flow_layout.setContentsMargins(50, 50, 50, 50)
        self.inner_widget.setLayout(self.flow_layout)
        self.scroll_area.setWidget(self.inner_widget)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.category_filter)
        layout.addWidget(self.scroll_area)

        self.setPalette(self._get_dark_palette())
        self.setAutoFillBackground(True)
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent, True)

        self.refresh_categories()

    def _get_dark_palette(self):
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#1e1e1e"))
        return palette

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor("#1e1e1e"))
        super().paintEvent(event)

    def setStyleSheet(self, style):
        super().setStyleSheet(style)
        self._style_sheet = style

    def populate(self, file_paths):
        self.all_file_paths = file_paths
        self._populate_filtered("All")

    def refresh_categories(self):
        self.category_filter.blockSignals(True)
        current = self.category_filter.currentText()
        self.category_filter.clear()
        self.category_filter.addItem("All")

        categories = []
        if os.path.exists(CATEGORIES_JSON_PATH):
            with open(CATEGORIES_JSON_PATH, "r") as f:
                data = json.load(f)
                categories = data.get("categories", [])

        self.category_filter.addItems(sorted(categories))
        if current in categories or current == "All":
            self.category_filter.setCurrentText(current)
        self.category_filter.blockSignals(False)

    def apply_filter(self, category):
        self._populate_filtered(category)

    def _populate_filtered(self, category):
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            if item:
                item.widget().deleteLater()

        assignments = Configuration.load_assignments()
        print("Loaded assignments:", assignments)

        for path in self.all_file_paths:
            if not path.lower().endswith(('.fbx', '.obj')):
                continue  

            base = os.path.splitext(os.path.basename(path))[0]
            assigned = assignments.get(base, None)

            print(f"Asset: {base}, Assigned: {assigned}, Filter: {category}")

            if category.lower() == "all" or (assigned and assigned.lower() == category.lower()):
                item = GridItem(path, style_sheet=self._style_sheet)
                item.clicked.connect(AssetSpawner.spawn_asset)
                self.flow_layout.addWidget(item)

