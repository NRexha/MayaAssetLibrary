# Maya Asset Library

The Maya Asset Library Tool is a custom asset manager designed to simplify asset organization and usage directly within Maya.

## Setup

### Requirements
- Autodesk Maya 2018 or later

### Installation
1. Clone or download the repository to a folder on disk.
2. Open `AssetLibrary.mod` with any text editor.
3. Replace `YourPath` with the path where you placed the repository. The file should look something like:

    ```
    + Asset_Library 1.0 C:/Users/user/Desktop/MyTools  
    scripts: C:/Users/user/Desktop/MyTools/AssetLibrary
    ```

4. Place `AssetLibrary.mod` in one of Maya's recognized module paths for your Maya version, for example:
```Documents/maya/2024/modules```

    > **Note:** If the `modules` folder doesn't exist, you can create it manually. Folder names are case-sensitive.

5. Restart Maya. You should now see an **Assets Library** menu in Maya’s main menu bar.

### First Launch
1. Open the **Assets Library** from the Maya menu bar.
2. Go to **Configure → Set Library Path**.
3. Depending on your path, you can either use existing folders or create new ones by right-clicking in the Library panel (or via Windows Explorer).

---

## How to Use

### Add Assets
1. Select a folder in the **Library** section.
2. Select a mesh in the scene.
3. From Maya's menu bar, click on **Assets Library → Add Mesh to Library**.
4. Enter a name for the asset (this name will be shown in the library) and choose a file format.
5. The asset is now in your library and can be spawned by clicking on it. You can also right-click the asset and assign a **Category**.

> **Note:** Assets added through the tool will automatically generate a thumbnail. Older assets (not added with the tool) will still appear in the library, but without thumbnails. This will be improved in the future.

### Categories and Properties
- To create a category, right-click in the **Categories** section and select **Add Category**.
- To assign a category to an asset, right-click the asset and choose **Properties** to open the **Properties Panel**.
- Categories can be used to filter your assets in the grid view.

---

## Future Improvements

- **Support more asset types:** Extend file filtering in the grid view.
- **Add thumbnails to legacy assets:** Implement thumbnail generation for existing files.
- **Enhance drag-and-drop:** Allow assets to be dragged into the scene.
- **Save metadata:** Expand the properties dialog to support more asset data.
- **Remote or shared libraries:** Enable cloud-based or network path support.
