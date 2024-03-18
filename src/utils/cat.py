import os
import subprocess

def append_to_file(filename, content):
    """Appends strings to a file in Ubuntu, handling potential errors."""
    if not isinstance(content, list):
        content = [content]  # Treat single string input as a list

    with open(filename, 'a') as file:
        for line in content:
            file.write(line + '\n')

    print(f"Content appended to {filename}")

def main():
    home_dir = os.path.expanduser('~')  # Get user's home directory
    bashrc_path = os.path.join(home_dir, '.bashrc')

    # Strings to append (you can modify or get these from user input)
    strings_to_append = [
        'export OLLAMA_HOST=0.0.0.0',
        'export OLLAMA_ORIGINS=:127.0.0.1:11434',
        'export OLLAMA_PORT=11434',
        '# Custom alias',
        'alias lll="ls -alh"'
    ]

    append_to_file(bashrc_path, strings_to_append)

    # Making changes effective in the current session
    subprocess.run(["source", bashrc_path])

if __name__ == "__main__":
    main()
