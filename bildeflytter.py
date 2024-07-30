import os
import shutil
from datetime import datetime
import argparse
import xxhash
from exif import Image
import multiprocessing
from functools import partial

VALID_EXTENSIONS = (
    # Image formats
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp',
    # Video formats
    '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v',
    # RAW formats
    '.raw', '.arw', '.cr2', '.cr3', '.dng', '.nef', '.nrw', '.orf', 
    '.raf', '.rw2', '.pef', '.srw', '.x3f'
)

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
    h = xxhash.xxh64()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def process_file(file_path, destination_dir, file_hashes):
    if not file_path.lower().endswith(VALID_EXTENSIONS):
        return

    file_size = os.path.getsize(file_path)
    file_hash = get_file_hash(file_path)
    year = get_date_taken(file_path)
    
    if file_hash in file_hashes:
        print(f"Duplicate found: {file_path} ({file_size / (1024 * 1024):.2f} MB) is identical to {file_hashes[file_hash]}")
        return

    file_hashes[file_hash] = file_path

    if year is None:
        year_dir = os.path.join(destination_dir, "Unknown_Year")
    else:
        year_dir = os.path.join(destination_dir, str(year))
    
    os.makedirs(year_dir, exist_ok=True)
    
    file_name = os.path.basename(file_path)
    destination_path = os.path.join(year_dir, file_name)
    
    if os.path.exists(destination_path):
        existing_file_hash = get_file_hash(destination_path)
        if existing_file_hash == file_hash:
            print(f"File already exists: {destination_path}")
            return
        else:
            counter = 1
            name, ext = os.path.splitext(file_name)
            while os.path.exists(destination_path):
                destination_path = os.path.join(year_dir, f"{name}_{counter}{ext}")
                counter += 1

    shutil.copy2(file_path, destination_path)
    print(f"Copied {file_path} ({file_size / (1024 * 1024):.2f} MB) to {destination_path}")

def copy_files_by_year(source_dir, destination_dir):
    file_hashes = {}

    file_paths = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(VALID_EXTENSIONS):
                file_paths.append(os.path.join(root, file))

    process_func = partial(process_file, destination_dir=destination_dir, file_hashes=file_hashes)

    with multiprocessing.Pool() as pool:
        pool.map(process_func, file_paths)

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