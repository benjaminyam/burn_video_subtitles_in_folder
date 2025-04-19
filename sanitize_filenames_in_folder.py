import os
import re

def sanitize_filename(filename):
    """Replace or remove unsupported characters in the filename."""
    return re.sub(r'[^\w\-.]', '_', filename)

def sanitize_filenames_in_folder(folder_path):
    """Sanitize filenames for all files in the given folder."""
    for filename in os.listdir(folder_path):
        sanitized_name = sanitize_filename(filename)
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, sanitized_name)
        os.rename(old_path, new_path)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sanitize filenames in a folder.")
    parser.add_argument("folder_path", help="Path to the folder containing files to sanitize")
    args = parser.parse_args()

    sanitize_filenames_in_folder(args.folder_path)