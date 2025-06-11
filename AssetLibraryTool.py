from maya import cmds

main_window = None 
window_instance = None

def open_asset_library(*args):
    global window_instance, main_window

    try:
        if cmds.workspaceControl('AssetsLibraryWindowWorkspaceControl', exists=True):
            cmds.deleteUI('AssetsLibraryWindowWorkspaceControl', control=True)
    except Exception as e:
        print(f"Could not delete existing workspaceControl: {e}")

    if main_window is None:
        from VisualModules.MainWindow import MainWindow as MW
        main_window = MW

    window_instance = main_window()
    window_instance.run()


def refresh_asset_library(*args):
    try:
        global window_instance
        if window_instance:
            window_instance.close()
            window_instance.deleteLater()
            window_instance = None

        import importlib
        import AssetLibraryTool
        importlib.reload(AssetLibraryTool)

        from Utilities.Utils import reload_package
        import VisualModules
        reload_package(VisualModules)
        from VisualModules.Dialogs.ConfigureDialog import ConfigureDialog

        from VisualModules.MainWindow import MainWindow
        AssetLibraryTool.main_window = MainWindow

        print("asset library reloaded successfully")
    except Exception as e:
        print(f"failed to refresh asset library: {e}")


def initialize_asset_library():
    if cmds.menu("assetsLibraryMenu", exists=True):
        cmds.deleteUI("assetsLibraryMenu")

    cmds.menu("assetsLibraryMenu", label="Assets Library", parent="MayaWindow", tearOff=True)
    cmds.menuItem(label="Open Library", parent="assetsLibraryMenu", command=open_asset_library)
    cmds.menuItem(divider=True, parent="assetsLibraryMenu")
    cmds.menuItem(label="Refresh Tool", parent="assetsLibraryMenu", command=refresh_asset_library)
