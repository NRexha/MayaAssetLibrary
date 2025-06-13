import os
import json
from PySide2.QtWidgets import QListWidget, QMenu, QInputDialog, QMessageBox
from PySide2 import QtCore
from LogicModules.Configuration import Configuration

CATEGORIES_JSON_PATH = Configuration.get_categories_json_path()

class Categories(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)
        self.setFixedHeight(175)
        self.setSpacing(2)
        self.load_categories()

    def open_context_menu(self, pos):
        menu = QMenu(self)
        add_action = menu.addAction("Add Category")
        del_action = menu.addAction("Delete Category")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == add_action:
            self.add_category()
        elif action == del_action:
            self.delete_category()

    def add_category(self):
        text, ok = QInputDialog.getText(self, "Add Category", "Category name:")
        if ok and text:
            if not self.findItems(text, QtCore.Qt.MatchExactly):
                self.addItem(text)
                self.save_categories()
            else:
                QMessageBox.warning(self, "Duplicate", "Category already exists.")

    def delete_category(self):
        item = self.currentItem()
        if item:
            self.takeItem(self.row(item))
            self.save_categories()

    def save_categories(self):
        data = {
            "categories": [self.item(i).text() for i in range(self.count())]
        }
        try:
            with open(CATEGORIES_JSON_PATH, "r") as f:
                existing = json.load(f)
        except:
            existing = {}
        existing["categories"] = data["categories"]
        with open(CATEGORIES_JSON_PATH, "w") as f:
            json.dump(existing, f, indent=4)

    def load_categories(self):
        if not os.path.exists(CATEGORIES_JSON_PATH):
            return
        with open(CATEGORIES_JSON_PATH, "r") as f:
            data = json.load(f)
        for cat in data.get("categories", []):
            self.addItem(cat)
