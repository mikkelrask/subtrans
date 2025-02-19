# Subtitle Translator (English to Danish)

A Python application that uses local machine learning models to translate English subtitles (.srt files) to Danish.

## Features

- Translates subtitle files from English to Danish
- Uses local translation models (no internet required after initial model download)
- Preserves subtitle timing and formatting
- Handles multi-line dialogues and dialogue markers
- GPU acceleration support (CUDA)
- Batch processing with automatic skipping of already translated files
- Currently only supports English to Danish translations
- Supports `.srt` files
- Graceful handling of interruptions (Ctrl+C)
- Extracts subtitles from media files (requires ffmpeg)

## Requirements

- Python 3.x
- CUDA-capable GPU (optional, for faster processing)
- `ffmpeg` and `ffprobe` (for extracting subtitles from media files)

## Installation

### **Create and activate a virtual environment:**  
To keep the dependencies isolated, we'll create and activate a virtual environment.

**MacOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate 
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### **Install dependencies:**  
Use `pip` to install the dependencies.

```bash
pip install -r requirements.txt
```

## Usage
The script supports both single file and batch translation, and depending on your needs, you can choose to run one of the following commands, passing the path to the file or directory as an argument.

### Single File Translation
To translate a single English subtitle file, run:
```bash
python src/translator.py "path/to/your/file.en.srt"
```

### Batch Translation
To translate all English subtitle files in a directory and its subdirectories, run:
```bash
python src/batch_translator.py "path/to/your/directory"
```

#### Batch Processing Optimization
The batch processor includes an optimization feature that tracks changes in your media directory:

- Calculates a hash of the directory structure (including file sizes and modification times)
- Stores the hash in `~/.subtitle_translator_state.json`
- Only processes files when changes are detected
- Includes a `--force` flag to override the hash check

To force processing regardless of directory changes:
```bash
python src/batch_translator.py "path/to/your/directory" --force
```

This makes the script ideal for automated runs (e.g., via cron) as it will only perform translations when necessary.

Example cron job (running daily at 4 AM):
```bash
0 4 * * * /path/to/venv/bin/python /path/to/src/batch_translator.py /path/to/media/directory
```

### Subtitle Extraction
The project includes a tool to extract embedded subtitles from media files that have subtitles embedded in the media file itself:

```bash
# Interactive mode - shows available subtitle streams and prompts for selection
python src/subtitle_extractor.py "path/to/movie.mkv"

# Auto-select specific stream (e.g., first subtitle stream)
python src/subtitle_extractor.py "path/to/movie.mkv" --auto-select 0

# Extract and automatically translate to Danish
python src/subtitle_extractor.py "path/to/movie.mkv" --translate
```

Features:
- Lists all available subtitle streams with language and flags (forced, default, etc.)
- Interactive stream selection
- Automatic stream selection with --auto-select
- Direct translation of extracted subtitles with --translate
- Preserves subtitle formatting during extraction

**Requirements:**
- `ffmpeg` and `ffprobe` must be installed on your system
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - MacOS: `brew install ffmpeg`
  - Windows: Download from https://ffmpeg.org/download.html

## Notes

- The first run will download the translation model (approximately 300MB)
- Translations are performed locally using the Helsinki-NLP English to Danish model
- GPU acceleration is automatically used if available
- Directory hashing ensures efficient automated runs