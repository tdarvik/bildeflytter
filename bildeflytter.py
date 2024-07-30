import os
import shutil
from datetime import datetime
import argparse
import hashlib
from exif import Image

def get_date_taken(file_path):
    try:
        with open(file_path, 'rb') as image_file:
            img = Image(image_file)
            if img.has_exif:
                if hasattr(img, 'datetime_original'):
                    return datetime.strptime(img.datetime_original, '%Y:%m:%d %H:%M:%S').year
    except:
        pass

    # Fallback to modified date if EXIF data is not available
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
    total_files = 0
    total_size = 0
    skipped_files = 0
    replaced_files = 0

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(valid_extensions):
                file_path = os.path.join(root, file)
                year = get_date_taken(file_path)
                
                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                total_size += file_size_mb
                total_files += 1

                if year is None:
                    year_dir = os.path.join(destination_dir, "Ukjent tid")
                else:
                    year_dir = os.path.join(destination_dir, str(year))
                
                if not os.path.exists(year_dir):
                    os.makedirs(year_dir)
                
                file_hash = get_file_hash(file_path)
                
                if file_hash in file_hashes:
                    print(f"Duplicate found: {file} ({file_size_mb:.2f} MB) is identical to {file_hashes[file_hash]}")
                    skipped_files += 1
                    continue
                
                file_hashes[file_hash] = file

                destination_path = os.path.join(year_dir, file)
                if os.path.exists(destination_path):
                    dest_size_mb = os.path.getsize(destination_path) / (1024 * 1024)
                    dest_hash = get_file_hash(destination_path)
                    if file_hash == dest_hash:
                        print(f"Skipping {file} - File exists")
                        skipped_files += 1
                        continue
                    else:
                        print(f"File-hash not matching {file_path} ({file_size_mb:.2f} MB) and {destination_path} ({dest_size_mb:.2f} MB)")
                        skipped_files += 1
                        continue

                counter = 1
                while os.path.exists(destination_path):
                    name, ext = os.path.splitext(file)
                    destination_path = os.path.join(year_dir, f"{name}_{counter}{ext}")
                    counter += 1

                shutil.copy2(file_path, destination_path)
                print(f"Copied {file} ({file_size_mb:.2f} MB) to {destination_path}")

    print(f"\nFinished processing all files.")
    print(f"Total files processed: {total_files}")
    print(f"Total size of processed files: {total_size:.2f} MB")
    print(f"Files skipped (duplicates or smaller): {skipped_files}")
    print(f"Files replaced in destination: {replaced_files}")

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