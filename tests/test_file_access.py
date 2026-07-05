import unittest

from medusa_agent import _list_project_files, _read_project_file


class ProjectFileAccessTests(unittest.TestCase):
    def test_list_project_files_returns_some_files(self):
        files = _list_project_files()
        self.assertIn("README.md", files)
        self.assertIn("app.py", files)

    def test_read_project_file_reads_existing_file(self):
        content = _read_project_file("README.md")
        self.assertIn("medusa", content.lower())

    def test_read_project_file_rejects_outside_path(self):
        content = _read_project_file("../etc/passwd")
        self.assertIn("Cannot access file", content)


if __name__ == "__main__":
    unittest.main()
