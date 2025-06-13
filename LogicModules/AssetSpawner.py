import os
import uuid
from maya import cmds

class AssetSpawner:

    @staticmethod
    def spawn_asset(file_path):
        if not os.path.exists(file_path):
            cmds.warning(f"Asset not found: {file_path}")
            return

        ext = os.path.splitext(file_path)[1].lower()
        unique_namespace = f"asset_{uuid.uuid4().hex[:8]}"

        try:
            before_nodes = set(cmds.ls(dag=True, long=True))

            if ext == ".fbx":
                cmds.file(file_path, i=True, type="FBX", ignoreVersion=True,
                          ra=True, mergeNamespacesOnClash=False, namespace=unique_namespace,
                          options="fbx", pr=True)
            elif ext == ".obj":
                cmds.file(file_path, i=True, type="OBJ", ignoreVersion=True,
                          ra=True, mergeNamespacesOnClash=False, namespace=unique_namespace,
                          options="obj", pr=True)
            else:
                cmds.warning("Unsupported file format: " + ext)
                return

            after_nodes = set(cmds.ls(dag=True, long=True))
            imported_nodes = list(after_nodes - before_nodes)

            imported_meshes = cmds.ls(imported_nodes, type="mesh", long=True)
            for mesh in imported_meshes:
                shading_groups = cmds.listConnections(mesh, type='shadingEngine')
                if shading_groups:
                    for sg in shading_groups:
                        cmds.sets(mesh, e=True, remove=sg)

                cmds.sets(mesh, e=True, forceElement='initialShadingGroup')

        except Exception as e:
            cmds.warning(f"Failed to import {file_path}: {str(e)}")
