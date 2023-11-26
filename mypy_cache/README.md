import os

def create_mypy_cache_readme():
    file_path = "mypy_cache/README.md"
    content = "This directory is used as a cache directory for mypy."

    with open(file_path, "w") as file:
        file.write(content)

# Create the README.md file in the mypy_cache directory
create_mypy_cache_readme()
