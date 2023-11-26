import sqlite3, os

def dbinit(db_name):
    # Create the database if it doesn't exist
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        conn.execute("CREATE TABLE IF NOT EXISTS rlhf (id INTEGER PRIMARY KEY, name TEXT, url TEXT, date TEXT)")
        conn.commit()
        conn.close()

class RLHF(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def dbinitcall(self):
        pass


if __name__ == "__main__":
    db_name = 'rlhf.db'
    dbinit(db_name)
    rlhf = RLHF(db_name)
    rlhf.dbinitcall(rlhf)
