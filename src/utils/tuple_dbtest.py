"""
This module creates a new SQLite database file, connects to the SQLite database, and creates the necessary tables in the database to represent the relational schema for the Unix file system object.
"""

import sqlite3
from src.app.classdef import *

def TestDB_():
    # Create a new SQLite database file
    conn = sqlite3.connect(db_name)

    # Connect to the SQLite database
    cursor = conn.cursor()

    return conn, cursor

def create_database(conn):
    """
    This function creates a new SQLite database file and connects to the SQLite database.

    Parameters:
    db_name (str): The name of the database file to be created.

    Returns:
    conn: The connection to the SQLite database.
    cursor: The cursor object to execute SQLite commands.
    """
    # Create a new SQLite database file
    conn = sqlite3.connect(conn)

    # Connect to the SQLite database
    cursor = conn.cursor()

    return conn, cursor

# Create the necessary tables in the database to represent the relational schema for the Unix file system object
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        name TEXT,
        path TEXT,
        size INTEGER,
        created_at TEXT,
        modified_at TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS directories (
        id INTEGER PRIMARY KEY,
        name TEXT,
        path TEXT,
        created_at TEXT,
        modified_at TEXT
    )
''')

def create_tables(cursor):
    """
    This function creates the necessary tables in the database to represent the relational schema for the Unix file system object.

    Parameters:
    cursor: The cursor object to execute SQLite commands.

    Returns:
    None
    """
    # Create the permissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY,
            file_id INTEGER,
            user_id INTEGER,
            permission TEXT,
            FOREIGN KEY (file_id) REFERENCES files (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')

# Define the attributes and elements of the Unix file system object as columns in the appropriate tables
# Insert the data from the source code files into the corresponding tables

# Insert example data into the files table
def insert_data(cursor):
    """
    This function inserts example data into the tables.

    Parameters:
    cursor: The cursor object to execute SQLite commands.

    Returns:
    None
    """
    # Insert example data into the files table
    cursor.execute('''
        INSERT INTO files (name, path, size, created_at, modified_at)
        VALUES ('file1.txt', '/path/to/file1.txt', 100, '2021-01-01', '2021-01-02')
    ''')

    cursor.execute('''
        INSERT INTO files (name, path, size, created_at, modified_at)
        VALUES ('file2.txt', '/path/to/file2.txt', 200, '2021-01-03', '2021-01-04')
    ''')

    # Insert example data into the directories table
    cursor.execute('''
        INSERT INTO directories (name, path, created_at, modified_at)
        VALUES ('dir1', '/path/to/dir1', '2021-01-01', '2021-01-02')
    ''')

    cursor.execute('''
        INSERT INTO directories (name, path, created_at, modified_at)
        VALUES ('dir2', '/path/to/dir2', '2021-01-03', '2021-01-04')
    ''')

    # Insert example data into the permissions table
    cursor.execute('''
        INSERT INTO permissions (file_id, user_id, permission)
        VALUES (1, 1, 'read')
    ''')

    cursor.execute('''
        INSERT INTO permissions (file_id, user_id, permission)
        VALUES (2, 2, 'write')
    ''')

    # Insert example data into the users table
    cursor.execute('''
        INSERT INTO users (name, email)
        VALUES ('user1', 'user1@example.com')
    ''')

    cursor.execute('''
        INSERT INTO users (name, email)
        VALUES ('user2', 'user2@example.com')
    ''')

def close_connection(conn):
    """
    This function commits the changes and closes the connection to the SQLite database.

    Parameters:
    conn: The connection to the SQLite database.

    Returns:
    None
    """
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
