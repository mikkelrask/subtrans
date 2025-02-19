import pytest
from pathlib import Path
from src.translator import SubtitleTranslator
import torch

@pytest.mark.timeout(300)  # 5 minutes timeout for first run
def test_translate_text():
    translator = SubtitleTranslator()
    result = translator.translate_text("Hello world")
    assert isinstance(result, str)
    assert len(result) > 0

def test_translate_empty_text():
    translator = SubtitleTranslator()
    result = translator.translate_text("")
    assert result == ""

def test_translate_multiline():
    translator = SubtitleTranslator()
    text = "Hello\nWorld"
    result = translator.translate_text(text)
    assert "\n" in result

def test_translate_with_dialogue_marker():
    translator = SubtitleTranslator()
    text = "-Hello there"
    result = translator.translate_text(text)
    assert result.startswith("-") 

def test_translate_with_formatting():
    translator = SubtitleTranslator()
    text = "<i>Hello Github</i>"
    result = translator.translate_text(text)
    # Check that HTML tags are preserved
    assert result.startswith("<i>")
    assert result.endswith("</i>")
    # Make sure there's text between the tags
    content = result[3:-4]  # Remove <i> and </i>
    assert len(content) > 0

def test_translate_with_mixed_formatting():
    translator = SubtitleTranslator()
    text = "-<i>Hello</i> there"
    result = translator.translate_text(text)
    # Check that both dialogue marker and HTML tags are preserved
    assert result.startswith("-<i>")
    assert "</i>" in result 

def test_translate_with_complex_formatting():
    translator = SubtitleTranslator()
    text = "-<i>Hello</i> there, <b>world</b>!"
    result = translator.translate_text(text)
    # Check all formatting is preserved
    assert result.startswith("-<i>")
    assert "</i>" in result
    assert "<b>" in result
    assert "</b>" in result
    assert result.endswith("!")

def test_translate_multiline_with_formatting():
    translator = SubtitleTranslator()
    text = """<i>First line</i>
-Second line
<b>Third line</b>"""
    result = translator.translate_text(text)
    lines = result.split('\n')
    assert len(lines) == 3
    assert lines[0].startswith("<i>") and lines[0].endswith("</i>")
    assert lines[1].startswith("-")
    assert lines[2].startswith("<b>") and lines[2].endswith("</b>")

@pytest.mark.timeout(30)
def test_translate_long_text():
    translator = SubtitleTranslator()
    # Test with a longer piece of text to ensure it handles chunking correctly
    text = " ".join(["Hello world"] * 50)  # 100 words
    result = translator.translate_text(text)
    assert isinstance(result, str)
    assert len(result) > 0 

@pytest.mark.skipif(not torch.cuda.is_available(), 
                   reason="Test requires GPU")
def test_translate_with_gpu():
    translator = SubtitleTranslator(device="cuda")
    result = translator.translate_text("Hello world")
    assert isinstance(result, str)
    assert len(result) > 0 