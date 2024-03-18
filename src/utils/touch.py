import sys
import shutil
import os

def replace_text_in_file(fileName: str, old_content: str, newContent: str) -> None:
    """
    Replace text in a file with new content.

    Replace all occurrences of old_content with newContent in the file
    specified by fileName.

    :param fileName: The name of the file to modify.
    :type fileName: str
    :param old_content: The text to replace
    :type old_content: str
    :param newContent: The new content to replace old_content with
    :type newContent: str
    :return: None
    """
    with open(fileName, 'r') as file:
        content = file.read()

	# how many times old_content occurs in content
    count = content.count(old_content)
    # if count is not 1, then we can't replace the text
    if count != 1:
		# output error message to stderr and exit
        print(f"Error: {old_content} occurs {count} times in {fileName}.", file=sys.stderr)
        exit(-1)

	# replace old_content with new_content
    modified_content = content.replace(old_content, newContent)

    with open(fileName, 'w') as file:
        file.write(modified_content)

def create_or_replace_file(source: str, destination: str) -> None:
    """Create new file or replace existing file with new content."""
    try:
        if os.path.exists(destination):
            os.remove(destination)
        shutil.move(source, destination)
    except Exception:
        raise

if __name__ == "__main__":
    content_file = sys.argv[1]
    new_file = sys.argv[2]
    create_or_replace_file(content_file, new_file)
    sys.exit(0)


if __name__ == "__main__":
	try:
		file_name = sys.argv[1]
		old_content = sys.argv[2]
		new_content = sys.argv[3]

		replace_text_in_file(file_name, old_content, new_content)
	except Exception as e:
		print(e, file=sys.stderr)
		exit(-1)
exit(0)