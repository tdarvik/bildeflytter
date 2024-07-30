import os
import shutil
from datetime import datetime
import argparse
import hashlib

def get_date_taken(file_path):
    try:
        return datetime.fromtimestamp(os.path.getmtime(file_path)).year
    except:
        return None

def get_file_hash(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def copy_files_by_year(source_dir, destination_dir):
    valid_extensions = (
        # Image formats
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp',
        # Video formats
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v',
        # RAW formats
        '.raw', '.arw', '.cr2', '.cr3', '.dng', '.nef', '.nrw', '.orf', 
        '.raf', '.rw2', '.pef', '.srw', '.x3f'
    )

    file_hashes = {}

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(valid_extensions):
                file_path = os.path.join(root, file)
                year = get_date_taken(file_path)
                
                if year is None:
                    year_dir = os.path.join(destination_dir, "Ukjent tid")
                else:
                    year_dir = os.path.join(destination_dir, str(year))
                
                if not os.path.exists(year_dir):
                    os.makedirs(year_dir)
                
                file_hash = get_file_hash(file_path)
                
                if file_hash in file_hashes:
                    print(f"Duplicate found: {file} is identical to {file_hashes[file_hash]}")
                    continue
                
                file_hashes[file_hash] = file

                destination_path = os.path.join(year_dir, file)
                counter = 1
                while os.path.exists(destination_path):
                    name, ext = os.path.splitext(file)
                    destination_path = os.path.join(year_dir, f"{name}_{counter}{ext}")
                    counter += 1

                shutil.copy2(file_path, destination_path)
                print(f"Copied {file} to {destination_path}")

def main():
    parser = argparse.ArgumentParser(description="Copy media files to year-based directories.")
    parser.add_argument("source", help="Full path to the source directory")
    parser.add_argument("destination", help="Full path to the destination directory")
    args = parser.parse_args()

    source_directory = os.path.abspath(args.source)
    destination_directory = os.path.abspath(args.destination)

    if not os.path.isdir(source_directory):
        print(f"Error: Source directory '{source_directory}' does not exist.")
        return

    if not os.path.isdir(destination_directory):
        print(f"Error: Destination directory '{destination_directory}' does not exist.")
        return

    print(f"Source directory: {source_directory}")
    print(f"Destination directory: {destination_directory}")

    copy_files_by_year(source_directory, destination_directory)

if __name__ == "__main__":
    main()