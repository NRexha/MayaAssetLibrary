import maya.utils
import AssetLibraryTool as al

def setup_asset_library():
    try:
        al.initialize_asset_library()
        print("asset library initialized successfully")
    except Exception as e:
        print(f"asset library failed to initialize: {e}")

maya.utils.executeDeferred(setup_asset_library)
