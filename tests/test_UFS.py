# tests/app.UFS.py

import unittest

from src.app.UFS import UnixFilesystem


class TestUnixFilesystem(unittest.TestCase):
    def test_initialization(self):
        # Test initialization of UnixFilesystem object
        fs = UnixFilesystem(
            inode=123,
            pathname="/path/to/file",
            filetype="file",
            permissions="rw",
            owner="user",
            group_id="group",
            PID=456,
            unit_file="unit",
            unit_file_addr="addr",
            size=1024,
            mtime=1623456789,
            atime=1623456790
        )
        self.assertEqual(fs.inode, 123)
        self.assertEqual(fs.pathname, "/path/to/file")
        self.assertEqual(fs.filetype, "file")
        self.assertEqual(fs.permissions, "rw")
        self.assertEqual(fs.owner, "user")
        self.assertEqual(fs.group_id, "group")
        self.assertEqual(fs.PID, 456)
        self.assertEqual(fs.unit_file, "unit")
        self.assertEqual(fs.unit_file_addr, "addr")
        self.assertEqual(fs.size, 1024)
        self.assertEqual(fs.mtime, 1623456789)
        self.assertEqual(fs.atime, 1623456790)

    def test_string_representation(self):
        # Test string representation of UnixFilesystem object
        fs = UnixFilesystem(
            inode=123,
            pathname="/path/to/file",
            filetype="file",
            permissions="rw",
            owner="user",
            group_id="group",
            PID=456,
            unit_file="unit",
            unit_file_addr="addr",
            size=1024,
            mtime=1623456789,
            atime=1623456790
        )
        expected_str = "123: /path/to/file"
        self.assertEqual(str(fs), expected_str)

    # Add more test methods to cover other functionalities and edge cases of the UnixFilesystem class

if __name__ == "__main__":
    unittest.main()
