import importlib.util
from pathlib import Path
from types import SimpleNamespace
import ast

""" hacked namespace uses `__all__` as a whitelist of symbols which are executable source code.
Non-whitelisted modules or runtime constituents are treated as 'data' which we call associative 
'articles' within the knowledge base, loaded at runtime."""

class KnowledgeBase:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.globals = SimpleNamespace()
        self.globals.__all__ = []
        self.initialize()

    def initialize(self):
        self._import_py_modules(self.base_dir)
        self._load_articles(self.base_dir)

    def _import_py_modules(self, directory):
        for path in directory.rglob("*.py"):
            if path.name.startswith("_"):
                continue
            try:
                module_name = path.stem
                spec = importlib.util.spec_from_file_location(module_name, str(path))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                setattr(self.globals, module_name, module)
                self.globals.__all__.append(module_name)
            except Exception as e:
                print(f"Error importing module {module_name}: {e}")

    def _load_articles(self, directory):
        for suffix in ['*.md', '*.txt']:
            for path in directory.rglob(suffix):
                try:
                    article_name = path.stem
                    content = path.read_text()
                    article = SimpleNamespace(
                        content=content,
                        path=str(path)
                    )
                    setattr(self.globals, article_name, article)
                except Exception as e:
                    print(f"Error loading article from {path}: {e}")

    def execute_query(self, query):
        try:
            parsed = ast.parse(query, mode='eval')
            result = eval(compile(parsed, '<string>', 'eval'), {'kb': self.globals})
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"

    def commit_changes(self):
        # TODO: Implement logic to write changes back to the file system
        pass

def initialize_kb(base_dir):
    return KnowledgeBase(base_dir)