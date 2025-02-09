# Blender Skunk [![Blender v4.3.0](https://img.shields.io/badge/Blender-v4.3.0-blue.svg)](https://www.blender.org/download/)

Blender add-on, which provides a set of tools for bulk 3D model processing. This add-on is designed to be used with Unity, so that LODs are imported automatically (see [Import Mesh with LOD settings](https://docs.unity3d.com/6000.0/Documentation/Manual/importing-lod-meshes.html)).

<p align="center">
  <img src="screenshot.png" />
</p>

## Features

> [!NOTE]
> All features are designed to work for bulk processing - select **root objects** and trigger the appropriate feature

- Distribute Objects - distribute selected objects on chosen axis
- Create Empty Parents - create an empty parent object for selected objects
- Match Mesh Names - match mesh data names to object names
- Sort Mesh By Material - sort mesh data by assigned materials
- Create UVs - create `UV0` and `UV1` channels
- Delete LODs - delete automatically created LODs
- Create LODs - automatically create LODs
- Bulk Export - export `.fbx` in bulk

## Installation

- Download `.zip` file from the [latest release](https://github.com/chark/blender-skunk/releases/latest)
- In Blender, select `Edit > Preferences`
- Open _Add-ons_ tab and click _Install_
- Select the downloaded `.zip` file and click _Install Add-on_

## Releases

- [Latest Release](https://github.com/chark/blender-skunk/releases/latest)
- [Changelog](CHANGELOG.md)
