﻿import bpy
import os

bl_info = {
    'name': 'Blender Skunk',
    'description': 'Collection of tools for processing models for CHARK games',
    'author': 'CHARK',
    'tracker_url': 'https://github.com/chark/blender-skunk',
    'doc_url': 'https://github.com/chark/blender-skunk',
    'support': 'COMMUNITY',
    'version': (0, 0, 1),
    'blender': (4, 1, 0),
    'category': 'Object',
}


class OpDistributeObjects(bpy.types.Operator):
    bl_idname = 'object.skunk_distribute_objects'
    bl_label = 'Distribute Objects'
    bl_description = 'Distributes selected objects evenly for easy viewing and processing'
    bl_options = {'REGISTER', 'UNDO'}

    distance: bpy.props.IntProperty(
        name='Distance',
        description='Distance between objects on X axis',
        default=10,
        min=0,
        max=100
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        objects = context.selected_objects[:]

        self.distribute_objects(objects)

        self.report(
            {'INFO'},
            f'Distributed {len(objects)} objects on X axis'
        )

        return {'FINISHED'}

    @staticmethod
    def distribute_objects(objects, distance=10):
        offset_x = 0

        for object in objects:
            if object.parent:
                continue

            object.location = (offset_x, 0, 0)
            offset_x = offset_x + distance


class OpCreateEmptyParents(bpy.types.Operator):
    bl_idname = 'object.skunk_create_empty_parents'
    bl_label = 'Create Empty Parents'
    bl_description = 'Creates empty parent for selected objects'
    bl_options = {'REGISTER', 'UNDO'}

    child_name_suffix: bpy.props.StringProperty(
        name='Child Name Suffix',
        description='Suffix appended to child names',
        default='Child'
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        objects = context.selected_objects[:]

        self.create_empty_parents(objects)

        self.report(
            {'INFO'},
            f'Created empty parents for {len(objects)} objects'
        )

        return {'FINISHED'}

    @staticmethod
    def create_empty_parents(objects, child_name_suffix='Child'):
        for object in objects:
            object_name = object.name

            parent_object = OpCreateEmptyParents.create_empty_parent(object)
            object.name = f"{object_name}_{child_name_suffix}"
            parent_object.name = object_name

    @staticmethod
    def create_empty_parent(object):
        # Create parent
        bpy.ops.object.add(type='EMPTY')
        parent_object = bpy.context.object

        # Move parent
        object_location = object.location.copy()
        parent_object.location = object_location

        # Parent child
        object.parent = parent_object
        object.location = (0, 0, 0)

        return parent_object


class OpMatchMeshNames(bpy.types.Operator):
    bl_idname = 'object.skunk_match_mesh_names'
    bl_label = 'Match Mesh Names'
    bl_description = 'Matches names of selected object meshes to the object names'
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        objects = context.selected_objects[:]

        updated_objects = self.match_mesh_name_to_object(objects)

        self.report(
            {'INFO'},
            f'Matched mesh names of {len(updated_objects)} objects'
        )

        return {'FINISHED'}

    @staticmethod
    def match_mesh_name_to_object(objects, updated_objects=None):
        if updated_objects is None:
            updated_objects = []

        for object in objects:
            object_data = object.data

            if object_data and object_data.users == 1:
                object_data.name = object.name
                updated_objects.append(object)
            else:
                OpMatchMeshNames.match_mesh_name_to_object(object.children, updated_objects)

        return updated_objects


class OpBulkExport(bpy.types.Operator):
    bl_idname = 'object.skunk_bulk_export'
    bl_label = 'Bulk Export'
    bl_description = 'Exports selected objects as FBX to desktop'

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        objects = context.selected_objects[:]

        self.export_fbx(objects)

        self.report(
            {'INFO'},
            f'Exported {len(objects)} objects to Desktop'
        )

        return {'FINISHED'}

    @staticmethod
    def export_fbx(objects):

        # Create a temp scene where exporting will take place
        temp_scene = bpy.data.scenes.new('TempFBXExportScene')
        bpy.context.window.scene = temp_scene

        for object in objects:
            temp_scene.collection.objects.link(object)

            for child_object in object.children_recursive:
                temp_scene.collection.objects.link(child_object)

        for object in objects:
            path = os.path.join(os.path.expanduser('~'), 'Desktop', f'{object.name}.fbx')

            bpy.ops.object.select_all(action='DESELECT')

            # Select a target object with children (needed to export only the selection)
            object.select_set(True)

            for child_object in object.children_recursive:
                child_object.select_set(True)

            original_location = object.location.copy()
            object.location = (0, 0, 0)

            bpy.ops.export_scene.fbx(
                filepath=path,
                use_selection=True,
                object_types={'MESH', 'ARMATURE', 'EMPTY'},
                apply_scale_options='FBX_SCALE_ALL',
                axis_forward='-Y',
                axis_up='Z',
                use_space_transform=False,
                apply_unit_scale=True,
            )

            object.location = original_location

        # Remove temp scene
        bpy.data.scenes.remove(temp_scene)


class OpCreateLODs(bpy.types.Operator):
    bl_idname = 'object.skunk_create_lods'
    bl_label = 'Create LODs'
    bl_description = 'Creates LODs for selected objects'
    bl_options = {'REGISTER', 'UNDO'}

    lod_count: bpy.props.IntProperty(
        name='LODs',
        description='LOD count',
        default=2,
        min=0,
        max=5
    )

    decimate_ratio: bpy.props.FloatProperty(
        name='Decimate ratio',
        description='Decimate ratio applied to LODs, first LOD will receive this value as is, '
                    'following LODs will stack this value',
        default=0.5,
        min=0.0,
        max=1.0
    )

    is_delete_old_lods: bpy.props.BoolProperty(
        name='Delete Old LODs',
        description='Should old LODs be deleted/overwritten?',
        default=True,
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        objects = context.selected_objects[:]

        if self.is_delete_old_lods:
            self.delete_lods(self.get_valid_objects(objects))

        self.create_lods(self.get_valid_objects(objects), self.lod_count, self.decimate_ratio)

        self.report(
            {'INFO'},
            f'Created {self.lod_count} LODs for {len(objects)} objects'
        )

        return {'FINISHED'}

    @staticmethod
    def get_valid_objects(objects):
        valid_objects = []

        for object in objects:
            if object.type == 'MESH':
                valid_objects.append(object)
            else:
                for object_child in object.children_recursive:
                    if object_child.type == 'MESH':
                        valid_objects.append(object_child)

        return valid_objects

    @staticmethod
    def delete_lods(objects):
        for object in objects:
            object_name = object.name

            if object_name.endswith('_LOD0'):
                continue
            else:
                bpy.data.objects.remove(object, do_unlink=True)

    @staticmethod
    def create_lods(objects, lod_count, decimate_ratio):
        for object in objects:
            for lod_index in range(1, lod_count + 1):
                OpCreateLODs.create_lod(object, lod_index, pow(decimate_ratio, lod_index))

    @staticmethod
    def create_lod(object, lod_index, decimate_ratio):

        # Copy data
        object_copy = object.copy()
        object_copy.data = object.data.copy()
        object_copy.location = object.location

        bpy.context.collection.objects.link(object_copy)

        # Naming
        if object.name.endswith('_LOD0'):
            object_name = object.name.replace('_LOD0', f'_LOD{lod_index}')
        else:
            object_name = f'{object.name}_LOD{lod_index}'

        object_copy.data.name = object_name
        object_copy.name = object_name

        # Decimate
        decimate_modifier = object_copy.modifiers.new(name='Decimate', type='DECIMATE')
        decimate_modifier.ratio = decimate_ratio
        bpy.context.view_layer.objects.active = object_copy
        bpy.ops.object.modifier_apply(modifier=decimate_modifier.name)


class SkunkPanel(bpy.types.Panel):
    bl_idname = 'skunk_panel'
    bl_label = 'Skunk'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Skunk'

    def draw(self, context):
        layout = self.layout

        layout.operator(OpDistributeObjects.bl_idname)
        layout.operator(OpCreateEmptyParents.bl_idname)
        layout.operator(OpMatchMeshNames.bl_idname)
        layout.operator(OpCreateLODs.bl_idname)
        layout.operator(OpBulkExport.bl_idname)


def register():
    bpy.utils.register_class(OpDistributeObjects)
    bpy.utils.register_class(OpCreateEmptyParents)
    bpy.utils.register_class(OpMatchMeshNames)
    bpy.utils.register_class(OpCreateLODs)
    bpy.utils.register_class(OpBulkExport)
    bpy.utils.register_class(SkunkPanel)


def unregister():
    bpy.utils.unregister_class(OpDistributeObjects)
    bpy.utils.unregister_class(OpCreateEmptyParents)
    bpy.utils.unregister_class(OpMatchMeshNames)
    bpy.utils.unregister_class(OpCreateLODs)
    bpy.utils.unregister_class(OpBulkExport)
    bpy.utils.unregister_class(SkunkPanel)


if __name__ == '__main__':
    register()