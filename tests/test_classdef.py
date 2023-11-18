import unittest

from src.app.classdef import BLOB, INTEGER, REAL, TEXT, VARCHAR


class TestTEXT(unittest.TestCase):
    def test_initialization(self):
        attribute = TEXT("name")
        self.assertEqual(attribute.name, "name")
        self.assertEqual(attribute.description, "TEXT")

    def test_string_representation(self):
        attribute = TEXT("name")
        self.assertEqual(str(attribute), "name: TEXT")

class TestINTEGER(unittest.TestCase):
    def test_initialization(self):
        attribute = INTEGER("name")
        self.assertEqual(attribute.name, "name")
        self.assertEqual(attribute.description, "INTEGER")

    def test_string_representation(self):
        attribute = INTEGER("name")
        self.assertEqual(str(attribute), "name: INTEGER")

class TestREAL(unittest.TestCase):
    def test_initialization(self):
        attribute = REAL("name")
        self.assertEqual(attribute.name, "name")
        self.assertEqual(attribute.description, "REAL")

    def test_string_representation(self):
        attribute = REAL("name")
        self.assertEqual(str(attribute), "name: REAL")

class TestBLOB(unittest.TestCase):
    def test_initialization(self):
        attribute = BLOB("name")
        self.assertEqual(attribute.name, "name")
        self.assertEqual(attribute.description, "BLOB")

    def test_string_representation(self):
        attribute = BLOB("name")
        self.assertEqual(str(attribute), "name: BLOB")

class TestVARCHAR(unittest.TestCase):
    def test_initialization(self):
        attribute = VARCHAR("name", 10)
        self.assertEqual(attribute.name, "name")
        self.assertEqual(attribute.description, "VARCHAR(10)")
        self.assertEqual(attribute.length, 10)

    def test_string_representation(self):
        attribute = VARCHAR("name", 10)
        self.assertEqual(str(attribute), "name: VARCHAR(10)")

if __name__ == "__main__":
    unittest.main()
