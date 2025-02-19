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

def test_srt_format_handling(tmp_path):
    handler = SrtFormat()
    test_file = tmp_path / "test.srt"
    
    # Write test content
    content = """1
00:00:01,000 --> 00:00:04,000
Test subtitle

2
00:00:05,000 --> 00:00:09,000
<i>Formatted text</i>"""
    test_file.write_text(content)
    
    # Read and verify
    subs = handler.read(str(test_file))
    assert len(subs) == 2
    assert handler.get_text(subs[0]) == "Test subtitle"
    assert handler.get_text(subs[1]) == "<i>Formatted text</i>"
    
    # Test text modification
    handler.set_text(subs[0], "Modified text")
    assert handler.get_text(subs[0]) == "Modified text"
    
    # Test saving
    output_file = tmp_path / "output.srt"
    handler.save(subs, str(output_file))
    assert output_file.exists()

@pytest.mark.skipif(not Path("/usr/bin/ffmpeg").exists(), 
                   reason="Requires ffmpeg for ASS testing")
def test_ass_format_handling(tmp_path):
    handler = AssFormat()
    test_file = tmp_path / "test.ass"
    
    # Write test content with ASS formatting
    content = """[Script Info]
Title: Test

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:04.00,Default,,0,0,0,,Test subtitle
Dialogue: 0,0:00:05.00,0:00:09.00,Default,,0,0,0,,{\\i1}Formatted text{\\i0}"""
    test_file.write_text(content)
    
    # Read and verify
    subs = handler.read(str(test_file))
    assert len(subs.events) == 2
    assert handler.get_text(subs.events[0]) == "Test subtitle"
    assert "Formatted text" in handler.get_text(subs.events[1]) 