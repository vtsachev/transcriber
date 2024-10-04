# file_manager.py

import os
import re

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_tmp_directory():
    tmp_dir = os.path.join(os.getcwd(), 'tmp')
    return create_directory(tmp_dir)

def create_transcripts_directory():
    transcripts_dir = os.path.join(os.getcwd(), 'transcripts')
    return create_directory(transcripts_dir)

def create_raw_transcripts_directory():
    raw_transcripts_dir = os.path.join(os.getcwd(), 'raw_transcripts')
    return create_directory(raw_transcripts_dir)

def get_unique_filename(base_name, extension, directory):
    """
    Generates a unique filename by appending an incremented number if the file already exists.

    Parameters:
    - base_name: The base name of the file without extension.
    - extension: The file extension, e.g., '.txt'.
    - directory: The directory where the file will be saved.

    Returns:
    - unique_filename: A unique filename that doesn't overwrite existing files.
    """
    filename = f"{base_name}{extension}"
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        return filename  # No conflict, return the original filename

    # Check for existing files with _n or _nn suffixes
    pattern = re.compile(rf"^{re.escape(base_name)}(?:_(\d+))?{re.escape(extension)}$")
    existing_files = [f for f in os.listdir(directory) if pattern.match(f)]

    # Extract existing suffix numbers
    suffix_numbers = []
    for f in existing_files:
        match = pattern.match(f)
        if match:
            if match.group(1):
                suffix_numbers.append(int(match.group(1)))
            else:
                suffix_numbers.append(0)

    # Find the next available suffix number
    next_suffix = max(suffix_numbers) + 1
    unique_filename = f"{base_name}_{next_suffix}{extension}"
    return unique_filename