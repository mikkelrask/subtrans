import pytest
from src.subtitle_extractor import format_stream_info

def test_format_stream_info():
    stream = {
        'tags': {'language': 'eng', 'title': 'Main'},
        'codec_name': 'ass',
        'disposition': {'default': 1}
    }
    info = format_stream_info(stream)
    assert 'Language: eng' in info
    assert 'Title: Main' in info
    assert 'Codec: ass' in info
    assert 'Flags: default' in info 