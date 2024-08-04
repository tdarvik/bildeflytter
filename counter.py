import os
import argparse

def count_files(dir):
    valid_extensions = (
        # Image formats
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp',
        # Video formats
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v',
        # RAW formats
        '.raw', '.arw', '.cr2', '.cr3', '.dng', '.nef', '.nrw', '.orf',
        '.raf', '.rw2', '.pef', '.srw', '.x3f'
    )

    total_matching_files = 0

    for root, _, files in os.walk(dir):
        for file in files:
            if file.lower().endswith(valid_extensions):
                total_matching_files += 1
    print(f"Found {total_matching_files} in {dir}")

def main():
    parser = argparse.ArgumentParser(description="Copy media files to year-based directories.")
    parser.add_argument("dir", help="Full path to the source directory")
    args = parser.parse_args()

    dir = os.path.abspath(args.dir)

    if not (check_dir(dir)):
        return

    count_files(dir)

def check_dir(dir):
    if not os.path.isdir(dir):
        print(f"Cannot find dir {dir}")
        return 0
    return 1


if __name__ == "__main__":
    main()