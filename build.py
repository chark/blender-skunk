import zipfile
import ast
from pathlib import Path
import re

INIT_FILE = '__init__.py'
INCLUDE_FILES = [INIT_FILE, 'CHANGELOG.md', 'README.md']
INCLUDE_DIRS = ['screenshots', 'unity-presets']


def build_plugin_zip():
    plugin_base_dir = Path(__file__).parent
    plugin_init_path = plugin_base_dir / INIT_FILE
    plugin_info = get_plugin_info(plugin_init_path)

    plugin_name = format_plugin_name(plugin_info.get('name', 'blender-plugin'))
    plugin_version_num = tuple(plugin_info.get('version', (0, 0, 1)))
    plugin_version_str = '.'.join(map(str, plugin_version_num))

    zip_filename = f'{plugin_name}-v{plugin_version_str}.zip'
    zip_path = plugin_base_dir / zip_filename

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_name in INCLUDE_FILES:
            file_path = plugin_base_dir / file_name
            if file_path.exists():
                archive_file_path = f'{plugin_name}/{file_name}'

                print(f'Adding file {archive_file_path} to archive')
                zipf.write(file_path, f'{plugin_name}/{file_name}')

        for dir_name in INCLUDE_DIRS:
            dir_path = plugin_base_dir / dir_name
            if dir_path.exists():
                for file in dir_path.rglob('*'):
                    if file.is_file():
                        archive_dir_path = f'{plugin_name}/{file.relative_to(plugin_base_dir)}'

                        print(f'Adding dir {archive_dir_path} to archive')
                        zipf.write(file, archive_dir_path)

    print(f'Created plugin ZIP at: {zip_path}')


def get_plugin_info(init_path):
    with open(init_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=init_path)

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'bl_info':
                    return ast.literal_eval(node.value)

    raise ValueError('bl_info not found in __init__.py')


def format_plugin_name(name):
    # Convert to lowercase, replace spaces with dashes, strip non-alphanum (except dash)
    return re.sub(r'[^a-z0-9\-]', '', name.lower().replace(' ', '-'))


if __name__ == '__main__':
    build_plugin_zip()
