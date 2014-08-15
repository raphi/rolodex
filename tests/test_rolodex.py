import unittest
import tempfile
import os.path

from src.rolodex import rolodex


class RolodexTest(unittest.TestCase):

    def test_main_rolodex(self):
        """
        Simple test to check that the rolodex program is working correctly.
        We do not check if the output is valid, as this atomic test is done in the correct test file.
        For example, check test_export.py file for test checking if the JSON output is valid.
        """
        result_file_path = tempfile.NamedTemporaryFile(delete=False).name
        rolodex("sample.in", result_file_path)

        # Assert that the result file as been created and exist
        self.assertTrue(os.path.isfile(result_file_path))

        os.remove(result_file_path)
