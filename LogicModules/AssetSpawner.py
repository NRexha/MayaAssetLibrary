import os
from maya import cmds

class AssetSpawner:

    @staticmethod
    def spawn_asset(file_path):
        if not os.path.exists(file_path):
            cmds.warning(f"Asset not found: {file_path}")
            return

        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == ".fbx":
                cmds.file(file_path, i=True, type="FBX", ignoreVersion=True, ra=True, mergeNamespacesOnClash=False, options="fbx", pr=True)
            elif ext == ".obj":
                cmds.file(file_path, i=True, type="OBJ", ignoreVersion=True, ra=True, mergeNamespacesOnClash=False, options="obj", pr=True)
            else:
                cmds.warning("unsupported file format: " + ext)
        except Exception as e:
            cmds.warning(f"failed to import {file_path}: {str(e)}")
