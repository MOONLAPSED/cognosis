import os
import subprocess
import sys


def append_to_file(filename, content):
    """Appends strings to a file in Ubuntu, handling potential errors."""
    if not isinstance(content, list):
        content = [content]  # Treat single string input as a list

    with open(filename, 'a') as file:
        for line in content:
            file.write(line + '\n')

    print(f"Content appended to {filename}")


def replace_text_in_file(file_name: str, old_content: str, new_content: str) -> None:
    """Replaces text in a file.

    Args:
        file_name: The name of the file to modify.
        old_content: The text to replace.
        new_content: The replacement text.
    """
    try:
        with open(file_name, 'r') as file:
            content = file.read()

        modified_content = content.replace(old_content, new_content)

        with open(file_name, 'w') as file:
            file.write(modified_content)

    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(-1)


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
    if len(sys.argv) != 4:
        print("Usage: script.py <file_name> <old_content> <new_content>", file=sys.stderr)
        sys.exit(-1)

    file_name, old_content, new_content = sys.argv[1:]
    replace_text_in_file(file_name, old_content, new_content)
