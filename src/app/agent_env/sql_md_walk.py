import os
import sqlite3
import markdown


def verify_data_structure(conn):
    """Verifies that the `documents` table exists and is valid."""

    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents'")
    if not c.fetchone():
        raise ValueError("The `documents` table does not exist.")

        c.execute("PRAGMA table_info('documents')")
        columns = [col[1] for col in c.fetchall()]
    if 'id' not in columns or 'path' not in columns or 'metadata' not in columns:
        raise ValueError("The `documents` table is not valid.")


def get_metadata(filename):
    """Gets the metadata from a markdown file."""

    with open(filename) as f:
        md = markdown.Markdown(f.read())

    metadata = md.metadata

    return metadata


def ingest_markdown(conn):
    """Ingests markdown files into the `documents` table."""

    verify_data_structure(conn)

    for filename in os.listdir('/opt/op/data'):
        metadata = get_metadata(filename)

        id = metadata['id']
        path = filename

        c = conn.cursor()
        c.execute(
            "INSERT INTO documents (id, path, metadata) VALUES (?, ?, ?)",
            (id, path, metadata))

    conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect('/opt/op/op.db')
    ingest_markdown(conn)
    conn.close()

