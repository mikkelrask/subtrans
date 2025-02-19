import pytest
from pathlib import Path
from batch_translator import find_subtitle_files, needs_translation, calculate_directory_hash

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

def test_find_subtitle_files(tmp_path):
    # Create various test files
    (tmp_path / "test1.en.srt").touch()
    (tmp_path / "test2.en.ass").touch()
    (tmp_path / "test3.da.srt").touch()  # Should be ignored
    (tmp_path / "test4.txt").touch()     # Should be ignored
    
    # Create a subdirectory with more files
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "test5.en.srt").touch()
    
    files = find_subtitle_files(str(tmp_path))
    assert len(files) == 3  # Should find 3 valid subtitle files
    assert any(f.name == "test1.en.srt" for f in files)
    assert any(f.name == "test2.en.ass" for f in files)
    assert any(f.name == "test5.en.srt" for f in files)

def test_calculate_directory_hash(tmp_path):
    # Create initial files
    (tmp_path / "test1.en.srt").touch()
    (tmp_path / "test2.en.ass").touch()
    
    # Get initial hash
    initial_hash = calculate_directory_hash(tmp_path)
    
    # Hash should be the same for same content
    assert calculate_directory_hash(tmp_path) == initial_hash
    
    # Adding a new file should change the hash
    (tmp_path / "test3.en.srt").touch()
    assert calculate_directory_hash(tmp_path) != initial_hash
    
    # Modifying a file should change the hash
    with open(tmp_path / "test1.en.srt", "w") as f:
        f.write("Some content")
    assert calculate_directory_hash(tmp_path) != initial_hash 