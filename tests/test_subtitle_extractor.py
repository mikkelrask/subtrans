import pytest
from src.subtitle_extractor import format_stream_info, SubtitleExtractor
from pathlib import Path
from unittest.mock import patch
import json

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

def test_format_stream_info_minimal():
    stream = {
        'tags': {'language': 'eng'},
        'codec_name': 'srt'
    }
    info = format_stream_info(stream)
    assert 'Language: eng' in info
    assert 'Codec: srt' in info
    assert 'Title:' not in info
    assert 'Flags:' not in info

@pytest.mark.skipif(not Path("/usr/bin/ffmpeg").exists(),
                   reason="Requires ffmpeg")
def test_subtitle_extractor_init(tmp_path):
    test_file = tmp_path / "test.mkv"
    test_file.touch()
    
    extractor = SubtitleExtractor(str(test_file))
    assert extractor.media_file == test_file

    with pytest.raises(FileNotFoundError):
        SubtitleExtractor("nonexistent.mkv")

@pytest.mark.skipif(not Path("/usr/bin/ffmpeg").exists(),
                   reason="Requires ffmpeg")
def test_get_subtitle_streams(tmp_path):
    test_file = tmp_path / "test.mkv"
    test_file.touch()
    
    mock_streams = {
        'streams': [
            {
                'codec_type': 'subtitle',
                'codec_name': 'ass',
                'tags': {'language': 'eng'}
            }
        ]
    }
    
    with patch('subprocess.run') as mock_run:
        # Mock successful ffprobe call
        mock_run.return_value.stdout = json.dumps(mock_streams)
        mock_run.return_value.returncode = 0
        
        extractor = SubtitleExtractor(str(test_file))
        streams = extractor.get_subtitle_streams()
        
        assert len(streams) == 1
        assert streams[0]['codec_name'] == 'ass'
        assert streams[0]['tags']['language'] == 'eng' 