import pytest
from pathlib import Path
from src.batch_translator import find_subtitle_files, needs_translation

def test_needs_translation(tmp_path):
    # Create a test file
    en_file = tmp_path / "test.en.srt"
    en_file.touch()
    
    # No da file exists yet
    assert needs_translation(en_file) == True
    
    # Create da file
    da_file = tmp_path / "test.da.srt"
    da_file.touch()
    
    # da file exists now
    assert needs_translation(en_file) == False 