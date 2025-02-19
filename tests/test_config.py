from src.config import get_source_patterns, get_target_suffix, get_model_name

def test_source_patterns():
    patterns = get_source_patterns()
    assert isinstance(patterns, list)
    assert all("*.en" in pattern for pattern in patterns)
    assert any(".srt" in pattern for pattern in patterns)
    assert any(".ass" in pattern for pattern in patterns)

def test_target_suffix():
    suffix = get_target_suffix()
    assert suffix == ".da"

def test_model_name():
    model = get_model_name()
    assert model == "Helsinki-NLP/opus-mt-en-da" 