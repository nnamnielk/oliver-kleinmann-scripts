import os
import hashlib
from pathlib import Path

def calculate_checksum(file_path):
    """Calculate MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def delete_duplicates(directory):
    """Delete files with duplicate checksums in the given directory."""
    checksums = {}
    directory = Path(directory)
    
    # First pass: Calculate checksums
    for file_path in directory.glob('*'):
        if file_path.is_file():
            checksum = calculate_checksum(file_path)
            if checksum in checksums:
                checksums[checksum].append(file_path)
            else:
                checksums[checksum] = [file_path]
    
    # Second pass: Delete duplicates
    deleted_files = []
    for checksum, file_list in checksums.items():
        if len(file_list) > 1:
            # Keep the first file, delete the rest
            for file_path in file_list[1:]:
                try:
                    file_path.unlink()
                    deleted_files.append(str(file_path))
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
    
    return deleted_files

if __name__ == "__main__":
    # Get directory path from user
    directory = input("Enter directory path: ")
    
    # Check if directory exists
    if not os.path.isdir(directory):
        print("Invalid directory path!")
        exit(1)
    
    # Delete duplicates and print results
    deleted = delete_duplicates(directory)
    
    if deleted:
        print("\nDeleted files:")
        for file in deleted:
            print(f"- {file}")
        print(f"\nTotal files deleted: {len(deleted)}")
    else:
        print("\nNo duplicate files found.") 
