import sys

from pathlib import Path

root_folder = str(Path(__file__).parent.parent.parent)


def add_custom_module_path():
    if root_folder not in sys.path:
        sys.path.append(root_folder)
