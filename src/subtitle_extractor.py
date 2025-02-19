import subprocess
import json
from pathlib import Path
import argparse
from typing import List, Dict
import shutil
from translator import process_single_file

def check_dependencies() -> bool:
    missing = []
    for cmd in ['ffmpeg', 'ffprobe']:
        if not shutil.which(cmd):
            missing.append(cmd)
    
    if missing:
        print("Error: Missing required dependencies:")
        for cmd in missing:
            print(f"  - {cmd}")
        print("\nPlease install ffmpeg:")
        print("  Ubuntu/Debian: sudo apt install ffmpeg")
        print("  MacOS: brew install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        return False
    return True

class SubtitleExtractor:
    def __init__(self, media_file: str):
        if not check_dependencies():
            raise RuntimeError("Required dependencies not found")
        
        self.media_file = Path(media_file)
        if not self.media_file.exists():
            raise FileNotFoundError(f"Media file not found: {media_file}")

    def get_subtitle_streams(self) -> List[Dict]:
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_streams',
            '-select_streams', 's',
            str(self.media_file)
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            return data.get('streams', [])
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error analyzing media file: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Error parsing ffprobe output: {e}")

    def extract_subtitle(self, stream_index: int) -> Path:
        output_path = self.media_file.with_suffix('.en.srt')
        
        if output_path.exists():
            output_path = self.media_file.with_suffix(f'.stream{stream_index}.en.srt')

        cmd = [
            'ffmpeg',
            '-v', 'quiet',
            '-i', str(self.media_file),
            '-map', f'0:s:{stream_index}',
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error extracting subtitle: {e}")

def format_stream_info(stream: Dict) -> str:
    info = []
    
    lang = stream.get('tags', {}).get('language', 'unknown')
    info.append(f"Language: {lang}")
    
    if 'tags' in stream and 'title' in stream['tags']:
        info.append(f"Title: {stream['tags']['title']}")
    
    dispositions = [k for k, v in stream.get('disposition', {}).items() if v == 1]
    if dispositions:
        info.append(f"Flags: {', '.join(dispositions)}")
    
    return ' | '.join(info)

def main():
    parser = argparse.ArgumentParser(description='Extract and translate subtitles from media files')
    parser.add_argument('media_file', help='Path to the media file')
    parser.add_argument('--auto-select', type=int, help='Automatically select stream index')
    parser.add_argument('--translate', action='store_true', help='Translate extracted subtitles to Danish')
    
    try:
        args = parser.parse_args()
        
        extractor = SubtitleExtractor(args.media_file)
        streams = extractor.get_subtitle_streams()
        
        if not streams:
            print("No subtitle streams found in the media file.")
            return 0
        
        if args.auto_select is not None:
            if 0 <= args.auto_select < len(streams):
                subtitle_path = extractor.extract_subtitle(args.auto_select)
                print(f"Extracted subtitles to: {subtitle_path}")
            else:
                print(f"Invalid stream index: {args.auto_select}")
                return 1
        else:
            print(f"\nAvailable subtitle streams for {Path(args.media_file).name}:")
            for i, stream in enumerate(streams):
                print(f"[{i}] {format_stream_info(stream)}")
            
            while True:
                try:
                    choice = input("\nSelect subtitle stream to extract (number): ")
                    stream_index = int(choice)
                    if 0 <= stream_index < len(streams):
                        subtitle_path = extractor.extract_subtitle(stream_index)
                        print(f"Extracted subtitles to: {subtitle_path}")
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
                except KeyboardInterrupt:
                    print("\nOperation cancelled by user. Exiting...")
                    return 1
        
        if args.translate and 'subtitle_path' in locals():
            print("\nTranslating extracted subtitles...")
            process_single_file(str(subtitle_path))
        
        return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting...")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 