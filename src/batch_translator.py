from pathlib import Path
import argparse
from translator import process_single_file
import hashlib
import json
import time
from typing import Optional

HASH_FILE = Path.home() / '.subtitle_translator_state.json'

def find_subtitle_files(directory: str) -> list[Path]:
    base_dir = Path(directory)
    return list(base_dir.rglob("*.en.srt"))

def needs_translation(srt_file: Path) -> bool:
    da_srt = srt_file.parent / f"{srt_file.stem[:-3]}.da.srt"
    return not da_srt.exists()

def calculate_directory_hash(directory: Path) -> str:
    hasher = hashlib.md5()
    
    srt_files = []
    for path in sorted(directory.rglob("*.en.srt")):
        stats = path.stat()
        file_info = f"{path}|{stats.st_size}|{stats.st_mtime}"
        srt_files.append(file_info)
    
    dir_content = "\n".join(srt_files)
    hasher.update(dir_content.encode())
    
    return hasher.hexdigest()

def load_last_hash() -> Optional[str]:
    if not HASH_FILE.exists():
        return None
    
    try:
        with open(HASH_FILE, 'r') as f:
            data = json.load(f)
            return data.get('last_hash')
    except (json.JSONDecodeError, FileNotFoundError):
        return None

def save_current_hash(hash_value: str) -> None:
    with open(HASH_FILE, 'w') as f:
        json.dump({
            'last_hash': hash_value,
            'last_check': time.time()
        }, f)

def process_directory(directory: str) -> None:
    try:
        base_dir = Path(directory)
        
        current_hash = calculate_directory_hash(base_dir)
        last_hash = load_last_hash()
        
        if current_hash == last_hash:
            print("No changes detected in directory structure since last run. Skipping processing.")
            return
        
        subtitle_files = find_subtitle_files(directory)
        
        if not subtitle_files:
            print(f"No .en.srt files found in {directory}")
            return
        
        files_to_process = [f for f in subtitle_files if needs_translation(f)]
        
        if not files_to_process:
            print(f"All {len(subtitle_files)} found subtitle files already have Danish translations!")
            save_current_hash(current_hash)
            return
        
        print(f"Found {len(subtitle_files)} subtitle files")
        print(f"Need to process {len(files_to_process)} files (skipping {len(subtitle_files) - len(files_to_process)} already translated)")
        
        for i, srt_file in enumerate(files_to_process, 1):
            print(f"\nProcessing file {i}/{len(files_to_process)}: {srt_file}")
            try:
                process_single_file(str(srt_file))
            except Exception as e:
                print(f"Error processing {srt_file}: {str(e)}")
        
        save_current_hash(current_hash)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting...")
        return 1
    
    return 0

def main():
    parser = argparse.ArgumentParser(description='Batch translate English SRT files to Danish')
    parser.add_argument('directory', help='Directory to search for .en.srt files')
    parser.add_argument('--force', action='store_true', help='Force processing even if no changes detected')
    
    try:
        args = parser.parse_args()
        
        if args.force:
            HASH_FILE.unlink(missing_ok=True)
        
        return process_directory(args.directory)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting...")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 