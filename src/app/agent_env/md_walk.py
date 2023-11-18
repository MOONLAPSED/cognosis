import logging
import sqlite3
from multiprocessing import Pool
import markdown
from typing import Dict, List

logger = logging.getLogger(__name__)

def validate_filename(filename: str) -> bool:
  """Check if file has .md extension"""
  return filename.endswith('.md')

def get_metadata(filename: str) -> Dict:
  """Get metadata from Markdown file"""
  
  try:
    with open(filename) as f:
      md = markdown.Markdown(f.read())
    return md.metadata
  
  except Exception as e:
    logger.error(f"Error parsing {filename}: {e}")
    raise
    
def ingest_file(filename: str):
  """Ingest single file metadata to DB"""
  
  if not validate_filename(filename):
    return  

  try: 
    metadata = get_metadata(filename)
  except Exception:
    logger.error(f"Invalid metadata in {filename}")
    return
  
  try:
    with sqlite3.connect('op.db') as conn:
      with conn.cursor() as cursor:
        
        cursor.execute("""
          INSERT INTO documents 
            (id, path, metadata) 
          VALUES (?, ?, ?)
        """, (metadata['id'], filename, metadata))

  except sqlite3.Error as e:
    logger.error(f"DB error processing {filename}: {e}")
      

def ingest_all(filenames: List[str]):
  """Parallel ingest multiple files"""

  pool = Pool()  
  pool.map(ingest_file, filenames)

def main():

  filenames = [f for f in os.listdir('data') if validate_filename(f)]

  logger.info(f"Ingesting {len(filenames)} files")

  ingest_all(filenames)

  logger.info("Done!")