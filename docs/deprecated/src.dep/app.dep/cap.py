# /src/app/cap.py - CAP Theorem Runtime (Re)interpreter

import json
import os
import threading
from queue import Queue

# Homoiconistic Bytecode Representation
class Bytecode:
    def __init__(self, instructions):
        self.instructions = instructions
    
    def execute(self, context):
        for instruction in self.instructions:
            op, *args = instruction
            if hasattr(context, op):
                getattr(context, op)(*args)


# Core Object Definition with Homoiconistic State
class StatefulObject:
    def __init__(self, oid, state):
        self.oid = oid
        self.state = state
    
    def update_state(self, new_state):
        self.state = new_state

    def __repr__(self):
        # Represent object state as Python code (homoiconism)
        return f"StatefulObject('{self.oid}', {self.state})"


# CAP Interpreter with Fault-tolerant and Homoiconistic Capabilities
class CAPInterpreter:
    def __init__(self):
        self.objects = {}             # Dictionary to store objects
        self.logs = Queue()           # Queue to hold logs for fault-tolerance
        self.lock = threading.Lock()  # Lock for synchronizing state access

    def create_object(self, oid, initial_state):
        with self.lock:
            self.objects[oid] = StatefulObject(oid, initial_state)
            self.log_change(oid, initial_state)
            self.save_to_source()  # Save changes to the source code
    
    def update_object(self, oid, new_state):
        with self.lock:
            obj = self.objects.get(oid)
            if obj:
                obj.update_state(new_state)
                self.log_change(oid, new_state)
                self.save_to_source()  # Save changes to the source code
            
    def log_change(self, oid, state):
        log_entry = json.dumps({"oid": oid, "state": state})
        self.logs.put(log_entry)

    def persist_logs(self, log_file):
        with open(log_file, 'a') as f:
            while not self.logs.empty():
                f.write(self.logs.get() + "\n")

    def recover_from_logs(self, log_file):
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    oid, state = entry["oid"], entry["state"]
                    self.objects[oid] = StatefulObject(oid, state)

    def save_to_source(self):
        # Serialize current state to the source code representation
        with open(__file__, 'r') as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if line.strip().startswith("# State:"):
                break
            new_lines.append(line)

        # Append the current state as comments (homiconistic data)
        new_lines.append("\n# State:\n")
        for obj in self.objects.values():
            new_lines.append(f"# {repr(obj)}\n")
        
        with open(__file__, 'w') as f:
            f.writelines(new_lines)

# Homoiconistic example runner
def homoiconistic_example():
    bytecode = Bytecode(
        instructions=[
            ("create_object", "obj1", {"attribute": "value"}),
            ("update_object", "obj1", {"attribute": "new_value"})
        ]
    )
    cap = CAPInterpreter()
    cap.recover_from_logs('cap_logs.txt')
    bytecode.execute(cap)
    cap.persist_logs('cap_logs.txt')  # Persist logs after execution

def main():
    homoiconistic_example()

if __name__ == "__main__":
    main()



# State:
# StatefulObject('obj1', {'attribute': 'new_value'})
