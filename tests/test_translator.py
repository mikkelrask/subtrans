import pytest
from pathlib import Path
from src.translator import SubtitleTranslator

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