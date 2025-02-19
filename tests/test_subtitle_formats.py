import pytest
from src.subtitle_formats import get_subtitle_handler, SrtFormat, AssFormat
from pathlib import Path

def test_get_subtitle_handler_srt():
    handler = get_subtitle_handler("test.srt")
    assert isinstance(handler, SrtFormat)

def test_get_subtitle_handler_ass():
    handler = get_subtitle_handler("test.ass")
    assert isinstance(handler, AssFormat)

def test_get_subtitle_handler_invalid():
    with pytest.raises(ValueError):
        get_subtitle_handler("test.txt") 