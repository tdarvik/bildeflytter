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
        return datetime.fromtimestamp(os.path.getmtime(file_path)).year

def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

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

    file_hashes = []
    total_files = 0
    total_size = 0
    skipped_files = 0

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(valid_extensions):
                file_path = os.path.join(root, file)
                year = get_date_taken(file_path)

                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

                print(f"Processing {file} ({file_size_mb:.2f} MB)")

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
                    print(f"File already exists {file}")
                    skipped_files += 1
                    continue

                file_hashes.append(file_hash)

                destination_path = os.path.join(year_dir, file)

                if os.path.exists(destination_path):
                    conflict_file_hash = get_file_hash(destination_path)
                    
                    if file_hash == conflict_file_hash:
                        print(f"File {file} already exists at {destination_path}")
                        continue
                    else:
                        counter = 1
                        while True:
                            name, ext = os.path.splitext(file)
                            conflict_path = os.path.join(year_dir, f"{name}_{counter}{ext}")
                            if not os.path.exists(conflict_path):
                                destination_path = conflict_path
                                break
                            else:
                                conflict_file_hash = get_file_hash(conflict_path)
                                if file_hash == conflict_file_hash:
                                    print(f"File {file} already exists at {conflict_path}")
                                    destination_path = None
                                    skipped_files += 1
                                    break
                            counter += 1

                if destination_path:
                    shutil.copy2(file_path, destination_path)
                    print(f"Copied {file} ({file_size_mb:.2f} MB) to {destination_path}")
                else:
                    print(f"Skipping {file} as it already exists")            

    print(f"\nFinished processing all files.")
    print(f"Total files processed: {total_files}")
    print(f"Total size of processed files: {total_size:.2f} MB")
    print(f"Files skipped: {skipped_files}")

def check_dir(dir):
    if not os.path.isdir(dir):
        print(f"Cannot find dir {dir}")
        return 0
    return 1


def main():
    parser = argparse.ArgumentParser(description="Copy media files to year-based directories.")
    parser.add_argument("source", help="Full path to the source directory")
    parser.add_argument("destination", help="Full path to the destination directory")
    args = parser.parse_args()

    source_directory = os.path.abspath(args.source)
    destination_directory = os.path.abspath(args.destination)

    if not (check_dir(source_directory) & check_dir(source_directory)):
        return

    print(f"Source directory: {source_directory}")
    print(f"Destination directory: {destination_directory}")

    copy_files_by_year(source_directory, destination_directory)

if __name__ == "__main__":
    main()