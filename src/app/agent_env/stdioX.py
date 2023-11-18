import subprocess
import os
os.environ['XONSH_INTERACTIVE'] = 'False'

cleaned_code = "TODO"

# Run xonsh and capture stdout
result = subprocess.run(['xonsh', '--no-script-cache', cleaned_code], 
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

# Extract stdout and stderr
stdout = result.stdout.decode('utf-8')
stderr = result.stderr.decode('utf-8')


def get_result(cleaned_code):
    if stderr:
        return print({'error': stderr})
    else: 
        return print({'output': stdout})


"""
result = subprocess.run(['xonsh', '-c', cleaned_code], stdout=subprocess.PIPE)

The -c flag tells xonsh to interpret the cleaned_code string as Python code to execute.

Without -c, it assumes it is a filename and tries to run it as a script, resulting in the "No such file" error.
"""
