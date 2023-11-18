import os
import hashlib

# Function to check for duplicate files based on content
def find_duplicates(directory):
    file_hashes = {}
    duplicates = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, 'rb') as file:
                file_hash = hashlib.sha256(file.read()).hexdigest()
            if file_hash in file_hashes:
                duplicates.append((file_path, file_hashes[file_hash]))
            else:
                file_hashes[file_hash] = file_path
    
    return duplicates

# Function to log operations
def log_operation(operation, filename):
    with open('operation_log.txt', 'a') as log_file:
        log_file.write(f"{operation} - {filename}\n")

# Function to perform file operations
def perform_file_operations():
    source_file = 'source_file.txt'
    target_file = 'target_file.txt'
    
    # Reading from source_file and appending to target_file
    with open(source_file, 'r') as source, open(target_file, 'a') as target:
        for line in source:
            target.write(line)
    log_operation("Append", target_file)
    
    # Searching for a specific keyword in target_file
    keyword = 'example'
    with open(target_file, 'r') as target:
        for line_number, line in enumerate(target, start=1):
            if keyword in line:
                print(f"Found '{keyword}' in line {line_number}")
    
    # Deleting target_file
    os.remove(target_file)
    log_operation("Delete", target_file)

if __name__ == "__main__":
    directory_to_check = '/path/to/your/directory'
    duplicates = find_duplicates(directory_to_check)
    
    if duplicates:
        print("Duplicate files found:")
        for duplicate_pair in duplicates:
            print(f"Duplicate 1: {duplicate_pair[0]}")
            print(f"Duplicate 2: {duplicate_pair[1]}")
    else:
        print("No duplicate files found.")
    
    perform_file_operations()
