import os
import json

class FileSystemManager:
    def __init__(self, kb_dir, output_dir):
        self.kb_dir = kb_dir
        self.output_dir = output_dir

    def list_kb_files(self):
        return [f for f in os.listdir(self.kb_dir) if f.endswith('.md')]

    def read_file(self, filename):
        with open(os.path.join(self.kb_dir, filename), 'r') as f:
            return f.read()

    def write_file(self, filename, content):
        with open(os.path.join(self.output_dir, filename), 'w') as f:
            f.write(content)