import pytest
from config import (
    get_source_patterns,
    get_target_suffix,
    get_model_name,
    SOURCE_LANG,
    TARGET_LANG,
    SUBTITLE_FORMATS
)

def test_source_patterns():
    patterns = get_source_patterns()
    assert isinstance(patterns, list)
    assert len(patterns) == len(SUBTITLE_FORMATS)
    for pattern in patterns:
        assert pattern.startswith(f"*.{SOURCE_LANG}")
        assert any(pattern.endswith(fmt) for fmt in SUBTITLE_FORMATS)

def test_target_suffix():
    suffix = get_target_suffix()
    assert suffix == f".{TARGET_LANG}"

def test_model_name():
    model = get_model_name()
    assert model == f"Helsinki-NLP/opus-mt-{SOURCE_LANG}-{TARGET_LANG}"

def test_subtitle_formats():
    assert ".srt" in SUBTITLE_FORMATS
    assert ".ass" in SUBTITLE_FORMATS
    assert all(fmt.startswith(".") for fmt in SUBTITLE_FORMATS)

def test_language_codes():
    assert len(SOURCE_LANG) >= 2  # Language codes should be at least 2 chars
    assert len(TARGET_LANG) >= 2
    assert SOURCE_LANG.islower()  # Should be lowercase
    assert TARGET_LANG.islower() 