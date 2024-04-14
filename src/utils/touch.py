import sys
import os
import pytest


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


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: script.py <file_name> <old_content> <new_content>", file=sys.stderr)
        sys.exit(-1)

    file_name, old_content, new_content = sys.argv[1:]
    replace_text_in_file(file_name, old_content, new_content)


def test_replace_text_in_file():
    # Arrange
    file_name = "test_file.txt"
    old_content = "Hello"
    new_content = "Goodbye"
    expected_content = "Goodbye, world!"

    # Create a test file with initial content
    with open(file_name, 'w') as file:
        file.write("Hello, world!")

    # Act
    replace_text_in_file(file_name, old_content, new_content)

    # Assert
    with open(file_name, 'r') as file:
        content = file.read()
        assert content == expected_content

    # Clean up
    os.remove(file_name)


def test_replace_text_in_file_error():
    # Arrange
    file_name = "nonexistent_file.txt"
    old_content = "Hello"
    new_content = "Goodbye"

    # Act and Assert
    with pytest.raises(FileNotFoundError):
        replace_text_in_file(file_name, old_content, new_content)
