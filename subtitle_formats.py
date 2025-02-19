from pathlib import Path
import pysrt
import ass

class SubtitleFormat:
    def read(self, file_path: str):
        raise NotImplementedError
        
    def save(self, subtitles, output_path: str):
        raise NotImplementedError
        
    def get_text(self, subtitle) -> str:
        raise NotImplementedError
        
    def set_text(self, subtitle, text: str):
        raise NotImplementedError

class SrtFormat(SubtitleFormat):
    def read(self, file_path: str):
        return pysrt.open(file_path)
    
    def save(self, subtitles, output_path: str):
        subtitles.save(output_path, encoding='utf-8')
    
    def get_text(self, subtitle) -> str:
        return subtitle.text
    
    def set_text(self, subtitle, text: str):
        subtitle.text = text

class AssFormat(SubtitleFormat):
    def read(self, file_path: str):
        with open(file_path, encoding='utf-8') as f:
            return ass.parse(f)
    
    def save(self, subtitles, output_path: str):
        with open(output_path, 'w', encoding='utf-8') as f:
            subtitles.dump_file(f)
    
    def get_text(self, subtitle) -> str:
        return subtitle.text
    
    def set_text(self, subtitle, text: str):
        subtitle.text = text

def get_subtitle_handler(file_path: str) -> SubtitleFormat:
    suffix = Path(file_path).suffix.lower()
    if suffix == '.srt':
        return SrtFormat()
    elif suffix == '.ass':
        return AssFormat()
    else:
        raise ValueError(f"Unsupported subtitle format: {suffix}") 