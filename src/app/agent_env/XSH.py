# import subprocess
import os
os.environ['XONSH_INTERACTIVE'] = 'False'
# Run xonsh and capture stdout
result = subprocess.run(['xonsh', '--no-script-cache', cleaned_code], 
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

# Extract stdout and stderr 
stdout = result.stdout.decode('utf-8')
stderr = result.stderr.decode('utf-8')

# Return JSON response
if stderr:
   return jsonify({'error': stderr})
else: 
   return jsonify({'output': stdout})

"""
The key points:

    Run xonsh and capture standard output/error streams to result.
    Decode the byte streams to text before JSON serialization.
    Check stderr for any errors, return those in JSON.
    Otherwise, return standard output in the JSON response.

This handles the serialization issue by extracting the required output text rather than directly returning the CompletedProcess object.

The "No such file or directory" error indicates that xonsh is trying to run the Python print statement as an executable file rather than a Python code snippet.

This is happening because by default xonsh will interpret code passed on the command line as a filename to run unless we specify it is Python code.

We need to pass the -c flag to xonsh to indicate the command line argument is Python code rather than a script filename.

For example:

directory_path = "/home/runner/work/cognosis/cognosis"
if not os.path.isdir(directory_path):
    os.makedirs(directory_path)
os.chdir(directory_path)
result = subprocess.run(['xonsh', '-c', cleaned_code], stdout=subprocess.PIPE)

The -c flag tells xonsh to interpret the cleaned_code string as Python code to execute.

Without -c, it assumes it is a filename and tries to run it as a script, resulting in the "No such file" error.
"""

# Xonsh Shell Access
class Xonsh_Shell_Access:
    def __init__(self):
        self.env = Env(
            PATH=os.environ.get("PATH"),
            PWD=os.getcwd(),
            HOME=os.environ.get("HOME"),
            USER=os.environ.get("USER"),
            SHELL=os.environ.get("SHELL"),
        )
        self.aliases = Aliases()

    def execute(self, command):
        return self.aliases[command](self.env)

# Virtualized Access
class Virtualized_Access:
    def __init__(self, shell_access):
        self.shell_access = shell_access

    def execute(self, command):
        return self.shell_access.execute(command)

# File System Access
class File_System_Access:
    def __init__(self, shell_access):
        self.shell_access = shell_access

    def read(self, filepath):
        with open(filepath, 'r') as file:
            return file.read()

    def write(self, filepath, content):
        with open(filepath, 'w') as file:
            file.write(content)

    def execute(self, command):
        return self.shell_access.execute(command)

# Instantiate classes
xonsh_shell_access = Xonsh_Shell_Access()
virtualized_access = Virtualized_Access(xonsh_shell_access)
file_system_access = File_System_Access(xonsh_shell_access)
