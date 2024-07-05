# just in time namespace


@dataclass
class GrammarRule:
    """
    Represents a single grammar rule in a context-free grammar.
    
    Attributes:
        lhs (str): Left-hand side of the rule.
        rhs (List[Union[str, 'GrammarRule']]): Right-hand side of the rule, which can be terminals or other rules.
    """
    lhs: str
    rhs: List[Union[str, 'GrammarRule']]
    
    def __repr__(self):
        """
        Provide a string representation of the grammar rule.
        
        Returns:
            str: The string representation.
        """
        rhs_str = ' '.join([str(elem) for elem in self.rhs])
        return f"{self.lhs} -> {rhs_str}"

import mmap

class LargeCodebase:
    def __init__(self, file_path):
        self.file = open(file_path, 'r+b')
        self.mm = mmap.mmap(self.file.fileno(), 0)
        self.line_index = self._build_line_index()

    def _build_line_index(self):
        index = {}
        current_pos = 0
        for i, line in enumerate(iter(self.mm.readline, b'')):
            index[i+1] = current_pos
            current_pos = self.mm.tell()
        return index

    def get_line(self, line_number):
        if line_number in self.line_index:
            self.mm.seek(self.line_index[line_number])
            return self.mm.readline().decode('utf-8').strip()
        return None

    def execute(self, start_line=1):
        current_line = start_line
        while True:
            line = self.get_line(current_line)
            if line is None:
                break
            if line.startswith('#'):
                current_line += 1
                continue
            if line.startswith('GOTO'):
                current_line = int(line.split()[1])
                continue
            exec(line)
            current_line += 1

# Usage
codebase = LargeCodebase('very_large_file.txt')
codebase.execute()