import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

class Configuration:
    @staticmethod
    def load():
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def save(data):
        with open(CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def get_asset_library_path():
        return Configuration.load().get("asset_library_path", "")

    @staticmethod
    def set_asset_library_path(path):
        config = Configuration.load()
        config["asset_library_path"] = path
        Configuration.save(config)

    @staticmethod
    def get_categories_json_path():
        return os.path.normpath(os.path.join(os.path.dirname(__file__), "categories.json"))

    @staticmethod
    def get_assignments_json_path():
        return os.path.normpath(os.path.join(os.path.dirname(__file__), "assignments.json"))

    @staticmethod
    def load_assignments():
        path = Configuration.get_assignments_json_path()
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def save_assignments(data):
        path = Configuration.get_assignments_json_path()
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
