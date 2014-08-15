import unittest
import tempfile
import os.path

from src.export.export_to_json import ExportToJson
from src.models.contact import Contact

JSON_OUTPUT = \
'{\n\
  "entries": [\n\
    {\n\
      "color": "red",\n\
      "firstname": "Raphael",\n\
      "lastname": "Daguenet",\n\
      "phonenumber": "435-345-6789",\n\
      "zipcode": "10036"\n\
    }\n\
  ],\n\
  "errors": [\n\
    42\n\
  ]\n\
}'


class ExportTest(unittest.TestCase):

    def setUp(self):
        self.contact_test = Contact("Raphael", "Daguenet", "435-345-6789", "red", "10036")

    def test_json_output(self):
        """
        Check that the result JSON is correctly formatted and as expected.
        Line-indent: 2 spaces
        """
        json_result = ExportToJson.export_contacts([self.contact_test], [42])
        self.assertEqual(json_result, JSON_OUTPUT)

    def test_empty_json_output(self):
        """
        Check that the exporter accepts empty arrays and that the result is correctly formatted.
        """
        expected_result = '{\n\
  "entries": [],\n\
  "errors": []\n\
}'
        json_result = ExportToJson.export_contacts([], [])
        self.assertEqual(json_result, expected_result)

    def test_output_file_permission(self):
        """
        Check that the exporter raises an IOError when given a wrong output file path (directory or permission denied)
        """
        # Export results to a directory
        self.assertIsNotNone(ExportToJson.export_contacts([self.contact_test], [1], "/tmp"))
        self.assertRaises(IOError, open, "/tmp")

        # Export results to a file without permissions
        self.assertIsNotNone(ExportToJson.export_contacts([self.contact_test], [1], "/dev/test.out"))
        self.assertRaises(IOError, open, "/dev/test.out")

    def test_output_file(self):
        """
        Validate the file creation, and compare the file content to what is expected
        """
        result_file_path = tempfile.gettempdir() + "result.out"
        ExportToJson.export_contacts([self.contact_test], [42], result_file_path)

        # Assert that the result file as been created and exist
        self.assertTrue(os.path.isfile(result_file_path))

        # Get the file's content
        with open(result_file_path, "r") as f:
            file_content = f.read()

        # Compare the JSON file's content with the expected output
        self.assertEqual(file_content, JSON_OUTPUT)
