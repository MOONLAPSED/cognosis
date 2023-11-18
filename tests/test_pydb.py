"""
This testing module creates a new SQLite database file, connects to the SQLite database, and creates the necessary tables in the database to represent the relational schema for the Unix file system object.
"""

import sqlite3
import unittest
from src.dbase import create_tables, insert_data, close_connection


def create_database(db_name):
    """
    This function creates a new SQLite database file and connects to the SQLite database.

    Parameters:
    db_name (str): The name of the database file to be created.

    Returns:
    conn: The connection to the SQLite database.
    cursor: The cursor object to execute SQLite commands.
    """
    # Create a new SQLite database file
    conn = sqlite3.connect(db_name)

    # Connect to the SQLite database
    cursor = conn.cursor()

    return conn, cursor


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create a connection to an in-memory SQLite database
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        # Create tables for testing
        create_tables(self.cursor)
        self.conn.commit()

    def test_table_creation(self):
        # Your assertions to check if tables are created correctly
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        self.assertIn(('files',), tables)
        self.assertIn(('directories',), tables)
        # Add more assertions as needed for other tables

    def test_insert_data(self):
        # Test insertion of example data
        insert_data(self.cursor)
        self.conn.commit()

        # Write assertions to check if data is correctly inserted
        # For example, check if a certain row exists in a table

        # Example assertion:
        self.cursor.execute("SELECT * FROM files WHERE id = 1")
        row = self.cursor.fetchone()
        self.assertIsNotNone(row)  # Assert that a row exists with ID 1

    def tearDown(self):
        # Close the database connection after each test
        close_connection(self.conn)

    # Add more test cases for other database functions if needed


if __name__ == '__main__':
    unittest.main()