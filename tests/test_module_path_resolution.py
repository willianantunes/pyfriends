import sys

from unittest import TestCase
from unittest.mock import patch

from pyfriends.module_path_resolution import add_custom_module_path


class TestModulePathResolution(TestCase):
    def test_should_include_custom_path_for_resolution(self):
        # Arrange
        some_path = "/agrabah/jafar"
        with patch("pyfriends.module_path_resolution.root_folder", some_path):
            assert some_path not in sys.path
            # Act
            add_custom_module_path()
            # Assert
            assert some_path in sys.path
