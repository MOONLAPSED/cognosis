#!/bin/bash

# File: setup_tests.sh
# Purpose: Run the application with the necessary parameters and baseline tests
# Usage: ./setup_tests.sh application_file

# Function to get the information of a file
get_file_info() {
  # Use -printf to format the output of stat
  stat -c "%i %n %F %A %U %g %s %Y %X %Z %h %b %B" "$1"
}

# Function to get the information of a service
get_service_info() {
  # Use -p to get the unit file and the unit file address
  systemctl show -p UnitFileState,FragmentPath "$1"
}

# Main code

# Check if the application file is provided as an argument
if [ -z "$1" ]; then
  # Use -n to suppress the newline
  echo -n "Error: No application file provided."
  # Use -e to enable interpretation of backslash escapes
  echo -e "\nUsage: ./setup_tests.sh application_file"
  exit 1
fi

# Check if the application file exists and is executable
if [ ! -f "$1" ] || [ ! -x "$1" ]; then
  # Use -n to suppress the newline
  echo -n "Error: Invalid application file."
  # Use -e to enable interpretation of backslash escapes
  echo -e "\nThe file must exist and be executable."
  exit 2
fi

# Get the application file name
app_file="$1"

# Get the application name by using basename
app_name="$(basename "$app_file" .sh)"

# Get the current unix time
current_time=$(get_time)

# Get the parameters for the UnixFilesystem class
inode=$(get_inode "$app_file")
# Use -r to get the pathname without following symbolic links
pathname=$(get_pathname -r "$app_file")
# Use -s to suppress the file name in the output
filetype=$(get_filetype -s "$app_file")
permissions=$(get_permissions "$app_file")
owner=$(get_owner "$app_file")
group_id=$(get_group_id "$app_file")
PID=$(get_PID "$app_name")
unit_file=$(get_unit_file "$app_name")
unit_file_addr=$(get_unit_file_addr "$app_name")
size=$(get_size "$app_file")
mtime=$(get_mtime "$app_file")
atime=$(get_atime "$app_file")
ctime=$(get_ctime "$app_file")
links_count=$(get_links_count "$app_file")
blocks=$(get_blocks "$app_file")
block_size=$(get_block_size "$app_file")

# Run the application with the parameters
./"$app_file" "$inode" "$pathname" "$filetype" "$permissions" "$owner" "$group_id" "$PID" "$unit_file" "$unit_file_addr" "$size" "$mtime" "$atime" "$ctime" "$links_count" "$blocks" "$block_size"
