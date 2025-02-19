import pytest
from pathlib import Path
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def sample_srt(tmp_path):
    content = """1
00:00:01,000 --> 00:00:04,000
Hello world!

2
00:00:05,000 --> 00:00:09,000
How are you?
"""
    file = tmp_path / "test.en.srt"
    file.write_text(content)
    return file 