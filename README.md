# Subtitle Translator (English to Danish)

A Python application that uses local machine learning models to translate subtitles. Uses the **Helsinki-NLP English to Danish model** by default, but can be modified to use any of the **Helsinki-NLP translation models**.

## Features

- Translates subtitle files from English to Danish out of the box
- Uses local translation models (no internet required after initial model download/first run)
- Preserves all subtitle timings and formatting
- Handles multi-line dialogues and dialogue markers
- GPU acceleration support (CUDA)
- Batch processing with automatic skipping of already translated files
- Supports `.srt` and `.ass` files
- Extracts subtitles from media files

## Language Support

By default, this tool uses the **Helsinki-NLP English to Danish model**. You can easily change languages by editing `src/config.py`:

```python
# Translation settings
SOURCE_LANG = "en"  # Change source language (e.g., 'ja' for Japanese)
TARGET_LANG = "da"  # Change target language (e.g., 'en' for English)
```

This will automatically:
1. Use the correct Helsinki-NLP model
2. Look for files with the correct language suffix
3. Save translations with the appropriate target language suffix

**Examples of available models:**
- English to German: `Helsinki-NLP/opus-mt-en-de`

For more available models, see the [Helsinki-NLP models on Hugging Face](https://huggingface.co/Helsinki-NLP).

## Requirements

- Python 3.x
- CUDA-capable GPU (optional, for faster processing)
- `ffmpeg` (for subtitle extraction)

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/mikkelrask/subtrans.git
cd subtrans
```

2. **Create and activate a virtual environment:**

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

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

For detailed usage instructions and examples, please see the [Wiki](https://github.com/mikkelrask/subtrans/wiki).