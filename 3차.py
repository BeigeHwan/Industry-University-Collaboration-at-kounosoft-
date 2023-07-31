import os
import subprocess
import re

root_dir = r'E:\MODE360_촬영_데이터\촬영1_3차'
script_path = r'D:\#rename_mod\rename_cw.py'


# Function to extract the 13-digit number from a path
def extract_number(path):
    match = re.search(r'\d{13}', path)
    if match:
        return match.group()
    return None

# Function to recursively iterate through leaf folders
stack = []
def iterate_leaf_folders(folder):
    for dirpath, dirnames, filenames in os.walk(folder):
        if not dirnames:  # Leaf folder
            source_path = dirpath
            source_dirs = source_path.split('\\')
            if len(source_dirs) > 5:
                source_number = extract_number(source_dirs[5])
                if source_number:
                    destination_dirs = source_dirs[:]
                    destination_dirs[5] = source_number
                    del destination_dirs[-1]  # Remove the last element (-1 index)
                    destination_path = '\\'.join(destination_dirs)
                    destination_path = destination_path.replace('촬영1_3차', '촬영1_3차_변환') + r'\촬영'
                    command_line = f"python {script_path} {source_path} {destination_path}"
                    stack.append(command_line)

# Start iterating from the root directory
iterate_leaf_folders(root_dir)

# Execute the command lines
for command_line in stack:
    subprocess.call(command_line, shell=True, encoding='utf-8')
