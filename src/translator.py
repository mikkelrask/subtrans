import warnings
warnings.filterwarnings("ignore", message=".*pip install sacremoses.*")

from transformers import pipeline
from pathlib import Path
import torch
import argparse
from src.subtitle_formats import get_subtitle_handler
from src.config import get_model_name

class SubtitleTranslator:
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        self.translator = pipeline(
            "translation",
            model=get_model_name(),
            device=device
        )

    def translate_text(self, text: str) -> str:
        if not text.strip():
            return ""
        
        lines = text.split('\n')
        translated_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            prefix = ""
            if line.startswith('-'):
                prefix = '-'
                line = line[1:].strip()
            
            result = self.translator(line, max_length=512)
            translated = result[0]['translation_text']
            
            if prefix:
                translated = f"{prefix}{translated}"
            
            translated_lines.append(translated)
        
        return '\n'.join(translated_lines)

    def translate_subtitle_file(self, input_path: str, output_path: str):
        handler = get_subtitle_handler(input_path)
        subs = handler.read(input_path)
        
        total = len(subs.events if hasattr(subs, 'events') else subs)
        items = subs.events if hasattr(subs, 'events') else subs
        
        for i, sub in enumerate(items, 1):
            print(f"[{input_path}] Translating subtitle {i}/{total}...")
            text = handler.get_text(sub)
            translated = self.translate_text(text)
            handler.set_text(sub, translated)
        
        handler.save(subs, output_path)
        print(f"Translation completed! Saved to: {output_path}")

def process_single_file(input_file: str) -> None:
    input_path = Path(input_file)
    
    if input_path.stem.endswith('.en'):
        output_path = input_path.parent / f"{input_path.stem[:-3]}.da{input_path.suffix}"
    else:
        output_path = input_path.parent / f"{input_path.stem}.da{input_path.suffix}"
    
    translator = SubtitleTranslator()
    translator.translate_subtitle_file(str(input_path), str(output_path))

def main():
    parser = argparse.ArgumentParser(description='Translate English SRT files to Danish')
    parser.add_argument('input', help='Path to the input .srt file')
    
    try:
        args = parser.parse_args()
        process_single_file(args.input)
        return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting...")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 