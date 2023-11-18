DISABLE TRIGGER entities_timestamp_trigger;
ENABLE TRIGGER entities_timestamp_trigger;

/*
You can also use GNU parallel to disable and enable the trigger before and after your load, respectively. For example, the following command would disable the trigger, run the load, and then re-enable the trigger:

gnu_parallel -j 10 --load 50% --progress disable trigger entities_timestamp_trigger
gnu_parallel -j 10 --load 50% --progress load_data
gnu_parallel -j 10 --load 50% --progress enable trigger entities_timestamp_trigger
*/

/* python version
import sqlite3

def disable_trigger(conn):
  cursor = conn.cursor()
  cursor.execute("DISABLE TRIGGER entities_timestamp_trigger")
  conn.commit()

def enable_trigger(conn):
  cursor = conn.cursor()
  cursor.execute("ENABLE TRIGGER entities_timestamp_trigger")
  conn.commit()

def load_data(conn, data):
  cursor = conn.cursor()
  for row in data:
    cursor.execute("INSERT INTO entities (name, description) VALUES (?, ?)", row)
  conn.commit()

if __name__ == "__main__":
  conn = sqlite3.connect("database.sqlite3")

  disable_trigger(conn)
  load_data(conn, data)
  enable_trigger(conn)
*/